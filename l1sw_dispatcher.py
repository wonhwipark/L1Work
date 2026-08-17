#!/usr/bin/env python3
"""Liveness and on-demand trigger agent for the skill update chain (Windows).

Lives outside the skills tree on purpose. Canonical migrations rewrite the
skills tree and have already broken scheduled tasks that pointed into it; the
component that owns liveness must not sit in the path being migrated.

Each cycle, in this order:

  1. heartbeat signal            -- always, before anything can fail
  2. self-heal own registration  -- re-register if the task is gone or stale
  3. fetch the remote trigger    -- one small raw GET, no API quota
  4. apply a requested interval  -- clamped to safe bounds
  5. run the engine if the nonce changed

Every step is best effort. Nothing here raises out of a cycle, and no failure
prevents the heartbeat from being observed.

    python l1sw_dispatcher.py install [--interval-min 30] [--dry-run]
    python l1sw_dispatcher.py run
    python l1sw_dispatcher.py status
    python l1sw_dispatcher.py uninstall [--dry-run]
    python l1sw_dispatcher.py make-trigger [--interval-min N] [--note TEXT]
"""
from __future__ import annotations

import argparse
import json
import locale
import os
import subprocess
import sys
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# The scheduler runs this windowless. A console child process launched from a
# parent that has no console gets a brand new window, so every subprocess here
# must suppress it explicitly -- otherwise a window pops up on every cycle.
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0

TASK_NAME = "l1sw-dispatcher"
ROOT = Path.home() / "l1sw-dispatcher"
CONFIG_PATH = ROOT / "config.json"
STATE_PATH = ROOT / "state.json"
LOCK_PATH = ROOT / "run.lock"
LOG_PATH = ROOT / "dispatcher.log"

SIGNAL_BASE = "https://github.com/wonhwipark/Fail/releases/download/signal-v1"
STAGES = ("heartbeat", "trigger-fired", "engine-ok", "engine-fail",
          "selfheal", "interval-changed")
SIGNALS = {s: f"{SIGNAL_BASE}/dispatcher-{s}.signal" for s in STAGES}

DEFAULT_CONFIG = {
    "trigger_url": "https://raw.githubusercontent.com/wonhwipark/L1Work/main/automation/trigger.json",
    "interval_min": 30,
    "interval_bounds_min": [10, 240],
    "allow_remote_interval": True,
    "engine_command": ["skillsilent", "run", "skill-updater", "update"],
    "engine_timeout_sec": 3600,
    "network_timeout_sec": 20,
    "lock_stale_min": 120,
}


# --- primitives -------------------------------------------------------------
def now() -> str:
    return datetime.now().astimezone().isoformat()


def log(message: str) -> None:
    line = f"{now()}  {message}"
    # Under pythonw.exe there is no console and sys.stdout is None, so a bare
    # print() raises. The scheduler runs this windowless, which is exactly the
    # path that must not fail; the file log below is the durable record.
    try:
        if sys.stdout is not None:
            print(line)
    except Exception:
        pass
    try:
        ROOT.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
            f.flush()
            os.fsync(f.fileno())
        if LOG_PATH.stat().st_size > 1_048_576:
            LOG_PATH.replace(LOG_PATH.with_suffix(".log.1"))
    except Exception:
        pass


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def read_json(path: Path, fallback: dict) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else dict(fallback)
    except Exception:
        return dict(fallback)


def load_config() -> dict:
    cfg = dict(DEFAULT_CONFIG)
    cfg.update(read_json(CONFIG_PATH, {}))
    return cfg


def load_state() -> dict:
    return read_json(STATE_PATH, {"last_seen_nonce": None, "runs": 0})


def send_signal(stage: str, timeout: float = 15.0) -> bool:
    """Best effort. Never raises; a signal failure changes nothing."""
    try:
        headers = {"User-Agent": "l1sw-dispatcher/1",
                   "Accept": "application/octet-stream",
                   "Cache-Control": "no-cache", "Pragma": "no-cache"}
        request = urllib.request.Request(SIGNALS[stage], headers=headers, method="GET")
        with urllib.request.urlopen(request, timeout=timeout):
            return True
    except Exception as exc:
        log(f"signal {stage} failed (non-fatal): {type(exc).__name__}: {exc}")
        return False


