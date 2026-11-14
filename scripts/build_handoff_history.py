#!/usr/bin/env python3
"""Publish a small, public-only handoff history for GitHub Pages.

Only files already committed under L1Work/handoffs are indexed. This does not
read private repositories or infer whether a review/feedback was performed.
"""
import json
import re
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "handoffs"
TARGET = ROOT / "docs" / "cowork-dashboard" / "handoffs.json"
KST = timezone(timedelta(hours=9))
FILE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,179}\.md\Z")


def published_on(relative: str) -> str:
    history = subprocess.run(
        ["git", "log", "--follow", "--diff-filter=A", "--format=%cI", "--", relative],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.strip().splitlines()
    if not history:
        raise ValueError(f"Missing Git creation history: {relative}")
    return datetime.fromisoformat(history[-1]).astimezone(KST).date().isoformat()


def title_for(path: Path) -> str:
    if path.stat().st_size > 300_000:
        raise ValueError(f"Oversized public handoff: {path.name}")
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            if not title or len(title) > 130:
                raise ValueError(f"Invalid public handoff title: {path.name}")
            return title
    raise ValueError(f"Missing public handoff heading: {path.name}")


def build() -> dict:
    entries = []
    for path in sorted(SOURCE.glob("*.md")):
        name = path.name
        if (path.is_symlink() or not path.is_file() or name.lower() == "readme.md"
                or not FILE_NAME.fullmatch(name) or "HANDOFF" not in name.upper()):
            continue
        relative = "handoffs/" + name
        entries.append({
            "filename": name,
            "title": title_for(path),
            "published_on": published_on(relative),
        })
    entries.sort(key=lambda item: (item["published_on"], item["filename"]), reverse=True)
    return {"schema": "L1WORK_HANDOFF_HISTORY_V1", "entries": entries[:3]}


if __name__ == "__main__":
    TARGET.write_text(json.dumps(build(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
