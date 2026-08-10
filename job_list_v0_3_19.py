#!/usr/bin/env python3
"""
job-list v0.3.19 - Private-14 Implementation Gate / Activation Plan / POST_CHECK

Purpose
-------
This is a deterministic PRE-ACTIVATION runner for the Private Skill migration.

It performs, in order:
  1) strict Private-14 scope guard
  2) 14-skill IMPLEMENTATION_REPAIR_COMPLETE gate
  3) activation-plan regeneration
  4) exact-byte SHA256 freeze
  5) activation POST_CHECK

It NEVER performs Activation APPLY.

Safety model
------------
- Only the 14 explicitly listed Private Skills are inspected.
- Group/common/shared skills are never enumerated, copied, repaired, reconciled,
  activated, registered, unregistered, or modified.
- ~/.claude/skills/<private-skill>/ is READ ONLY.
- ~/l1sw-skills/private-skills/<private-skill>/ is READ ONLY.
- ~/.claude/main/<private-skill>/ is READ ONLY.
- The only writable location is ~/.claude/main/job-list/output/...
- No delete/move/rename/cleanup/GitHub write/Knowledge migration.
- Fail closed when repair metadata, managed asset closure, execution_root, or
  scope is ambiguous.

Repair verification intentionally uses the explicit asset list recorded by
.implementation-version.json. Target-only unmanaged files are ignored/kept.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

VERSION = "0.3.19"
RESULT_PASS = 1
RESULT_FAILED_SAFE = 5
MAX_TEXT_SCAN_BYTES = 2 * 1024 * 1024

PRIVATE_SKILLS: dict[str, str] = {
    "code-analyzer": "0.13.19",
    "code-fix": "0.4.5",
    "doc-converter": "0.2.0",
    "hld-code-compare": "0.10.4",
    "hld-code-implement": "0.5.9",
    "hld-composer": "0.4.13",
    "issue-analyzer": "0.11.5",
    "issue-fix-implement": "0.3.1",
    "l1_fla": "0.2.0",
    "l1-sam-fixer": "0.2.14",
    "p4-code-owner": "0.6.0",
    "p4-fix-kb": "0.2.2",
    "slte-knowledge-manager": "0.4.5",
    "slte-port-impact-analyzer": "0.8.23",
}
PRIVATE_SET = frozenset(PRIVATE_SKILLS)

# Preserve the established activation wave grouping.
WAVE3_SKILLS = frozenset(
    {"issue-analyzer", "code-analyzer", "code-fix", "issue-fix-implement"}
)
WAVE4_SKILLS = frozenset(
    {"slte-knowledge-manager", "slte-port-impact-analyzer"}
)

RUNTIME_TEXT_SUFFIXES = frozenset(
    {".py", ".ps1", ".cmd", ".bat", ".sh", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".md"}
)

CONTROL_FILES = (
    "skillsilent/manifest.json",
    ".skill-main.json",
    "skillsilent/contract.json",
    "skillsilent/policy.json",
)

EXECUTION_ROOT_KEYS = frozenset({"execution_root", "executionroot"})


class SafeStop(RuntimeError):
    pass


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def stamp() -> str:
    return dt.datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".tmp.{os.getpid()}")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    os.replace(tmp, path)


def atomic_json(path: Path, payload: Any) -> None:
    atomic_write(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SafeStop(f"missing JSON: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SafeStop(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SafeStop(f"JSON root must be object: {path}")
    return data


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def assert_exact_private_path(path: Path, root: Path, skill: str) -> None:
    if skill not in PRIVATE_SET:
        raise SafeStop(f"SCOPE_VIOLATION: unlisted skill: {skill}")
    expected = (root / skill).resolve()
    if path.resolve() != expected:
        raise SafeStop(
            f"SCOPE_VIOLATION: non-canonical private path: skill={skill} "
            f"path={path} expected={expected}"
        )


def assert_output_scope(path: Path, main_root: Path) -> None:
    allowed = (main_root / "job-list" / "output").resolve()
    if not is_relative_to(path.resolve(), allowed):
        raise SafeStop(f"SCOPE_VIOLATION: output path outside job-list output: {path}")


def tree_stat_fingerprint(root: Path) -> dict[str, Any]:
    """Read-only metadata fingerprint to prove this run did not change a main tree."""
    if not root.exists():
        return {"exists": False, "digest": None, "entries": 0}
    if root.is_symlink():
        return {"exists": True, "symlink": True, "digest": None, "entries": 0}

    h = hashlib.sha256()
    entries = 0
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        dirs.sort()
        files.sort()

        # Record symlink dirs but do not follow them.
        kept_dirs: list[str] = []
        for name in dirs:
            p = current_path / name
            rel = p.relative_to(root).as_posix()
            if p.is_symlink():
                target = os.readlink(p)
                h.update(f"L|{rel}|{target}\n".encode("utf-8", errors="surrogatepass"))
                entries += 1
            else:
                kept_dirs.append(name)
        dirs[:] = kept_dirs

        for name in files:
            p = current_path / name
            rel = p.relative_to(root).as_posix()
            try:
                st = p.lstat()
            except OSError as exc:
                h.update(f"E|{rel}|{exc}\n".encode("utf-8", errors="replace"))
                entries += 1
                continue
            if p.is_symlink():
                target = os.readlink(p)
                h.update(f"L|{rel}|{target}\n".encode("utf-8", errors="surrogatepass"))
            else:
                h.update(
                    f"F|{rel}|{st.st_size}|{st.st_mtime_ns}\n".encode(
                        "utf-8", errors="surrogatepass"
                    )
                )
            entries += 1
    return {"exists": True, "symlink": False, "digest": h.hexdigest(), "entries": entries}


def managed_asset_manifest(root: Path, asset: str) -> dict[str, Any]:
    """
    Manifest only files that belong to one explicitly managed implementation asset.
    Symlinks are blockers. Target extras are handled separately and are not failures.
    """
    asset = asset.replace("\\", "/").strip("/")
    if not asset or asset.startswith("../") or "/../" in f"/{asset}/":
        raise SafeStop(f"unsafe asset path: {asset!r}")

    base = root / Path(asset)
    if not base.exists():
        raise SafeStop(f"managed asset missing: {base}")
    if base.is_symlink():
        raise SafeStop(f"managed asset is symlink: {base}")

    files: dict[str, dict[str, Any]] = {}
    symlinks: list[str] = []

    if base.is_file():
        rel = Path(asset).as_posix()
        files[rel] = {"size": base.stat().st_size, "sha256": sha256_file(base)}
        return {"files": files, "symlinks": symlinks}

    if not base.is_dir():
        raise SafeStop(f"managed asset is not regular file/directory: {base}")

    for current, dirs, names in os.walk(base, topdown=True, followlinks=False):
        current_path = Path(current)
        dirs.sort()
        names.sort()

        kept_dirs: list[str] = []
        for name in dirs:
            p = current_path / name
            rel = p.relative_to(root).as_posix()
            if p.is_symlink():
                symlinks.append(rel)
            else:
                kept_dirs.append(name)
        dirs[:] = kept_dirs

        for name in names:
            p = current_path / name
            rel = p.relative_to(root).as_posix()
            if p.is_symlink():
                symlinks.append(rel)
            elif p.is_file():
                files[rel] = {"size": p.stat().st_size, "sha256": sha256_file(p)}
            else:
                raise SafeStop(f"non-regular managed file: {p}")

    if symlinks:
        raise SafeStop(f"symlink inside managed asset {asset}: {symlinks[:10]}")
    return {"files": files, "symlinks": symlinks}


def compare_managed_assets(
    package_root: Path, target_root: Path, assets: list[str]
) -> dict[str, Any]:
    """
    Require every package-managed file to exist in target with the same hash.
    Target-only files are intentionally preserved and do not fail the gate.
    """
    missing: list[str] = []
    changed: list[str] = []
    source_files = 0
    target_extra_count = 0
    per_asset: list[dict[str, Any]] = []

    for asset in assets:
        src = managed_asset_manifest(package_root, asset)
        dst = managed_asset_manifest(target_root, asset)
        src_files = src["files"]
        dst_files = dst["files"]
        source_files += len(src_files)

        a_missing = sorted(set(src_files) - set(dst_files))
        a_changed = sorted(
            rel for rel in set(src_files) & set(dst_files)
            if src_files[rel] != dst_files[rel]
        )
        extras = sorted(set(dst_files) - set(src_files))
        missing.extend(a_missing)
        changed.extend(a_changed)
        target_extra_count += len(extras)
        per_asset.append(
            {
                "asset": asset,
                "package_files": len(src_files),
                "target_files": len(dst_files),
                "missing": a_missing,
                "changed": a_changed,
                "target_only_unmanaged_kept": extras,
            }
        )

    return {
        "ok": not missing and not changed,
        "source_files": source_files,
        "missing": missing,
        "changed": changed,
        "target_only_unmanaged_count": target_extra_count,
        "assets": per_asset,
    }


def collect_versions(package_root: Path) -> dict[str, Any]:
    observations: list[dict[str, str]] = []

    manifest = package_root / "skillsilent" / "manifest.json"
    if manifest.is_file() and not manifest.is_symlink():
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data.get("version") is not None:
                observations.append(
                    {"source": "skillsilent/manifest.json", "version": str(data["version"])}
                )
        except Exception:
            pass

    skill_md = package_root / "SKILL.md"
    if skill_md.is_file() and not skill_md.is_symlink():
        text = skill_md.read_text(encoding="utf-8", errors="ignore")[:32768]
        m = re.search(r"(?im)^\s*version\s*:\s*[\"']?([^\"'\s]+)", text)
        if m:
            observations.append({"source": "SKILL.md", "version": m.group(1)})

    for candidate in ("VERSION", "VERSION.md"):
        p = package_root / candidate
        if p.is_file() and not p.is_symlink():
            text = p.read_text(encoding="utf-8", errors="ignore")[:4096]
            m = re.search(r"\b(?:v)?(\d+\.\d+\.\d+)\b", text)
            if m:
                observations.append({"source": candidate, "version": m.group(1)})

    unique = sorted({x["version"].lstrip("v") for x in observations})
    return {"observations": observations, "unique_versions": unique}


def recursive_execution_roots(obj: Any, source: str, out: list[dict[str, str]]) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = re.sub(r"[^A-Za-z0-9]", "", str(k)).lower()
            if key in EXECUTION_ROOT_KEYS and isinstance(v, str) and v.strip():
                out.append({"source": source, "value": v.strip()})
            recursive_execution_roots(v, source, out)
    elif isinstance(obj, list):
        for v in obj:
            recursive_execution_roots(v, source, out)


def detect_execution_root(package_root: Path) -> dict[str, Any]:
    found: list[dict[str, str]] = []
    parse_errors: list[str] = []
    control_seen: list[str] = []

    for rel in CONTROL_FILES:
        p = package_root / rel
        if not p.exists():
            continue
        if p.is_symlink() or not p.is_file():
            parse_errors.append(f"{rel}: not regular file")
            continue
        control_seen.append(rel)
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:
            parse_errors.append(f"{rel}: {exc}")
            continue
        recursive_execution_roots(data, rel, found)

    distinct = sorted({x["value"] for x in found})
    return {
        "control_files_seen": control_seen,
        "parse_errors": parse_errors,
        "observations": found,
        "distinct_values": distinct,
        "ok": len(distinct) == 1 and not parse_errors,
        "value": distinct[0] if len(distinct) == 1 else None,
        "source": next((x["source"] for x in found if x["value"] == distinct[0]), None)
        if len(distinct) == 1
        else None,
    }


def expand_percent_vars(value: str) -> str:
    return re.sub(r"%([^%]+)%", lambda m: os.environ.get(m.group(1), m.group(0)), value)


def resolve_runtime_path(value: str, package_root: Path) -> Path:
    text = expand_percent_vars(value)
    text = os.path.expandvars(os.path.expanduser(text))
    if re.search(r"<[^>]+>", text):
        raise SafeStop(f"unresolved placeholder in execution_root: {value}")
    p = Path(text)
    if not p.is_absolute():
        p = package_root / p
    return p.resolve()


def scan_private_dependencies(target_root: Path, self_skill: str) -> list[str]:
    """
    Inspect only files inside this Private Skill target.
    Never opens another skill's directory.
    """
    found: set[str] = set()
    for current, dirs, files in os.walk(target_root, topdown=True, followlinks=False):
        current_path = Path(current)
        dirs.sort()
        files.sort()

        # Never follow symlink directories.
        dirs[:] = [d for d in dirs if not (current_path / d).is_symlink()]

        for name in files:
            p = current_path / name
            if p.is_symlink() or p.suffix.lower() not in RUNTIME_TEXT_SUFFIXES:
                continue
            try:
                if p.stat().st_size > MAX_TEXT_SCAN_BYTES:
                    continue
                text = p.read_text(encoding="utf-8", errors="ignore").lower()
            except OSError:
                continue

            for other in PRIVATE_SET:
                if other == self_skill:
                    continue
                o = re.escape(other.lower())
                patterns = (
                    rf"skillsilent\s+run\s+{o}(?:\s|$)",
                    rf"\.claude[/\\]+skills[/\\]+{o}(?:[/\\]|\b)",
                    rf"private-skills[/\\]+{o}(?:[/\\]|\b)",
                )
                if any(re.search(pattern, text) for pattern in patterns):
                    found.add(other)
    return sorted(found)


def assign_wave(skill: str, deps: list[str]) -> int:
    if skill in WAVE4_SKILLS:
        return 4
    if skill in WAVE3_SKILLS:
        return 3
    if deps:
        return 2
    return 1


def probe_skillsilent(skip: bool = False) -> dict[str, Any]:
    if skip:
        return {"ok": True, "skipped": True, "reason": "explicit test override"}

    candidates: list[str] = []
    explicit = os.environ.get("SKILLSILENT_CMD")
    if explicit:
        candidates.append(explicit)
    for name in ("skillsilent", "skillsilent.cmd", "skillsilent.exe"):
        found = shutil.which(name)
        if found and found not in candidates:
            candidates.append(found)

    # Read-only command candidates only. No setup/install/reconcile.
    errors: list[str] = []
    for cmd in candidates:
        for argv in ([cmd, "--version"], [cmd, "version"]):
            try:
                cp = subprocess.run(
                    argv,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    timeout=20,
                    shell=False,
                )
            except Exception as exc:
                errors.append(f"{argv!r}: {exc}")
                continue
            output = (cp.stdout or "").strip()[-2000:]
            if cp.returncode == 0:
                return {
                    "ok": True,
                    "skipped": False,
                    "command": argv,
                    "returncode": cp.returncode,
                    "output": output,
                }
            errors.append(f"{argv!r}: rc={cp.returncode}: {output}")

    return {
        "ok": False,
        "skipped": False,
        "errors": errors or ["skillsilent command not found"],
    }


def validate_marker(
    marker: dict[str, Any],
    skill: str,
    expected_version: str,
    package_root: Path,
    target_root: Path,
) -> tuple[list[str], list[str], list[str]]:
    blockers: list[str] = []
    failures: list[str] = []
    warnings: list[str] = []

    if str(marker.get("skill") or "") != skill:
        blockers.append(f"marker skill mismatch: {marker.get('skill')!r}")

    assets_raw = marker.get("assets")
    if not isinstance(assets_raw, list) or not assets_raw:
        blockers.append("marker assets missing/empty")
        assets: list[str] = []
    else:
        assets = []
        for x in assets_raw:
            if not isinstance(x, str) or not x.strip():
                blockers.append(f"invalid marker asset: {x!r}")
                continue
            rel = x.replace("\\", "/").strip("/")
            if rel in {"SKILL.md", "skillsilent"} or rel.startswith("skillsilent/"):
                blockers.append(f"forbidden repair asset in marker: {rel}")
                continue
            if rel not in assets:
                assets.append(rel)

    if marker.get("expected_package_version") not in (None, "", expected_version):
        warnings.append(
            "marker expected_package_version differs: "
            f"expected={expected_version} marker={marker.get('expected_package_version')}"
        )
    if str(marker.get("package_version") or "").lstrip("v") not in ("", "UNKNOWN", expected_version):
        warnings.append(
            f"marker package_version differs: expected={expected_version} "
            f"marker={marker.get('package_version')}"
        )

    source_root = marker.get("source_root")
    if source_root:
        try:
            if Path(os.path.expanduser(os.path.expandvars(str(source_root)))).resolve() != package_root.resolve():
                warnings.append(f"marker source_root differs from canonical package root: {source_root}")
        except Exception:
            warnings.append(f"marker source_root unreadable: {source_root}")

    marker_target = marker.get("target_root")
    if marker_target:
        try:
            if Path(os.path.expanduser(os.path.expandvars(str(marker_target)))).resolve() != target_root.resolve():
                blockers.append(f"marker target_root differs from canonical target: {marker_target}")
        except Exception:
            blockers.append(f"marker target_root unreadable: {marker_target}")

    if blockers:
        return assets, failures, blockers + [f"WARN:{w}" for w in warnings]
    return assets, failures, [f"WARN:{w}" for w in warnings]


def gate_one_skill(
    skill: str,
    expected_version: str,
    skills_root: Path,
    private_root: Path,
    main_root: Path,
) -> dict[str, Any]:
    package_root = (skills_root / skill).resolve()
    target_root = (private_root / skill).resolve()
    persistent_root = (main_root / skill).resolve()

    # Exact scope checks: no broad directory enumeration.
    assert_exact_private_path(package_root, skills_root, skill)
    assert_exact_private_path(target_root, private_root, skill)
    assert_exact_private_path(persistent_root, main_root, skill)

    rec: dict[str, Any] = {
        "skill": skill,
        "expected_package_version": expected_version,
        "package_root": str(package_root),
        "target_root": str(target_root),
        "persistent_root": str(persistent_root),
        "status": "BLOCKED",
        "warnings": [],
        "failures": [],
        "blockers": [],
    }

    if not package_root.is_dir() or package_root.is_symlink():
        rec["blockers"].append("installed package root missing/not-safe-directory")
        return rec

    skill_md = package_root / "SKILL.md"
    if not skill_md.is_file() or skill_md.is_symlink():
        rec["blockers"].append("SKILL.md missing/not-regular")
        return rec
    rec["skill_md_sha256_before"] = sha256_file(skill_md)

    if not target_root.is_dir() or target_root.is_symlink():
        rec["blockers"].append("implementation target missing/not-safe-directory")
        return rec

    marker_path = target_root / ".implementation-version.json"
    if not marker_path.is_file() or marker_path.is_symlink():
        rec["blockers"].append(".implementation-version.json missing/not-regular")
        return rec

    try:
        marker = load_json(marker_path)
    except SafeStop as exc:
        rec["blockers"].append(str(exc))
        return rec

    assets, _, marker_notes = validate_marker(
        marker, skill, expected_version, package_root, target_root
    )
    for note in marker_notes:
        if note.startswith("WARN:"):
            rec["warnings"].append(note[5:])
        else:
            rec["blockers"].append(note)

    rec["implementation_marker"] = {
        "path": str(marker_path),
        "sha256": sha256_file(marker_path),
        "assets": assets,
        "package_version": marker.get("package_version"),
        "expected_package_version": marker.get("expected_package_version"),
        "completed_at": marker.get("completed_at"),
        "engine_version": marker.get("engine_version"),
    }

    rec["package_version_observation"] = collect_versions(package_root)
    observed = rec["package_version_observation"]["unique_versions"]
    if observed and expected_version not in observed:
        rec["warnings"].append(
            f"package version observation differs: expected={expected_version}, observed={observed}"
        )

    if not rec["blockers"]:
        try:
            closure = compare_managed_assets(package_root, target_root, assets)
            rec["implementation_closure"] = closure
            if not closure["ok"]:
                rec["failures"].append("managed implementation closure SHA256 mismatch")
        except SafeStop as exc:
            rec["blockers"].append(str(exc))

    execution = detect_execution_root(package_root)
    rec["execution_root"] = execution
    if not execution["ok"]:
        rec["blockers"].append(
            "execution_root ambiguous/unavailable: "
            f"values={execution['distinct_values']} errors={execution['parse_errors']}"
        )
    else:
        try:
            current_root = resolve_runtime_path(str(execution["value"]), package_root)
            rec["current_execution_root"] = str(current_root)
            rec["current_execution_root_exists"] = current_root.is_dir()
            rec["target_execution_root"] = str(target_root)
            rec["already_active"] = current_root == target_root
            if not current_root.is_dir():
                rec["blockers"].append(
                    f"current execution_root does not exist as directory: {current_root}"
                )
        except SafeStop as exc:
            rec["blockers"].append(str(exc))

    try:
        rec["private_dependencies"] = scan_private_dependencies(target_root, skill)
    except Exception as exc:
        rec["blockers"].append(f"dependency scan failed: {exc}")

    if rec["blockers"]:
        rec["status"] = "BLOCKED"
    elif rec["failures"]:
        rec["status"] = "FAIL"
    elif rec["warnings"]:
        rec["status"] = "WARN"
    else:
        rec["status"] = "PASS"
    return rec


def build_activation_plan(gate_items: list[dict[str, Any]]) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    waves: dict[str, list[str]] = {"1": [], "2": [], "3": [], "4": []}

    for rec in gate_items:
        if rec["skill"] not in PRIVATE_SET:
            raise SafeStop(f"SCOPE_VIOLATION in plan input: {rec['skill']}")
        if rec["status"] not in {"PASS", "WARN"}:
            raise SafeStop(
                f"cannot build activation plan; gate not passed: "
                f"{rec['skill']}={rec['status']}"
            )

        skill = rec["skill"]
        target = rec["target_execution_root"]
        current = rec["current_execution_root"]
        deps = list(rec.get("private_dependencies") or [])
        if any(d not in PRIVATE_SET for d in deps):
            raise SafeStop(f"SCOPE_VIOLATION dependency list: {skill}: {deps}")
        wave = assign_wave(skill, deps)

        apply_action = "SKIP_ALREADY_ACTIVE" if rec.get("already_active") else "SWITCH_EXECUTION_ROOT"
        item = {
            "skill": skill,
            "current_execution_root": current,
            "target_execution_root": target,
            "manifest_path": str(
                Path(rec["package_root"]) / str(rec["execution_root"]["source"])
            ),
            "dependencies": deps,
            "precheck": [
                "target implementation closure SHA256 PASS",
                "manifest parse PASS",
                "current execution_root known",
                "rollback execution_root exists unless already active",
                "persistent path read-only fingerprint unchanged",
            ],
            "validate": [
                "skillsilent manifest validation",
                "execution_root equals target after future APPLY",
                "representative read-only/self-check in future Wave",
            ],
            "dry_run": "required before future reconcile/apply where supported",
            "reconcile": "future Wave only; NOT executed by v0.3.19",
            "functional_validation": [
                "--help or equivalent read-only command",
                "self-check/read-only parse where supported",
                "dependency lookup",
                "output-path dry-run",
            ],
            "rollback_execution_root": current,
            "rollback_ready": bool(rec.get("already_active") or rec.get("current_execution_root_exists")),
            "wave_assignment": wave,
            "apply_action": apply_action,
            "already_active": bool(rec.get("already_active")),
        }
        if not item["rollback_ready"]:
            raise SafeStop(f"rollback route is not ready: {skill}")
        items.append(item)
        waves[str(wave)].append(skill)

    plan = {
        "schema_version": 1,
        "engine": "job-list/private-skill-preactivation",
        "engine_version": VERSION,
        "created_at": now_iso(),
        "scope": "PRIVATE_SKILL_14_ONLY",
        "group_common_skills_policy": "NO_TOUCH",
        "activation_apply_performed": False,
        "knowledge_migration_performed": False,
        "source_delete_move_rename_cleanup_performed": False,
        "items": items,
        "waves": waves,
        "next_step_on_pass": "ACTIVATION_WAVES",
    }
    if {x["skill"] for x in items} != PRIVATE_SET:
        raise SafeStop("SCOPE_VIOLATION: plan target set is not exactly Private-14")
    return plan


def post_check(
    gate_items: list[dict[str, Any]],
    plan_path: Path,
    frozen_sha256: str,
    skills_root: Path,
    private_root: Path,
    main_root: Path,
    main_before: dict[str, dict[str, Any]],
    skill_md_before: dict[str, str],
    skip_skillsilent_probe: bool,
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    actual_sha = sha256_file(plan_path)
    checks.append(
        {
            "check": "PLAN_SHA256_MATCH",
            "pass": actual_sha == frozen_sha256,
            "expected": frozen_sha256,
            "actual": actual_sha,
        }
    )

    try:
        plan = load_json(plan_path)
        plan_skills = {str(x.get("skill")) for x in plan.get("items", []) if isinstance(x, dict)}
        scope_ok = (
            plan.get("scope") == "PRIVATE_SKILL_14_ONLY"
            and plan.get("group_common_skills_policy") == "NO_TOUCH"
            and plan_skills == PRIVATE_SET
            and plan.get("activation_apply_performed") is False
        )
    except Exception:
        scope_ok = False
        plan_skills = set()
    checks.append(
        {
            "check": "PRIVATE_SCOPE_GUARD",
            "pass": scope_ok,
            "plan_skill_count": len(plan_skills),
        }
    )

    # Revalidate exact 14 package/target paths, markers and managed closure.
    revalidated: list[dict[str, Any]] = []
    all_gate_ok = True
    for skill, version in PRIVATE_SKILLS.items():
        rec = gate_one_skill(skill, version, skills_root, private_root, main_root)
        revalidated.append(
            {
                "skill": skill,
                "status": rec["status"],
                "failures": rec["failures"],
                "blockers": rec["blockers"],
            }
        )
        if rec["status"] not in {"PASS", "WARN"}:
            all_gate_ok = False
    checks.append(
        {
            "check": "TARGET_IMPLEMENTATION_AND_MANIFEST_REVALIDATION",
            "pass": all_gate_ok,
            "items": revalidated,
        }
    )

    persistent_checks: list[dict[str, Any]] = []
    persistent_ok = True
    for skill in PRIVATE_SKILLS:
        root = (main_root / skill).resolve()
        after = tree_stat_fingerprint(root)
        before = main_before[skill]
        same = before == after
        persistent_checks.append(
            {"skill": skill, "unchanged": same, "before": before, "after": after}
        )
        persistent_ok = persistent_ok and same
    checks.append(
        {
            "check": "PERSISTENT_MAIN_UNCHANGED_DURING_V0_3_19",
            "pass": persistent_ok,
            "items": persistent_checks,
        }
    )

    skill_md_checks: list[dict[str, Any]] = []
    skill_md_ok = True
    for skill in PRIVATE_SKILLS:
        p = (skills_root / skill / "SKILL.md").resolve()
        after_sha = sha256_file(p) if p.is_file() and not p.is_symlink() else None
        same = after_sha == skill_md_before[skill]
        skill_md_checks.append(
            {
                "skill": skill,
                "unchanged": same,
                "before_sha256": skill_md_before[skill],
                "after_sha256": after_sha,
            }
        )
        skill_md_ok = skill_md_ok and same
    checks.append(
        {"check": "SKILL_MD_UNCHANGED_DURING_V0_3_19", "pass": skill_md_ok, "items": skill_md_checks}
    )

    probe = probe_skillsilent(skip_skillsilent_probe)
    checks.append({"check": "SKILLSILENT_OPERATIONAL_READ_ONLY_PROBE", "pass": probe["ok"], "detail": probe})

    # The executing Python process itself is the job-list runner operational signal.
    checks.append(
        {
            "check": "JOB_LIST_RUNNER_OPERATIONAL",
            "pass": True,
            "detail": f"job-list v{VERSION} process reached POST_CHECK",
        }
    )

    # This version contains no apply/reconcile/delete/move/rename/cleanup action.
    checks.append(
        {
            "check": "NO_UNSAFE_PENDING_OPERATION_IN_V0_3_19",
            "pass": True,
            "detail": "pre-activation runner exposes no Activation APPLY path",
        }
    )

    ok = all(bool(x["pass"]) for x in checks)
    return {
        "status": "PASS" if ok else "FAIL",
        "ready_for_activation": ok,
        "checks": checks,
    }


def resolve_roots(args: argparse.Namespace) -> tuple[Path, Path, Path, Path]:
    home = Path(args.home).expanduser().resolve() if args.home else Path.home().resolve()
    skills_root = (
        Path(args.skills_root).expanduser().resolve()
        if args.skills_root
        else (home / ".claude" / "skills").resolve()
    )
    private_root = (
        Path(args.private_root).expanduser().resolve()
        if args.private_root
        else (home / "l1sw-skills" / "private-skills").resolve()
    )
    main_root = (
        Path(args.main_root).expanduser().resolve()
        if args.main_root
        else (home / ".claude" / "main").resolve()
    )
    output_root = (
        Path(args.output_root).expanduser().resolve()
        if args.output_root
        else (main_root / "job-list" / "output" / "activation-precheck" / f"v{VERSION}").resolve()
    )
    assert_output_scope(output_root, main_root)
    return skills_root, private_root, main_root, output_root


def run(args: argparse.Namespace) -> int:
    started = now_iso()
    skills_root, private_root, main_root, output_root = resolve_roots(args)

    # Scope is intentionally closed and static.
    if len(PRIVATE_SKILLS) != 14 or set(PRIVATE_SKILLS) != PRIVATE_SET:
        raise SafeStop("PRIVATE_SCOPE_GUARD internal configuration invalid")

    run_dir = output_root / f"run_{stamp()}_{os.getpid()}"
    assert_output_scope(run_dir, main_root)
    run_dir.mkdir(parents=True, exist_ok=False)

    # Snapshot only the 14 exact private paths; do not enumerate group/common skills.
    main_before: dict[str, dict[str, Any]] = {}
    skill_md_before: dict[str, str] = {}
    for skill in PRIVATE_SKILLS:
        main_path = (main_root / skill).resolve()
        package_path = (skills_root / skill).resolve()
        assert_exact_private_path(main_path, main_root, skill)
        assert_exact_private_path(package_path, skills_root, skill)
        main_before[skill] = tree_stat_fingerprint(main_path)

        skill_md = package_path / "SKILL.md"
        if not skill_md.is_file() or skill_md.is_symlink():
            # Gate will report detailed error; keep placeholder for safe final check.
            skill_md_before[skill] = ""
        else:
            skill_md_before[skill] = sha256_file(skill_md)

    gate_items: list[dict[str, Any]] = []
    for skill, version in PRIVATE_SKILLS.items():
        gate_items.append(
            gate_one_skill(skill, version, skills_root, private_root, main_root)
        )

    counts = {
        key: sum(1 for x in gate_items if x["status"] == key)
        for key in ("PASS", "WARN", "FAIL", "BLOCKED")
    }
    gate_ok = counts["FAIL"] == 0 and counts["BLOCKED"] == 0

    gate_report = {
        "schema_version": 1,
        "engine_version": VERSION,
        "created_at": now_iso(),
        "scope": "PRIVATE_SKILL_14_ONLY",
        "group_common_skills_policy": "NO_TOUCH",
        "total_skills": 14,
        "counts": counts,
        "IMPLEMENTATION_REPAIR_COMPLETE": "YES" if gate_ok else "NO",
        "items": gate_items,
    }
    gate_path = run_dir / "implementation_repair_complete_gate.json"
    atomic_json(gate_path, gate_report)

    if not gate_ok:
        summary = {
            "RESULT_CODE": RESULT_FAILED_SAFE,
            "RESULT": "FAILED_SAFE",
            "FAILED_STAGE": "IMPLEMENTATION_REPAIR_COMPLETE_GATE",
            "TOTAL_SKILLS": 14,
            **counts,
            "IMPLEMENTATION_REPAIR_COMPLETE": "NO",
            "PLAN_GENERATED": "NO",
            "ACTIVATION_PERFORMED": "NO",
            "GROUP_COMMON_SKILL_TOUCHED": "NO",
            "PERSISTENT_MUTATION_PERFORMED": "NO",
            "NEXT_STEP": "REPAIR_FAILED_OR_BLOCKED_PRIVATE_SKILL_ONLY",
            "gate_report": str(gate_path),
            "started_at": started,
            "completed_at": now_iso(),
        }
        atomic_json(run_dir / "summary.json", summary)
        print_machine_summary(summary)
        return RESULT_FAILED_SAFE

    plan = build_activation_plan(gate_items)
    plan_path = run_dir / "activation_plan.json"
    atomic_json(plan_path, plan)
    frozen_sha = sha256_file(plan_path)
    atomic_write(plan_path.with_suffix(".json.sha256"), f"{frozen_sha}  {plan_path.name}\n")

    post = post_check(
        gate_items,
        plan_path,
        frozen_sha,
        skills_root,
        private_root,
        main_root,
        main_before,
        skill_md_before,
        args.skip_skillsilent_probe,
    )
    post_path = run_dir / "activation_post_check.json"
    atomic_json(post_path, post)

    ok = post["status"] == "PASS"
    summary = {
        "RESULT_CODE": RESULT_PASS if ok else RESULT_FAILED_SAFE,
        "RESULT": "PASS" if ok else "FAILED_SAFE",
        "FAILED_STAGE": None if ok else "ACTIVATION_POST_CHECK",
        "TOTAL_SKILLS": 14,
        **counts,
        "IMPLEMENTATION_REPAIR_COMPLETE": "YES",
        "PLAN_GENERATED": "YES",
        "PLAN_SHA256_FROZEN": "YES",
        "PLAN_SHA256": frozen_sha,
        "POST_CHECK": post["status"],
        "READY_FOR_ACTIVATION": "YES" if ok else "NO",
        "ACTIVATION_PERFORMED": "NO",
        "GROUP_COMMON_SKILL_TOUCHED": "NO",
        "PERSISTENT_MUTATION_PERFORMED": "NO",
        "KNOWLEDGE_MIGRATION_PERFORMED": "NO",
        "NEXT_STEP": "ACTIVATION_WAVES" if ok else "REPAIR_OR_REGENERATE_PLAN",
        "gate_report": str(gate_path),
        "activation_plan": str(plan_path),
        "post_check": str(post_path),
        "started_at": started,
        "completed_at": now_iso(),
    }
    atomic_json(run_dir / "summary.json", summary)
    print_machine_summary(summary)
    # Machine RESULT_CODE follows the project contract (1=PASS), while the OS
    # process exit code follows normal CLI semantics (0=success).
    return 0 if ok else RESULT_FAILED_SAFE


def print_machine_summary(summary: dict[str, Any]) -> None:
    ordered = (
        "RESULT_CODE",
        "RESULT",
        "FAILED_STAGE",
        "TOTAL_SKILLS",
        "PASS",
        "WARN",
        "FAIL",
        "BLOCKED",
        "IMPLEMENTATION_REPAIR_COMPLETE",
        "PLAN_GENERATED",
        "PLAN_SHA256_FROZEN",
        "PLAN_SHA256",
        "POST_CHECK",
        "READY_FOR_ACTIVATION",
        "ACTIVATION_PERFORMED",
        "GROUP_COMMON_SKILL_TOUCHED",
        "PERSISTENT_MUTATION_PERFORMED",
        "KNOWLEDGE_MIGRATION_PERFORMED",
        "NEXT_STEP",
        "gate_report",
        "activation_plan",
        "post_check",
    )
    for key in ordered:
        if key in summary and summary[key] is not None:
            print(f"{key}={summary[key]}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "job-list v0.3.19 Private-14 pre-activation gate/plan/SHA/post-check. "
            "No Activation APPLY."
        )
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument(
        "command",
        nargs="?",
        default="run",
        choices=("run",),
        help="Only 'run' exists. There is intentionally no apply command.",
    )
    parser.add_argument("--home", help="Override HOME for controlled validation/testing.")
    parser.add_argument("--skills-root", help="Override ~/.claude/skills.")
    parser.add_argument("--private-root", help="Override ~/l1sw-skills/private-skills.")
    parser.add_argument("--main-root", help="Override ~/.claude/main.")
    parser.add_argument(
        "--output-root",
        help="Override output root; must remain under <main-root>/job-list/output/.",
    )
    parser.add_argument(
        "--skip-skillsilent-probe",
        action="store_true",
        help="Controlled test override only; production should not use this.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return run(args)
    except SafeStop as exc:
        summary = {
            "RESULT_CODE": RESULT_FAILED_SAFE,
            "RESULT": "FAILED_SAFE",
            "FAILED_STAGE": "SCOPE_OR_PRECHECK",
            "ACTIVATION_PERFORMED": "NO",
            "GROUP_COMMON_SKILL_TOUCHED": "NO",
            "PERSISTENT_MUTATION_PERFORMED": "NO",
            "NEXT_STEP": "FIX_PRECHECK",
            "ERROR": str(exc),
        }
        print_machine_summary(summary)
        print(f"ERROR={exc}")
        return RESULT_FAILED_SAFE
    except Exception as exc:
        # Fail closed. This runner has no mutation path for Skill sources/targets.
        summary = {
            "RESULT_CODE": RESULT_FAILED_SAFE,
            "RESULT": "FAILED_SAFE",
            "FAILED_STAGE": "UNEXPECTED_EXCEPTION",
            "ACTIVATION_PERFORMED": "NO",
            "GROUP_COMMON_SKILL_TOUCHED": "NO",
            "PERSISTENT_MUTATION_PERFORMED": "NO",
            "NEXT_STEP": "REVIEW_LOCAL_JOB_LIST_OUTPUT",
            "ERROR": repr(exc),
        }
        print_machine_summary(summary)
        print(f"ERROR={exc!r}")
        return RESULT_FAILED_SAFE


if __name__ == "__main__":
    sys.exit(main())