def decode_output(data: bytes) -> str:
    """Decode child output without ever raising.

    The tools invoked here disagree on encoding: the update engine emits UTF-8,
    while Windows console utilities emit the ANSI/OEM code page. Letting
    subprocess decode with text=True uses the locale codec, which raises on the
    other one -- the reader thread dies and the entire output is lost. Capturing
    bytes and decoding here keeps the diagnostics intact in both cases.
    """
    if not data:
        return ""
    for encoding in ("utf-8", locale.getpreferredencoding(False), "cp949", "latin-1"):
        try:
            return data.decode(encoding)
        except (UnicodeDecodeError, LookupError, TypeError):
            continue
    return data.decode("utf-8", errors="replace")


def ps(script: str, timeout: int = 60) -> str:
    try:
        out = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", script],
                             capture_output=True, timeout=timeout, creationflags=NO_WINDOW)
        return decode_output(out.stdout).strip()
    except Exception:
        return ""


# --- scheduled task ---------------------------------------------------------
def script_path() -> Path:
    return Path(__file__).resolve()


def pythonw() -> str:
    exe = Path(sys.executable)
    candidate = exe.with_name("pythonw.exe")
    return str(candidate if candidate.is_file() else exe)


def task_info() -> dict:
    # Built as one plain string with a single substitution. Concatenating
    # f-strings and plain strings here silently breaks brace escaping: only
    # the f-string parts collapse "{{" to "{", so the PowerShell body arrives
    # malformed and every query returns "not registered".
    script = (
        "$ErrorActionPreference='SilentlyContinue'; "
        "$t=Get-ScheduledTask -TaskName '@NAME@'; "
        "if ($null -eq $t) { '{}' } else { "
        "$i=Get-ScheduledTaskInfo -TaskName '@NAME@'; "
        "$a=$t.Actions[0]; "
        "@{ exists=$true; state=[string]$t.State; execute=[string]$a.Execute; "
        "arguments=[string]$a.Arguments; last_run=[string]$i.LastRunTime; "
        "next_run=[string]$i.NextRunTime; last_result=$i.LastTaskResult } | "
        "ConvertTo-Json -Compress }"
    ).replace("@NAME@", TASK_NAME)
    raw = ps(script)
    try:
        return json.loads(raw) if raw else {}
    except Exception:
        return {}


def register_task(interval_min: int, dry_run: bool = False) -> bool:
    command = f'"{pythonw()}" "{script_path()}" run'
    args = ["schtasks", "/create", "/tn", TASK_NAME, "/tr", command,
            "/sc", "MINUTE", "/mo", str(interval_min), "/f"]
    if dry_run:
        log("dry-run: " + " ".join(args))
        return True
    try:
        out = subprocess.run(args, capture_output=True, timeout=60, creationflags=NO_WINDOW)
        ok = out.returncode == 0
        message = (decode_output(out.stdout) or decode_output(out.stderr)).strip()
        log(f"register interval={interval_min}min rc={out.returncode} {message[:160]}")
        return ok
    except Exception as exc:
        log(f"register failed: {type(exc).__name__}: {exc}")
        return False


def registration_is_healthy(info: dict) -> bool:
    """The task must exist and its action must still point at this script."""
    if not info.get("exists"):
        return False
    arguments = info.get("arguments") or ""
    execute = info.get("execute") or ""
    if str(script_path()) not in arguments:
        return False
    if execute and not Path(execute.strip('"')).is_file():
        return False
    return True


def self_heal(cfg: dict) -> bool:
    """Repair an existing registration that has gone stale.

    Deliberately does not create a registration that was never installed:
    a manual `run` must not silently schedule anything. Absence is reported
    by `status` instead, where the operator can act on it.
    """
    info = task_info()
    if not info.get("exists"):
        log("self-heal: task not registered (run 'install' to schedule) -- skipping")
        return False
    if registration_is_healthy(info):
        return False
    log("self-heal: registration points at a stale path -> re-registering")
    if register_task(int(cfg["interval_min"])):
        send_signal("selfheal")
        return True
    return False


