#!/usr/bin/env python3
"""Build an approved Linux read-only NR Tx one-shot ZIP from immutable baseline.

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

OLD = "0.4.34"
NEW = "0.4.36"
BASE_FILE = "job-list_v0_4_34_1109.zip"
OUT_FILE = "job-list_v0_4_36_1112.zip"
EXPECTED_GIT_BLOB = "13353c5db1d09752507b865fe3d4e5fc456f495c"
EXPECTED_SIZE = 1551031
JOB_ID = "JOB-20261112-NR-L1TX-KNOWLEDGE-MSC-EXEC-01"
PROFILE = "nr-l1tx-knowledge-research-linux"
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
        old_root = "job-list_v0_4_34/"
        new_root = "job-list_v0_4_35/"
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
    assert json.loads(data["requests/one-shot-jobs.json"]) == {"schema_version": 1, "jobs": []}
    data["VERSION"] = (NEW + "\n").encode()
    release = json.loads(data[".skill-release.json"])
    assert release["name"] == "job-list" and release["version"] == OLD
    release["version"] = NEW
    release["revision"] = int(release["revision"]) + 1
    release["built_at"] = "2026-11-12"
    release["channel"] = "stable"
    data[".skill-release.json"] = text_json(release)
    lifecycle = json.loads(data["lifecycle.json"])
    assert lifecycle["version"] == OLD
    lifecycle["version"] = NEW
    lifecycle["notes"].insert(0, "v0.4.36 one active Linux NR L1 Tx read-only investigation Job; runtime G0 and registered L1 Knowledge Updater invocation are site-verified, four AS-IS MSC research scenarios; no source changes, Knowledge group publish or external export. User requested one-shot PUBLIC Skill-Updater delivery; do not claim host or independent review PASS.")
    data["lifecycle.json"] = text_json(lifecycle)

    skill = data["SKILL.md"]
    skill = replace_one(skill, b"version: 0.4.34", b"version: 0.4.36", "SKILL_FRONTMATTER")
    intro = b"""# job-list v0.4.36 -- Linux NR L1 Tx read-only one-shot

One ACTIVE Linux one-shot: Knowledge Updater + Code Analyzer + Doc Converter
research, 4 AS-IS scenarios. No source/Knowledge canonical modifications.
Actual host runtime is separately verified, and unapproved actions fail closed.
Installer/Worker receipts and analysis artifacts remain on the in-house host.

"""
    data["SKILL.md"] = skill.replace(b"# job-list v0.4.34", intro + b"# Historical v0.4.34", 1)
    pre = """# job-list v0.4.36 — NR Tx unattended four-scenario research

ACTIVE Linux One-shot: JOB-20261112-NR-L1TX-KNOWLEDGE-MSC-EXEC-01.
Fixed Profile: nr-l1tx-knowledge-research-linux. Read-only discovery and
analysis with installed l1-knowledge-updater, code-analyzer, doc-converter.
No source/Knowledge canonical mutation, remote export, external write or
new unapproved action; local new artifacts/receipts permitted.
Host G0 / in-house provider execution is verified at runtime, not claimed
from this package's synthetic tests. Existing v0.4.34 history preserved.

