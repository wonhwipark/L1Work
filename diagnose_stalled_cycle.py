#!/usr/bin/env python3
"""Read-only diagnosis of a stalled skill-updater scheduled cycle (Windows).

Run on the affected machine. Touches nothing: no installs, no config writes,
no scheduled-task changes, and deliberately no requests to observation signal
assets (that would corrupt the remote delta measurement).

    python diagnose_stalled_cycle.py

Writes diagnosis_<timestamp>.json next to itself and prints a verdict.
"""
from __future__ import annotations

import json
import os
import socket
import ssl
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

# Windows consoles default to a legacy codepage; force UTF-8 so the Korean
# verdict text is readable on the machine being diagnosed.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HOME = Path.home()
CANONICAL = HOME / "l1sw-private-skills"
ENTRY = HOME / ".claude" / "skills"
LEGACY_MAIN = HOME / ".claude" / "main"
TASK_NAME_PATTERN = "skill|updater|autotask|job"
WATCHED_SKILLS = ("skill-updater", "job-list", "l1_fla", "autotask-builder", "skillsilent")

report: dict = {"generated_at": datetime.now().astimezone().isoformat(), "host": socket.gethostname()}


def ps(script: str) -> str:
    """Run PowerShell and return stdout ('' on failure)."""
    try:
        out = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", script],
            capture_output=True, text=True, timeout=90,
        )
        return out.stdout.strip()
    except Exception:
        return ""


def section(title: str) -> None:
    print(f"\n{'=' * 66}\n{title}\n{'=' * 66}")


# --- A. scheduled tasks -----------------------------------------------------
def collect_tasks() -> list:
    raw = ps(
        "$r=@(); Get-ScheduledTask | Where-Object { $_.TaskName -match '" + TASK_NAME_PATTERN + "' } | "
        "ForEach-Object { $t=$_; $i=Get-ScheduledTaskInfo -TaskName $t.TaskName -TaskPath $t.TaskPath; "
        "$acts=@(); foreach ($a in $t.Actions) { $acts += @{ execute=[string]$a.Execute; "
        "arguments=[string]$a.Arguments; workdir=[string]$a.WorkingDirectory } } "
        "$trg=@(); foreach ($x in $t.Triggers) { $trg += @{ type=$x.CimClass.CimClassName; "
        "start=[string]$x.StartBoundary; enabled=[string]$x.Enabled; "
        "interval=[string]$x.Repetition.Interval } } "
        "$r += @{ name=$t.TaskName; path=$t.TaskPath; state=[string]$t.State; "
        "last_run=[string]$i.LastRunTime; next_run=[string]$i.NextRunTime; "
        "last_result=$i.LastTaskResult; actions=$acts; triggers=$trg } }; "
        "$r | ConvertTo-Json -Depth 6 -Compress"
    )
    if not raw:
        return []
    try:
        data = json.loads(raw)
        return data if isinstance(data, list) else [data]
    except Exception:
        return []


def referenced_paths(task: dict) -> list:
    """Extract filesystem paths an action depends on, and whether they exist."""
    found = []
    for act in task.get("actions") or []:
        for token in [act.get("execute", "")] + (act.get("arguments", "") or "").split():
            token = token.strip('"')
            if len(token) > 3 and (":" in token or token.startswith("\\\\")) and ("\\" in token or "/" in token):
                found.append({"path": token, "exists": Path(token).exists()})
    return found


# --- D/F. canonical layout & versions ---------------------------------------
def read_version(skill: str) -> dict:
    root = CANONICAL / skill
    info = {"canonical_root_exists": root.is_dir(), "version": None, "entry_files": None}
    vf = root / "VERSION"
    if vf.is_file():
        try:
            info["version"] = vf.read_text(encoding="utf-8").strip()
        except Exception:
            pass
    ent = ENTRY / skill
    if ent.is_dir():
        try:
            info["entry_files"] = sorted(p.name for p in ent.iterdir())
        except Exception:
            pass
    return info


def read_updater_config() -> dict:
    out = {"path": None, "readable": False, "job_sync_enabled": None,
           "target_count": None, "has_job_list": None, "has_l1_fla": None, "mode": None}
    for cand in (CANONICAL / "skill-updater" / "data" / "config" / "skill-updater.json",
                 LEGACY_MAIN / "skill-updater" / "config" / "skill-updater.json"):
        if cand.is_file():
            out["path"] = str(cand)
            try:
                cfg = json.loads(cand.read_text(encoding="utf-8"))
                out["readable"] = True
                out["job_sync_enabled"] = bool((cfg.get("job_sync") or {}).get("enabled", False))
                targets = [t for t in (cfg.get("targets") or []) if t.get("enabled", True)]
                out["target_count"] = len(targets)
                names = {t.get("name") for t in targets}
                out["has_job_list"] = "job-list" in names
                out["has_l1_fla"] = "l1_fla" in names
                out["mode"] = (cfg.get("source") or {}).get("mode")
            except Exception as exc:
                out["error"] = f"{type(exc).__name__}: {exc}"
            break
    return out