# --- trigger ----------------------------------------------------------------
def fetch_trigger(cfg: dict) -> dict | None:
    try:
        headers = {"User-Agent": "l1sw-dispatcher/1", "Cache-Control": "no-cache", "Pragma": "no-cache"}
        request = urllib.request.Request(cfg["trigger_url"], headers=headers, method="GET")
        with urllib.request.urlopen(request, timeout=int(cfg["network_timeout_sec"])) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        return payload if isinstance(payload, dict) else None
    except Exception as exc:
        log(f"trigger fetch failed: {type(exc).__name__}: {exc}")
        return None


def apply_interval(cfg: dict, trigger: dict) -> None:
    """Honour a remotely requested cadence, clamped to configured bounds."""
    if not cfg.get("allow_remote_interval", True):
        return
    requested = trigger.get("interval_min")
    if not isinstance(requested, int) or isinstance(requested, bool):
        return
    low, high = cfg["interval_bounds_min"]
    clamped = max(int(low), min(int(high), requested))
    if clamped != requested:
        log(f"requested interval {requested}min clamped to {clamped}min")
    if clamped == int(cfg["interval_min"]):
        return
    if register_task(clamped):
        cfg["interval_min"] = clamped
        atomic_json(CONFIG_PATH, cfg)
        send_signal("interval-changed")
        log(f"interval changed to {clamped}min")


def run_engine(cfg: dict) -> int:
    """Invoke the update engine.

    The engine is typically a shim (.cmd/.bat) resolved through PATH, so the
    command is passed as a single shell string. Mixing a list with shell=True
    is unreliable on Windows: only the first element is treated as the command.
    """
    parts = cfg["engine_command"]
    command = parts if isinstance(parts, str) else subprocess.list2cmdline(parts)
    log("engine start: " + command)
    try:
        out = subprocess.run(command, capture_output=True, shell=True,
                             timeout=int(cfg["engine_timeout_sec"]),
                             creationflags=NO_WINDOW)
        text = (decode_output(out.stdout) or decode_output(out.stderr)).strip()
        tail = text.splitlines()[-3:]
        log(f"engine rc={out.returncode} " + " | ".join(tail))
        return out.returncode
    except subprocess.TimeoutExpired:
        log(f"engine timed out after {cfg['engine_timeout_sec']}s")
        return -2
    except Exception as exc:
        log(f"engine invocation failed: {type(exc).__name__}: {exc}")
        return -1


# --- lock -------------------------------------------------------------------
def acquire_lock(cfg: dict) -> bool:
    try:
        ROOT.mkdir(parents=True, exist_ok=True)
        if LOCK_PATH.is_file():
            age_min = (datetime.now(timezone.utc).timestamp() - LOCK_PATH.stat().st_mtime) / 60
            if age_min < float(cfg["lock_stale_min"]):
                log(f"another cycle holds the lock (age {age_min:.0f}min) -- skipping")
                return False
            log(f"stale lock ({age_min:.0f}min) -- taking over")
        LOCK_PATH.write_text(str(os.getpid()), encoding="utf-8")
        return True
    except Exception:
        return True


def release_lock() -> None:
    try:
        LOCK_PATH.unlink(missing_ok=True)
    except Exception:
        pass


# --- cycle ------------------------------------------------------------------
def cycle() -> int:
    cfg = load_config()
    # Liveness first: a heartbeat must survive every failure below it.
    send_signal("heartbeat")

    if not acquire_lock(cfg):
        return 0
    try:
        state = load_state()
        state["runs"] = int(state.get("runs", 0)) + 1
        state["last_run_at"] = now()

        self_heal(cfg)

        trigger = fetch_trigger(cfg)
        if trigger is None:
            state["last_trigger_status"] = "UNREACHABLE"
            atomic_json(STATE_PATH, state)
            return 0

        apply_interval(cfg, trigger)

        nonce = str(trigger.get("nonce") or "")
        if not nonce:
            state["last_trigger_status"] = "NO_NONCE"
            atomic_json(STATE_PATH, state)
            return 0

        if nonce == state.get("last_seen_nonce"):
            state["last_trigger_status"] = "UNCHANGED"
            atomic_json(STATE_PATH, state)
            log(f"nonce unchanged ({nonce[:16]}) -- idle")
            return 0

        log(f"nonce changed -> {nonce[:16]}  note={trigger.get('note')}")
        send_signal("trigger-fired")
        state["last_trigger_status"] = "FIRED"
        state["last_trigger_at"] = now()
        # Record the nonce before running so a crashing engine cannot loop.
        state["last_seen_nonce"] = nonce
        atomic_json(STATE_PATH, state)

        rc = run_engine(cfg)
        state["last_engine_rc"] = rc
        state["last_engine_at"] = now()
        atomic_json(STATE_PATH, state)
        send_signal("engine-ok" if rc == 0 else "engine-fail")
        return 0
    except Exception as exc:
        log(f"cycle error (contained): {type(exc).__name__}: {exc}")
        return 0
    finally:
        release_lock()


