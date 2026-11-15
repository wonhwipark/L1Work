#!/usr/bin/env python3
"""Build a user-approved read-only NR Tx debug delivery ZIP from immutable baseline.

Package contains a single active Job. No site code or proprietary data is bundled.
Actual host execution and Knowledge Updater provider remain separately observable.
"""
from __future__ import annotations
import copy
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

OLD = "0.4.36"
NEW = "0.4.38"
BASE_FILE = "job-list_v0_4_36_1112.zip"
OUT_FILE = "job-list_v0_4_38_1115.zip"
EXPECTED_GIT_BLOB = "4357594be4cdae26a4fd19788fb3a35d7de3b5d5"
EXPECTED_SIZE = 1563658
JOB_ID = "JOB-20261115-NR-L1TX-INIT-RACH-EXEC-01"
PROFILE = "nr-l1tx-init-rach-analysis-linux"
REQUEST = "requests/one-shot-jobs.json"

def text_json(data: dict) -> bytes:
    return (json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf8")

def path_ok(name: str) -> None:
    p = Path(name)
    if name.startswith("/") or ".." in p.parts or "\\" in name or "\0" in name:
        raise ValueError("ZIP_PATH_TRAVERSAL")

def replace_one(src: bytes, old: bytes, new: bytes, label: str) -> bytes:
    if src.count(old) != 1:
        raise ValueError("PATCH_ANCHOR_AMBIGUOUS_" + label)
    return src.replace(old, new, 1)

def build(base: Path, tool_dir: Path, out_dir: Path) -> Path:
    binary = base.read_bytes()
    sha = hashlib.sha1(b"blob " + str(len(binary)).encode("ascii") + b"\0" + binary).hexdigest()
    if sha != EXPECTED_GIT_BLOB or len(binary) != EXPECTED_SIZE:
        raise ValueError("BASELINE_ZIP_BYTES_MISMATCH")
    with zipfile.ZipFile(base) as oldzip:
        if oldzip.testzip() is not None:
            raise ValueError("BASELINE_BAD_CRC")
        infos = oldzip.infolist()
        old_root = "job-list_v0_4_36/"
        new_root = "job-list_v0_4_38/"
        if not all(i.filename.startswith(old_root) for i in infos):
            raise ValueError("BASELINE_ROOT_INCONSISTENT")
        found = set()
        data = {}
        for info in infos:
            path_ok(info.filename)
            if info.filename in found:
                raise ValueError("BASELINE_DUPLICATE_PATH")
            found.add(info.filename)
            name = info.filename[len(old_root):]
            data[name] = oldzip.read(info.filename) if not info.is_dir() else b""

    assert data["VERSION"].decode("utf8").strip() == OLD
    old_req = json.loads(data["requests/one-shot-jobs.json"])
    assert old_req["schema_version"] == 1
    assert len(old_req["jobs"]) == 1
    assert old_req["jobs"][0]["job_id"] == "JOB-20261112-NR-L1TX-KNOWLEDGE-MSC-EXEC-01"
    data["VERSION"] = (NEW + "\n").encode()
    release = json.loads(data[".skill-release.json"])
    assert release["name"] == "job-list" and release["version"] == OLD
    release["version"] = NEW
    release["revision"] = int(release["revision"]) + 1
    release["built_at"] = "2026-11-15"
    release["channel"] = "stable"
    data[".skill-release.json"] = text_json(release)
    lifecycle = json.loads(data["lifecycle.json"])
    assert lifecycle["version"] == OLD
    lifecycle["version"] = NEW
    lifecycle["notes"].insert(0, "v0.4.38 approved read-only debug delivery for NR L1 Tx Init RACH Code Analyzer; host G0 and Claude independent review are post-release verification gates, not implied PASS. No old one-shot requeue, source or canonical knowledge writes.")
    data["lifecycle.json"] = text_json(lifecycle)

    skill = data["SKILL.md"]
    skill = replace_one(skill, b"version: 0.4.36", b"version: 0.4.38", "SKILL_FRONTMATTER")
    intro = b"""# job-list v0.4.38 -- APPROVED READ-ONLY DEBUG RELEASE\n\nNew unique NR L1 Tx Init RACH one-shot; use installed code-analyzer via approved non-mutating action. No source/Knowledge modification or old Job reactivation. Independent review and host E2E pending.\n\n"""
    data["SKILL.md"] = skill.replace(b"# job-list v0.4.36", intro + b"# Historical v0.4.36", 1)
    pre = """# job-list v0.4.38 — read-only NR Init RACH debug release\n\nNew active request: JOB-20261115-NR-L1TX-INIT-RACH-EXEC-01. User-approved debug delivery with pre-release safety gates; independent review and host G0/activation are post-release verification, not assumed PASS. Legacy 0.4.36 Job history retained but cannot be re-queued.\n\n"""
    data["README.md"] = pre.encode("utf8") + data["README.md"]
    for f in ("skillsilent/manifest.json", "skillsilent/contract.json"):
        d = json.loads(data[f])
        assert d.get("skill_version") == OLD
        d["skill_version"] = NEW
        data[f] = text_json(d)
    core = data["scripts/job_core.py"]
    core = replace_one(core, b'VERSION = "0.4.36"', b'VERSION = "0.4.38"', "CORE_VERSION")
    anchor = b"BUILTIN_SAFE_PROFILES: dict[str, dict[str, Any]] = {\n"
    profile = (
        b'    # v0.4.38 new bounded Linux NR Tx Init RACH read-only job.\n'
        b'    "nr-l1tx-init-rach-analysis-linux": {\n'
        b'        "enabled": True, "skill": "job-list",\n'
        b'        "entrypoint": "scripts/nrtx_init_rach_linux_job.py",\n'
        b'        "args": [], "timeout_sec": 3600, "retry": 0,\n'
        b'        "required_outputs": ["output/nr_tx_init_rach/latest_result.json"],\n'
        b'        "semantic_result_path": "output/nr_tx_init_rach/latest_result.json",\n'
        b'        "semantic_result_required": True, "env": {}, "parameters": {},\n'
        b'        "supersede_policy": {"enabled": False},\n'
        b'    },\n'
    )
    core = replace_one(core, anchor, anchor + profile, "PROFILE_INSERT")
    data["scripts/job_core.py"] = core
    # Update only release-identity/active-request expectations; retain legacy tests.
    for tn in ("tests/test_v0434_dependency_gate.py", "tests/test_v0431_knowledge_input_stage.py"):
        body = data[tn].replace(b"0.4.36", b"0.4.38")
        body = body.replace(b"JOB-20261112-NR-L1TX-KNOWLEDGE-MSC-EXEC-01",
                            b"JOB-20261115-NR-L1TX-INIT-RACH-EXEC-01")
        data[tn] = body
    tn = "tests/test_v0436_nrtx_active.py"
    body = data[tn].replace(b"0.4.36", b"0.4.38")
    begin = body.index(b"def test_version_and_active_request():")
    end = body.index(b"def test_no_old_job_requeue():", begin)
    body = body[:begin] + b'''def test_v0436_retired_request_not_active():
    active = json.loads((ROOT / "requests/one-shot-jobs.json").read_text())
    assert all(j["job_id"] != worker.JOB_ID for j in active["jobs"])

''' + body[end:]
    data[tn] = body
    data["tests/test_v0438_init_rach_active.py"] = (
        tool_dir / "test_v0438_init_rach_active.py").read_bytes()

    for f in ("install.py",):
        if f in data:
            # Installer may include the exact current release label; never mass-
            # rewrite historical notes or bundled tests/fixtures.
            data[f] = data[f].replace(b'0.4.36', b'0.4.38')

    data[REQUEST] = text_json({
        "schema_version": 1,
        "jobs": [{
            "job_id": JOB_ID, "profile": PROFILE, "platform": "linux",
            "priority": 65, "expires_at": "2026-12-15T23:59:59+09:00",
            "params": {}
        }]
    })
    data["scripts/nrtx_init_rach_linux_job.py"] = (tool_dir / "nrtx_init_rach_linux_job.py").read_bytes()
    data["references/NR_TX_INIT_RACH_CODE_ANALYSIS_v0438.md"] = (
        tool_dir / "NR_TX_INIT_RACH_CODE_ANALYSIS_v0438.md").read_bytes()

    # Detect the original sha256sum format; use the canonical two-space style.
    old_manifest = data.get("PACKAGE_CONTENTS.sha256", b"").decode("utf8")
    records = [x for x in old_manifest.splitlines() if x.strip() and not x.startswith("#")]
    if not records or not re.fullmatch(r"[0-9a-f]{64}\s{1,2}[*]?\S.*", records[0]):
        raise ValueError("UNKNOWN_PACKAGE_SHA_MANIFEST_FORMAT")
    paths = sorted(x for x in data if x and not x.endswith("/") and x != "PACKAGE_CONTENTS.sha256")
    data["PACKAGE_CONTENTS.sha256"] = ("".join(
        hashlib.sha256(data[k]).hexdigest() + "  " + k + "\n" for k in paths)).encode("utf8")
    dest = out_dir / OUT_FILE
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w") as z:
        for info in infos:
            rel = info.filename[len(old_root):]
            newinfo = copy.copy(info)
            newinfo.filename = new_root + rel
            z.writestr(newinfo, data[rel])
        added = sorted(set(data) - {i.filename[len(old_root):] for i in infos})
        for rel in added:
            newinfo = zipfile.ZipInfo(new_root + rel, (2026, 11, 15, 1, 0, 0))
            newinfo.compress_type = zipfile.ZIP_DEFLATED
            newinfo.external_attr = 0o100644 << 16
            z.writestr(newinfo, data[rel])
    verify(dest, data, old_root, new_root)
    return dest

def verify(zippath: Path, data: dict, oldroot: str, newroot: str) -> None:
    with zipfile.ZipFile(zippath) as z:
        assert z.testzip() is None
        names = z.namelist()
        assert len(names) == len(set(names))
        assert all(x.startswith(newroot) for x in names)
        for n in names:
            path_ok(n)
            p = n[len(newroot):]
            if not n.endswith("/"):
                assert z.read(n) == data[p], p
        assert len(json.loads(z.read(newroot + "requests/one-shot-jobs.json"))["jobs"]) == 1
        assert json.loads(z.read(newroot + REQUEST))["jobs"][0]["job_id"] == JOB_ID
        assert z.read(newroot + "VERSION") == (NEW + "\n").encode()
        assert z.read(newroot + "scripts/nrtx_init_rach_linux_job.py").count(b"JOB-20261115") == 1
        # Every sha256sum path must be the exact package payload, not fabricated.
        manifest = z.read(newroot + "PACKAGE_CONTENTS.sha256").decode("utf8").splitlines()
        for rec in manifest:
            sha, rel = rec.split("  ", 1)
            assert hashlib.sha256(z.read(newroot + rel)).hexdigest() == sha, rel
        assert len(manifest) == sum(1 for p in data if p and not p.endswith("/") and p != "PACKAGE_CONTENTS.sha256")
        assert b"github.com/wonhwipark/" not in z.read(newroot + "references/NR_TX_INIT_RACH_CODE_ANALYSIS_v0438.md")
    print("ZIP_CRC=PASS", "MANIFEST=PASS", "ACTIVE_JOBS=1",
          "VERSION=" + NEW, "PACKAGE_BYTES=" + str(zippath.stat().st_size),
          "PACKAGE_SHA256=" + hashlib.sha256(zippath.read_bytes()).hexdigest(), flush=True)

def main() -> None:
    repo = Path(__file__).resolve().parent
    base = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    target = build(base, repo, out)
    print("APPROVED_READ_ONLY_DEBUG_ZIP_BUILT_HOST_UNVERIFIED", target, flush=True)

if __name__ == "__main__":
    main()