# --- E. updater run history -------------------------------------------------
def recent_updater_runs(limit: int = 12) -> dict:
    out = {"log_root": None, "recent": [], "last_run_json": None}
    logs = CANONICAL / "skill-updater" / "output" / "logs"
    if logs.is_dir():
        out["log_root"] = str(logs)
        try:
            entries = sorted(logs.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)[:limit]
            out["recent"] = [{"name": p.name,
                              "mtime": datetime.fromtimestamp(p.stat().st_mtime).astimezone().isoformat()}
                             for p in entries]
        except Exception:
            pass
    lr = CANONICAL / "skill-updater" / "data" / "state" / "runtime" / "state" / "last_run.json"
    if not lr.is_file():
        lr = CANONICAL / "skill-updater" / "data" / "state" / "last_run.json"
    if lr.is_file():
        try:
            d = json.loads(lr.read_text(encoding="utf-8"))
            out["last_run_json"] = {k: d.get(k) for k in
                                    ("run_id", "action", "status", "phase", "started_at", "completed_at")}
        except Exception:
            pass
    return out


def joblist_evidence() -> dict:
    out = {"runs": [], "install_observations": None, "observations": None}
    base = CANONICAL / "job-list" / "output"
    runs = base / "runs"
    if runs.is_dir():
        try:
            out["runs"] = sorted((p.name for p in runs.iterdir() if p.is_dir()), reverse=True)[:10]
        except Exception:
            pass
    for key, rel in (("install_observations", "install-observations"), ("observations", "observations")):
        d = base / rel
        if d.is_dir():
            try:
                out[key] = sorted(p.name for p in d.iterdir())[:10]
            except Exception:
                pass
    return out


# --- H. network (never touches signal assets) -------------------------------
def check_network() -> dict:
    targets = {
        "api.github.com": "https://api.github.com/rate_limit",
        "raw.githubusercontent.com": "https://raw.githubusercontent.com/wonhwipark/L1Work/main/automation/job-list.json",
    }
    results = {}
    for label, url in targets.items():
        entry = {"url": url, "reachable": False, "status": None, "error": None, "tls_verified": None}
        for verify in (True, False):
            ctx = ssl.create_default_context()
            if not verify:
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "stall-diagnosis/1"}, method="GET")
                with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
                    entry.update(reachable=True, status=getattr(resp, "status", 200), tls_verified=verify)
                break
            except urllib.error.HTTPError as exc:
                # An HTTP status means the host answered: the network path works.
                # Only the resource is wrong, which is not a connectivity fault.
                entry.update(reachable=True, status=exc.code, tls_verified=verify,
                             error=f"HTTP {exc.code} (연결은 성공, 리소스 응답만 비정상)")
                break
            except Exception as exc:
                entry["error"] = f"{type(exc).__name__}: {exc}"
        results[label] = entry
    results["proxy_env"] = {k: os.environ.get(k) for k in
                            ("HTTPS_PROXY", "HTTP_PROXY", "https_proxy", "http_proxy") if os.environ.get(k)}
    return results