# --- commands ---------------------------------------------------------------
def cmd_install(args) -> int:
    cfg = load_config()
    if args.interval_min:
        low, high = cfg["interval_bounds_min"]
        cfg["interval_min"] = max(int(low), min(int(high), args.interval_min))
    ok = register_task(int(cfg["interval_min"]), dry_run=args.dry_run)
    if not args.dry_run and ok:
        atomic_json(CONFIG_PATH, cfg)
        log(f"installed: every {cfg['interval_min']} minutes")
        log(f"config: {CONFIG_PATH}")
    return 0 if ok else 1


def cmd_uninstall(args) -> int:
    if args.dry_run:
        log(f"dry-run: schtasks /delete /tn {TASK_NAME} /f")
        return 0
    out = subprocess.run(["schtasks", "/delete", "/tn", TASK_NAME, "/f"],
                         capture_output=True, creationflags=NO_WINDOW)
    log(f"uninstall rc={out.returncode} {decode_output(out.stdout).strip()[:120]}")
    return out.returncode


def cmd_status(args) -> int:
    cfg = load_config()
    state = load_state()
    info = task_info()
    print("=" * 60)
    print("l1sw-dispatcher status")
    print("=" * 60)
    print(f"  script          : {script_path()}")
    print(f"  interval        : {cfg['interval_min']} min "
          f"(허용 {cfg['interval_bounds_min'][0]}~{cfg['interval_bounds_min'][1]})")
    print(f"  trigger_url     : {cfg['trigger_url']}")
    print(f"  engine_command  : {' '.join(cfg['engine_command'])}")
    print("  --- 예약 작업 ---")
    if info.get("exists"):
        print(f"  state           : {info.get('state')}")
        print(f"  last_run        : {info.get('last_run')}   result={info.get('last_result')}")
        print(f"  next_run        : {info.get('next_run')}")
        print(f"  registration    : {'정상' if registration_is_healthy(info) else '비정상 (다음 실행 시 자동 복구)'}")
    else:
        print("  등록되지 않음 -- 'install'을 실행하세요")
    print("  --- 실행 상태 ---")
    print(f"  cycles          : {state.get('runs', 0)}")
    print(f"  last_run_at     : {state.get('last_run_at')}")
    print(f"  last_trigger    : {state.get('last_trigger_status')} at {state.get('last_trigger_at')}")
    print(f"  last_seen_nonce : {(state.get('last_seen_nonce') or '')[:24]}")
    print(f"  last_engine_rc  : {state.get('last_engine_rc')} at {state.get('last_engine_at')}")
    print(f"  log             : {LOG_PATH}")
    return 0


def cmd_make_trigger(args) -> int:
    """Produce the trigger document to publish from the maintenance machine."""
    payload = {
        "nonce": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8],
        "issued_at": now(),
    }
    if args.note:
        payload["note"] = args.note
    if args.interval_min:
        payload["interval_min"] = args.interval_min
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {args.out}")
    print(text)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="liveness and trigger agent")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("install", help="register the scheduled task")
    p.add_argument("--interval-min", type=int, default=None)
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_install)

    p = sub.add_parser("run", help="execute one cycle")
    p.set_defaults(func=lambda a: cycle())

    p = sub.add_parser("status", help="show current state")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("uninstall", help="remove the scheduled task")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_uninstall)

    p = sub.add_parser("make-trigger", help="build a trigger document to publish")
    p.add_argument("--interval-min", type=int, default=None)
    p.add_argument("--note", default=None)
    p.add_argument("--out", default=None)
    p.set_defaults(func=cmd_make_trigger)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