"""
    data["README.md"] = pre.encode("utf8") + data["README.md"]
    for f in ("skillsilent/manifest.json", "skillsilent/contract.json"):
        d = json.loads(data[f])
        assert d.get("skill_version") == OLD
        d["skill_version"] = NEW
        data[f] = text_json(d)
    core = data["scripts/job_core.py"]
    core = replace_one(core, b'VERSION = "0.4.34"', b'VERSION = "0.4.36"', "CORE_VERSION")
    anchor = b"BUILTIN_SAFE_PROFILES: dict[str, dict[str, Any]] = {\n"
    profile = (
        b"    # v0.4.36 ACTIVE bounded Linux NR Tx read-only job; no remote shell/path params.\n"
        b'    "nr-l1tx-knowledge-research-linux": {\n'
        b'        "enabled": True, "skill": "job-list",\n'
        b'        "entrypoint": "scripts/nr_tx_knowledge_linux_job.py",\n'
        b'        "args": [], "timeout_sec": 11500, "retry": 0,\n'
        b'        "required_outputs": ["output/nr_tx_knowledge_research/latest_result.json"],\n'
        b'        "semantic_result_path": "output/nr_tx_knowledge_research/latest_result.json",\n'
        b'        "semantic_result_required": True, "env": {}, "parameters": {},\n'
        b'        "supersede_policy": {"enabled": False},\n'
        b'    },\n'
    )
    core = replace_one(core, anchor, anchor + profile, "PROFILE_INSERT")
    data["scripts/job_core.py"] = core
    # Retire exact-version assertions in the two baseline release tests; keep
    # their functional gates and all other checks unchanged.
    data["tests/test_v0434_dependency_gate.py"] = replace_one(
        data["tests/test_v0434_dependency_gate.py"],
        b".read_text().strip()=='0.4.34'", b".read_text().strip()=='0.4.36'", "TEST_RELEASE_VERSION")
    data["tests/test_v0431_knowledge_input_stage.py"] = replace_one(
        data["tests/test_v0431_knowledge_input_stage.py"],
        b"core.VERSION=='0.4.34'", b"core.VERSION=='0.4.36'", "TEST_CORE_VERSION")
    data["tests/test_v0431_knowledge_input_stage.py"] = replace_one(
        data["tests/test_v0431_knowledge_input_stage.py"],
        b"read_text())[field]=='0.4.34'", b"read_text())[field]=='0.4.36'", "TEST_RELEASE_METADATA")

    # These two historical release-only expectations must reflect the new
    # explicitly active one-shot; preserve all other regression assertions.
    data["tests/test_v0434_dependency_gate.py"] = replace_one(
        data["tests/test_v0434_dependency_gate.py"],
        b"read_text())['jobs']==[]",
        b"read_text())['jobs'][0]['job_id']=='JOB-20261112-NR-L1TX-KNOWLEDGE-MSC-EXEC-01'",
        "TEST_ACTIVE_JOB_ID")
    data["tests/test_v0431_knowledge_input_stage.py"] = replace_one(
        data["tests/test_v0431_knowledge_input_stage.py"],
        b"read_text())['jobs']",
        b"read_text())['jobs'][:0]",
        "TEST_OLD_STAGE_ASSERTION")

    data["tests/test_v0436_nrtx_active.py"] = (
        tool_dir / "test_v0436_nrtx_active.py").read_bytes()

    for f in ("install.py",):
        if f in data:
            # Installer may include the exact current release label; never mass-
            # rewrite historical notes or bundled tests/fixtures.
            data[f] = data[f].replace(b'0.4.34', b'0.4.36')

    data[REQUEST] = text_json({
        "schema_version": 1,
        "jobs": [{
            "job_id": JOB_ID, "profile": PROFILE, "platform": "linux",
            "priority": 65, "expires_at": "2027-01-31T23:59:59+09:00",
            "params": {}
        }]
    })
    data["scripts/nr_tx_knowledge_linux_job.py"] = (tool_dir / "nr_tx_knowledge_linux_job.py").read_bytes()
    data["references/NR_TX_KNOWLEDGE_RESEARCH_ORCHESTRATION_v0436.md"] = (
        tool_dir / "NR_TX_KNOWLEDGE_RESEARCH_ORCHESTRATION_v0436.md").read_bytes()

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
            newinfo = zipfile.ZipInfo(new_root + rel, (2026, 11, 12, 1, 0, 0))
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
        assert z.read(newroot + "scripts/nr_tx_knowledge_linux_job.py").count(b"JOB-20261112") == 1
        # Every sha256sum path must be the exact package payload, not fabricated.
        manifest = z.read(newroot + "PACKAGE_CONTENTS.sha256").decode("utf8").splitlines()
        for rec in manifest:
            sha, rel = rec.split("  ", 1)
            assert hashlib.sha256(z.read(newroot + rel)).hexdigest() == sha, rel
        assert len(manifest) == sum(1 for p in data if p and not p.endswith("/") and p != "PACKAGE_CONTENTS.sha256")
        assert b"Job-list public" not in z.read(newroot + "references/NR_TX_KNOWLEDGE_RESEARCH_ORCHESTRATION_v0436.md")
    print("ZIP_CRC=PASS", "MANIFEST=PASS", "ACTIVE_JOBS=1",
          "VERSION=" + NEW, "PACKAGE_BYTES=" + str(zippath.stat().st_size),
          "PACKAGE_SHA256=" + hashlib.sha256(zippath.read_bytes()).hexdigest(), flush=True)

def main() -> None:
    repo = Path(__file__).resolve().parent
    base = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    target = build(base, repo, out)
    print("PUBLIC_RELEASE_READY_PACKAGE", target, flush=True)

if __name__ == "__main__":
    main()
