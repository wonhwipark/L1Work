#!/usr/bin/env python3
"""Build a curated current index while surfacing unclassified new handoffs."""
import argparse
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "handoffs/README.md"
START = "<!-- BEGIN HANDOFF_CURRENT_INDEX: managed by scripts/build_handoff_current_index.py -->"
END = "<!-- END HANDOFF_CURRENT_INDEX -->"
DOC = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]*\.md\Z")


def run(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout


def safe(value):
    if not isinstance(value, str) or not value.strip() or any(c in value for c in "\r\n|[]<>"):
        raise ValueError("Invalid index label: " + repr(value))
    return value.strip()


def document(name):
    if not isinstance(name, str) or not DOC.fullmatch(name) or name == "README.md":
        raise ValueError("Invalid handoff path: " + repr(name))
    path = ROOT / "handoffs" / name
    if not path.is_file() or path.is_symlink() or path.stat().st_size > 300000:
        raise ValueError("Missing or unsafe handoff: " + name)
    return name


def build():
    data = json.loads((ROOT / "handoffs/current-index.json").read_text(encoding="utf-8"))
    if data.get("schema") != "HANDOFF_CURRENT_INDEX_V1":
        raise ValueError("Unexpected schema")
    baseline = data["baseline_commit"]
    if not re.fullmatch(r"[a-f0-9]{40}", baseline):
        raise ValueError("Bad baseline SHA")
    run("cat-file", "-e", baseline + "^{commit}")
    projects = data["projects"]
    if not projects:
        raise ValueError("Missing projects")
    rows, included, ids = [], set(), set()
    for p in projects:
        key = safe(p["id"])
        if key in ids:
            raise ValueError("Duplicate project")
        ids.add(key)
        name = document(p["primary"])
        included.add(name)
        documents = [name]
        links = ["[" + safe(p["primary_label"]) + "](" + name + ")"]
        for r in p.get("related", []):
            name = document(r["file"])
            included.add(name)
            documents.append(name)
            links.append("[" + safe(r["label"]) + "](" + name + ")")
        dates = [run("log", "-1", "--format=%ct", "--", "handoffs/" + doc).strip() for doc in documents]
        updated = datetime.fromtimestamp(max(int(d) for d in dates), timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M") if all(dates) else "미확인"
        rows.append("| " + safe(p["title"]) + " | " + " · ".join(links) + " | "
                    + updated + " | " + safe(p["status"]) + " | " + safe(p["next_action"]) + " |")
    changed = run("diff", "--name-only", baseline, "HEAD", "--", "handoffs/").splitlines()
    pending = sorted({Path(p).name for p in changed
                      if p.startswith("handoffs/") and p.endswith(".md")
                      and Path(p).name not in included and Path(p).name != "README.md"
                      and (ROOT / p).is_file()})
    for name in pending:
        document(name)
    lines = [START, "# 인계서 최신 정본 인덱스", "",
             "> 최신 정본은 명시적으로 검토·등록합니다. 새 인계서 게시와 업무 GPT 실제 적용·운영은 구분합니다. 업데이트 날짜는 등록된 정본·보완 문서의 마지막 Git 커밋 일시 중 최신값(KST)입니다.", "",
             "| 관리 영역 | 최신 정본 및 보완 문서 | 마지막 문서 업데이트 (KST) | 현재 확인 상태 | 다음 조치 |",
             "|---|---|---|---|---|", *rows, "",
             "## 신규·변경 인계서 (정본 미분류)", ""]
    if pending:
        lines += ["새로 게시되었지만 정본으로 승격되지 않았습니다. 대체·보완 관계를 검토한 뒤 "
                  "handoffs/current-index.json에 등록하세요.", ""]
        lines += ["- [" + name + "](" + name + ") — 정본 미분류 / 실제 적용 미확인"
                  for name in pending]
    else:
        lines += ["현재 정본 인덱스 생성 기준 이후 신규·변경 미분류 문서는 없습니다. "
                  "새 문서는 정본 자동 승격 대신 이곳에 표시됩니다."]
    lines += ["", "기존 인계서와 검증 기록은 아래의 작성 당시 이력을 보존합니다.", END]
    original = README.read_text(encoding="utf-8")
    if original.count(START) != original.count(END) or original.count(START) > 1:
        raise ValueError("Invalid index markers")
    block = "\n".join(lines)
    if START in original:
        before, rest = original.split(START, 1)
        _, after = rest.split(END, 1)
        return before + block + after
    return block + "\n\n---\n\n## 기존 인계서 이력 (작성 당시 기준)\n\n" + original


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    opts = parser.parse_args()
    expected = build()
    actual = README.read_text(encoding="utf-8")
    if opts.check:
        if actual != expected:
            raise SystemExit("README_INDEX_STALE")
        print("README_INDEX=PASS")
    elif actual != expected:
        README.write_text(expected, encoding="utf-8")
        print("README_INDEX=UPDATED")
    else:
        print("README_INDEX=UNCHANGED")
