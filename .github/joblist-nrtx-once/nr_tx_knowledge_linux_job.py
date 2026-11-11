#!/usr/bin/env python3
"""One-shot NR L1 Tx knowledge research with in-house read-only execution.

No source or canonical knowledge edits. Job-list owns the sole activation and
run ID. All local results stay inside the in-house environment.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time

JOB_ID = "JOB-20261112-NR-L1TX-KNOWLEDGE-MSC-EXEC-01"
PROFILE = "nr-l1tx-knowledge-research-linux"
RESULT = "output/nr_tx_knowledge_research/latest_result.json"
PROMPT = "references/NR_TX_KNOWLEDGE_RESEARCH_ORCHESTRATION_v0436.md"
_RUN = re.compile(r"core_\d{8}_\d{6}_[0-9a-f]{8}\Z")
_EXCLUDE_PATHS = {".git", "build", "out", "output", "cache", "tmp", "temp"}

def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

def _atomic_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", prefix=".nrtx-",
                                     dir=path.parent, delete=False) as handle:
        json.dump(obj, handle, indent=2, sort_keys=True, ensure_ascii=False)
        handle.write("\n")
        temporary = Path(handle.name)
    os.replace(temporary, path)

def _read_local(path: Path, limit: int = 1000000) -> str:
    if path.is_symlink() or not path.is_file():
        raise RuntimeError("LOCAL_POLICY_UNAVAILABLE")
    info = path.stat(follow_symlinks=False)
    if not stat.S_ISREG(info.st_mode) or info.st_size > limit or not info.st_size:
        raise RuntimeError("LOCAL_POLICY_INVALID")
    return path.read_text(encoding="utf-8")

def _run_git(root: Path, *args: str) -> str:
    try:
        r = subprocess.run(["git", "-C", str(root), *args], timeout=25,
                           stdin=subprocess.DEVNULL, capture_output=True, check=False)
    except (OSError, subprocess.TimeoutExpired):
        raise RuntimeError("SOURCE_GIT_UNAVAILABLE")
    if r.returncode or len(r.stdout) > 100000:
        raise RuntimeError("SOURCE_GIT_IDENTITY_UNVERIFIED")
    return r.stdout.decode("utf-8", "replace").strip()

def _installed_skill(home: Path, skill: str) -> Path:
    for parent in (home / "l1sw-private-skills", home / ".claude" / "skills"):
        candidate = parent / skill
        if candidate.is_symlink() or not candidate.is_dir():
            continue
        policy = candidate / "SKILL.md"
        try:
            _read_local(policy)
            return candidate
        except (OSError, RuntimeError, UnicodeError):
            pass
    raise RuntimeError("SKILL_NOT_FOUND_" + skill.upper().replace("-", "_"))

def preflight(root: Path, home: Path) -> dict:
    if sys.platform != "linux" or os.name != "posix" or os.geteuid() == 0:
        raise RuntimeError("LINUX_NONROOT_REQUIRED")
    if root.is_symlink() or root.resolve() != home / "l1sw-private-skills" / "job-list":
        raise RuntimeError("JOB_ROOT_NOT_CANONICAL")
    if os.environ.get("JOB_LIST_JOB_ID") != JOB_ID or os.environ.get("JOB_LIST_PROFILE") != PROFILE:
        raise RuntimeError("JOB_RUNNER_IDENTITY_UNVERIFIED")
    run_id = os.environ.get("JOB_LIST_RUN_ID", "")
    if not _RUN.fullmatch(run_id):
        raise RuntimeError("JOB_RUN_ID_INVALID")
    source = home / "Project" / "smp1900"
    if source.is_symlink() or not source.is_dir() or source.resolve() != source:
        raise RuntimeError("SOURCE_ROOT_NOT_FOUND")
    head = _run_git(source, "rev-parse", "--verify", "HEAD")
    branch = _run_git(source, "rev-parse", "--abbrev-ref", "HEAD")
    if not re.fullmatch("[0-9a-fA-F]{40,64}", head):
        raise RuntimeError("SOURCE_REVISION_INVALID")
    dirty = bool(_run_git(source, "status", "--porcelain", "--untracked-files=no"))
    installed = {}
    for name in ("l1-knowledge-updater", "code-analyzer", "doc-converter"):
        installed[name] = _installed_skill(home, name)
    executable = shutil.which("opencode") or shutil.which("opencode2")
    if not executable or not Path(executable).is_file() or not os.access(executable, os.X_OK):
        raise RuntimeError("OPENCODE_CLI_NOT_FOUND")
    prompt = _read_local(root / PROMPT, limit=30000)
    return {"source": source, "source_revision": head, "branch": branch,
            "dirty": dirty, "installed": installed,
            "exe": executable, "prompt": prompt, "run_id": run_id}

def opencode_permissions() -> dict:
    # Maximal discoverability for installed analysis skills, but no direct
    # edit/patch/write, no arbitrary shell, no external web tools.
    # The exact SkillSilent action contract remains the actual permission gate.
    return {
        "*": "deny",
        "read": "allow", "glob": "allow", "grep": "allow", "list": "allow",
        "skill": "allow", "external_directory": "allow", "task": "allow",
        "edit": "deny", "write": "deny", "apply_patch": "deny",
        "webfetch": "deny", "websearch": "deny",
        "bash": {
            "skillsilent run l1-knowledge-updater *": "allow",
            "skillsilent run code-analyzer *": "allow",
            "skillsilent run doc-converter *": "allow",
            "skillsilent run l1-fix-workflow *": "allow",
            "skillsilent run work-ledger-kernel *": "allow",
            "skillsilent run l1-github *": "allow",
            "git rev-parse *": "allow", "git status *": "allow",
            "git log *": "allow", "git show *": "allow", "git grep *": "allow",
            "rg *": "allow", "ls *": "allow", "pwd": "allow",
            "*": "deny"
        }
    }

def main_run(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    result = {
        "schema_version": 1, "job_id": JOB_ID, "profile": PROFILE,
        "status": "BLOCKED", "reason_codes": [], "job_run_id": None,
        "started_at": _now(), "completed_at": None,
        "source_write": False, "group_write": False, "external_export": False,
        "analysis_status": "NOT_RUN", "msc_status": "NOT_RUN",
        "knowledge_updater_status": "NOT_RUN", "independent_review": "NOT_RUN",
        "run_catalog": "NOT_VERIFIED"
    }
    try:
        runtime = preflight(root, Path.home().resolve())
        result["job_run_id"] = runtime["run_id"]
        result["source_revision"] = runtime["source_revision"]
        result["source_branch"] = runtime["branch"]
        result["source_dirty"] = runtime["dirty"]
        prompt = runtime["prompt"] + (
            "\n\n=== HOST-VERIFIED SOURCE CONTEXT ===\n"
            "The active code root is the current working directory of this OpenCode run.\n"
            "Source commit: " + runtime["source_revision"] + "\n"
            "Branch: " + runtime["branch"] + "\n"
            "Tracked working tree dirty: " + str(runtime["dirty"]) + "\n"
            "Job Run ID: " + runtime["run_id"] + "\n"
            "Do NOT use files outside the approved source tree except the installed "
            "skill policies, and their canonical private result/ledger roots.\n"
        )
        output = root / "output" / "nr_tx_knowledge_research" / "runs" / runtime["run_id"]
        output.mkdir(parents=True, exist_ok=False)
        result["local_output"] = str(output)
        env = dict(os.environ)
        env["OPENCODE_CONFIG_CONTENT"] = json.dumps({
            "permission": opencode_permissions(), "plugin": [],
            "agent": {"build": {"permission": opencode_permissions()}}
        }, ensure_ascii=False)
        env["OPENCODE_AUTO_SHARE"] = "false"
        env["OPENCODE_DISABLE_AUTOUPDATE"] = "true"
        env["OPENCODE_DISABLE_TERMINAL_TITLE"] = "true"
        transcript = output / "nr_tx_research_transcript.txt"
        with transcript.open("wb") as handle:
            try:
                process = subprocess.run(
                    [runtime["exe"], "run", "--dir", str(runtime["source"]),
                     "--agent", "build", prompt],
                    stdin=subprocess.DEVNULL, stdout=handle, stderr=subprocess.STDOUT,
                    env=env, timeout=10800, check=False)
                result["opencode_returncode"] = process.returncode
            except subprocess.TimeoutExpired:
                result["opencode_returncode"] = 124
                raise RuntimeError("OPENCODE_TIMEOUT")
        size = transcript.stat().st_size
        result["transcript_sha256"] = hashlib.sha256(transcript.read_bytes()[:2000000]).hexdigest()
        result["transcript_bytes"] = size
        # Actual artifacts remain on host. CLI completion is not MSC or
        # Knowledge publication evidence; never fabricate full completion.
        if not size:
            raise RuntimeError("OPENCODE_EMPTY_TRANSCRIPT")
        if process.returncode:
            raise RuntimeError("OPENCODE_NONZERO_EXIT")
        result["status"] = "ANALYSIS_PARTIAL"
        result["reason_codes"] = ["INHOUSE_ARTIFACT_READBACK_REQUIRED"]
        result["analysis_status"] = "MODEL_RUN_COMPLETED_ARTIFACT_UNVERIFIED"
        result["msc_status"] = "REQUIRES_DOC_CONVERTER_RECEIPT"
        result["knowledge_updater_status"] = "REQUIRES_REGISTERED_ACTION_RECEIPT"
    except (RuntimeError, OSError, UnicodeError) as exc:
        result["reason_codes"] = [str(exc)[:95] if isinstance(exc, RuntimeError)
                                  else type(exc).__name__]
    finally:
        result["completed_at"] = _now()
        _atomic_json(root / RESULT, result)
    print(json.dumps({
        "job_id": JOB_ID, "job_run_id": result.get("job_run_id"),
        "status": result["status"], "reason_codes": result["reason_codes"],
        "source_write": False, "group_write": False,
        "external_export": False,
    }, ensure_ascii=False))
    # Job Core collects the semantic latest_result even when the host blocks.
    return result

if __name__ == "__main__":
    main_run()