# --- verdict ----------------------------------------------------------------
def verdict(rep: dict) -> list:
    findings = []
    tasks = rep["scheduled_tasks"]
    updater_tasks = [t for t in tasks if "updater" in (t.get("name") or "").lower()
                     or "skill" in (t.get("name") or "").lower()]

    if not tasks:
        findings.append(("CRITICAL", "TASK_NOT_REGISTERED",
                         "skill-updater 관련 예약 작업이 하나도 없습니다. cron이 애초에 등록돼 있지 않습니다."))
    for t in updater_tasks:
        missing = [p["path"] for p in t.get("_paths", []) if not p["exists"]]
        rc = t.get("last_result")
        if missing:
            findings.append(("CRITICAL", "TASK_PATHS_STALE",
                             f"[{t['name']}] 실행 경로가 존재하지 않습니다 (canonical 이관으로 끊긴 것으로 보임): "
                             + "; ".join(missing)))
        if rc not in (0, None):
            findings.append(("CRITICAL", "TASK_LAUNCH_FAILED",
                             f"[{t['name']}] LastTaskResult={rc} "
                             f"(2=파일 없음, 267011=아직 실행 안 됨). last_run={t.get('last_run')}"))
        if str(t.get("state")).lower() == "disabled":
            findings.append(("CRITICAL", "TASK_DISABLED", f"[{t['name']}] 작업이 비활성 상태입니다."))
        if rc == 0 and not missing:
            findings.append(("INFO", "TASK_OK",
                             f"[{t['name']}] 정상 실행 이력. last_run={t.get('last_run')}"))

    cfg = rep["updater_config"]
    if not cfg["path"]:
        findings.append(("CRITICAL", "CONFIG_MISSING", "skill-updater config를 찾을 수 없습니다."))
    elif not cfg["readable"]:
        findings.append(("CRITICAL", "CONFIG_UNREADABLE", f"config 파싱 실패: {cfg.get('error')}"))
    else:
        if cfg["has_job_list"] is False:
            findings.append(("CRITICAL", "TARGET_MISSING", "targets에 job-list가 없습니다."))
        if cfg["has_l1_fla"] is False:
            findings.append(("WARN", "CANARY_MISSING", "targets에 l1_fla가 없습니다 (카나리아 판정 무효)."))
        findings.append(("INFO", "CONFIG_OK",
                         f"config={cfg['path']} mode={cfg['mode']} targets={cfg['target_count']} "
                         f"job_sync={cfg['job_sync_enabled']}"))

    net = rep["network"]
    for label in ("api.github.com", "raw.githubusercontent.com"):
        info = net.get(label, {})
        if not info.get("reachable"):
            findings.append(("CRITICAL", "NETWORK_BLOCKED",
                             f"{label} 연결 실패: {info.get('error')}"))
            continue
        if info.get("tls_verified") is False:
            findings.append(("WARN", "TLS_UNVERIFIED", f"{label}는 TLS 검증 없이만 접근됩니다."))
        if info.get("status") and not (200 <= int(info["status"]) < 400):
            findings.append(("INFO", "NETWORK_REACHABLE",
                             f"{label} 연결 정상 (HTTP {info['status']} — 경로만 다름, 차단 아님)"))

    lr = rep["updater_runs"].get("last_run_json")
    if lr:
        findings.append(("INFO", "LAST_UPDATER_RUN",
                         f"status={lr.get('status')} completed_at={lr.get('completed_at')}"))
    if not rep["updater_runs"]["recent"]:
        findings.append(("WARN", "NO_UPDATER_LOGS", "skill-updater 로그 디렉터리가 비어 있거나 없습니다."))

    return findings


def main() -> int:
    section("A. 예약 작업 (Scheduled Tasks)")
    tasks = collect_tasks()
    for t in tasks:
        t["_paths"] = referenced_paths(t)
        print(f"\n  {t.get('path','')}{t.get('name')}")
        print(f"    state={t.get('state')} last_result={t.get('last_result')}")
        print(f"    last_run={t.get('last_run')}  next_run={t.get('next_run')}")
        for a in t.get("actions") or []:
            print(f"    exec: {a.get('execute')}")
            if a.get("arguments"):
                print(f"    args: {a.get('arguments')}")
        for p in t["_paths"]:
            print(f"      [{'OK ' if p['exists'] else 'MISSING'}] {p['path']}")
    if not tasks:
        print("  (일치하는 예약 작업 없음)")
    report["scheduled_tasks"] = tasks

    section("B. 설치 레이아웃 / 버전")
    report["skills"] = {s: read_version(s) for s in WATCHED_SKILLS}
    for name, info in report["skills"].items():
        print(f"  {name:20} version={info['version']}  canonical={info['canonical_root_exists']}  "
              f"entry={info['entry_files']}")
    report["legacy_main_exists"] = LEGACY_MAIN.is_dir()
    print(f"  legacy ~/.claude/main 존재: {report['legacy_main_exists']}")

    section("C. skill-updater config")
    report["updater_config"] = read_updater_config()
    print("  " + json.dumps(report["updater_config"], ensure_ascii=False, indent=2).replace("\n", "\n  "))

    section("D. skill-updater 실행 이력")
    report["updater_runs"] = recent_updater_runs()
    print(f"  last_run.json: {report['updater_runs']['last_run_json']}")
    for e in report["updater_runs"]["recent"][:8]:
        print(f"    {e['mtime']}  {e['name']}")

    section("E. job-list 로컬 evidence")
    report["job_list_evidence"] = joblist_evidence()
    print("  " + json.dumps(report["job_list_evidence"], ensure_ascii=False, indent=2).replace("\n", "\n  "))

    section("F. 네트워크 (신호 asset은 건드리지 않음)")
    report["network"] = check_network()
    for k, v in report["network"].items():
        if k == "proxy_env":
            print(f"  proxy_env: {v}")
        else:
            print(f"  {k:28} reachable={v['reachable']} status={v['status']} "
                  f"tls_verified={v['tls_verified']} {v['error'] or ''}")

    section("VERDICT")
    findings = verdict(report)
    report["findings"] = [{"severity": s, "code": c, "detail": d} for s, c, d in findings]
    for sev in ("CRITICAL", "WARN", "INFO"):
        for s, c, d in findings:
            if s == sev:
                print(f"  [{sev:8}] {c}: {d}")

    out = Path(__file__).resolve().parent / f"diagnosis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"\n리포트 저장: {out}")
    print("이 JSON을 그대로 붙여넣으면 원인 판정과 복구 절차를 이어서 진행할 수 있습니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
