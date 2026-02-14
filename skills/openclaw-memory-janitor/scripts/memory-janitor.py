#!/usr/bin/env python3
"""memory-janitor.py

Maintain a 3-tier OpenClaw memory system:
- Hot memory: MEMORY.md (keep ≤ 200 lines)
- Cold memory: memory/archive/ (archived / expired items; still searchable)
- Raw logs: memory/YYYY-MM-DD.md (untouched)

Rules:
- [P0] never expires.
- [P1][ts:YYYY-MM-DD] expires after 90 days.
- [P2][ts:YYYY-MM-DD] expires after 30 days.
- P1/P2 missing [ts:...] are NOT archived (safety).
- If MEMORY.md is still > 200 lines after expiring items, archive oldest P2 items (by ts) until ≤ 200.

Usage:
  python3 memory-janitor.py
  python3 memory-janitor.py --dry-run
  python3 memory-janitor.py --now 2026-02-14

Windows equivalent:
  py memory-janitor.py ...
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import List, Optional, Tuple

TS_RE = re.compile(r"\[ts:(\d{4}-\d{2}-\d{2})\]")
PRIO_RE = re.compile(r"\[(P0|P1|P2)\]")


@dataclass
class MemoryItem:
    idx: int
    line: str
    prio: str
    ts: Optional[date]


def parse_iso_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def find_prio(line: str) -> Optional[str]:
    m = PRIO_RE.search(line)
    return m.group(1) if m else None


def find_ts(line: str) -> Optional[date]:
    m = TS_RE.search(line)
    if not m:
        return None
    try:
        return parse_iso_date(m.group(1))
    except ValueError:
        return None


def get_expiry_days(prio: str) -> Optional[int]:
    if prio == "P1":
        return 90
    if prio == "P2":
        return 30
    return None


def load_items(lines: List[str]) -> Tuple[List[MemoryItem], List[str]]:
    items: List[MemoryItem] = []
    warnings: List[str] = []

    for i, raw in enumerate(lines):
        line = raw.rstrip("\n")
        if not line.lstrip().startswith("-"):
            continue
        prio = find_prio(line)
        if prio not in ("P0", "P1", "P2"):
            continue
        ts = find_ts(line)
        if prio in ("P1", "P2") and ts is None:
            warnings.append(
                f"Line {i+1}: {prio} item missing [ts:YYYY-MM-DD]; will NOT be auto-archived: {line}"
            )
        items.append(MemoryItem(idx=i, line=line, prio=prio, ts=ts))

    return items, warnings


def archive_path(root: Path, today: date) -> Path:
    arch_dir = root / "memory" / "archive"
    arch_dir.mkdir(parents=True, exist_ok=True)
    return arch_dir / f"MEMORY-archive-{today.isoformat()}.md"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Show what would change; write nothing")
    ap.add_argument("--now", type=str, default=None, help="Override today's date (YYYY-MM-DD)")
    args = ap.parse_args()

    root = Path.cwd()
    mem_path = root / "MEMORY.md"

    if not mem_path.exists():
        print(f"ERROR: {mem_path} not found")
        return 2

    today = parse_iso_date(args.now) if args.now else date.today()

    lines = mem_path.read_text(encoding="utf-8").splitlines(True)
    items, warnings = load_items(lines)
    had_format_warnings = bool(warnings)

    if warnings:
        print("WARN: format issues found (fix these to enable auto-archiving):")
        for w in warnings:
            print("- " + w)

    expired: List[MemoryItem] = []
    for it in items:
        expiry = get_expiry_days(it.prio)
        if expiry is None or it.ts is None:
            continue
        if (today - it.ts).days > expiry:
            expired.append(it)

    overflow: List[MemoryItem] = []
    remove_idx = {it.idx for it in expired}
    projected_lines = len(lines) - len(remove_idx)

    if projected_lines > 200:
        candidates = [
            it for it in items if it.prio == "P2" and it.ts is not None and it.idx not in remove_idx
        ]
        candidates.sort(key=lambda x: x.ts)  # oldest first

        while projected_lines > 200 and candidates:
            it = candidates.pop(0)
            overflow.append(it)
            remove_idx.add(it.idx)
            projected_lines -= 1

    to_archive = expired + overflow

    if not to_archive:
        print("OK: nothing to archive")
        if len(lines) > 200:
            print(f"WARN: MEMORY.md is {len(lines)} lines (>200) and no archivable P2 items were found.")
            return 2
        return 2 if had_format_warnings else 0

    arch_file = archive_path(root, today)

    if args.dry_run:
        print("DRY RUN: would archive:")
        if expired:
            print("- Expired items:")
            for it in sorted(expired, key=lambda x: x.idx):
                print(f"  - Line {it.idx+1}: {it.line}")
        if overflow:
            print("- Line-limit pruning (overflow; oldest P2 first):")
            for it in sorted(overflow, key=lambda x: x.ts or date.min):
                print(f"  - Line {it.idx+1}: {it.line}")
        return 0

    archived_block: List[str] = []
    archived_block.append(f"# MEMORY Archive — {today.isoformat()}\n\n")
    archived_block.append("Archived from `MEMORY.md` by `memory-janitor.py`.\n\n")

    if expired:
        archived_block.append("## Expired items\n\n")
        for it in sorted(expired, key=lambda x: x.idx):
            archived_block.append(f"- [{it.prio}] {it.line.lstrip('-').strip()}\n")
        archived_block.append("\n")

    if overflow:
        archived_block.append("## Line-limit pruning (overflow)\n\n")
        archived_block.append("Archived to keep `MEMORY.md` ≤ 200 lines (oldest P2 first).\n\n")
        for it in sorted(overflow, key=lambda x: x.ts or date.min):
            archived_block.append(f"- [{it.prio}] {it.line.lstrip('-').strip()}\n")
        archived_block.append("\n")

    # Delete archived lines from MEMORY.md (bottom-up for stable indices)
    for idx in sorted({it.idx for it in to_archive}, reverse=True):
        del lines[idx]

    arch_file.parent.mkdir(parents=True, exist_ok=True)
    with arch_file.open("a", encoding="utf-8") as f:
        f.writelines(archived_block)
        f.write("\n")

    mem_path.write_text("".join(lines), encoding="utf-8")

    print(
        f"OK: archived {len(to_archive)} item(s) (expired={len(expired)}, overflow={len(overflow)}) -> {arch_file}"
    )

    if len(lines) > 200:
        print(f"WARN: MEMORY.md is still {len(lines)} lines (>200). Consider pruning.")
        return 2

    return 2 if had_format_warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
