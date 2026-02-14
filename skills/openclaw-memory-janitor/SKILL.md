---
name: openclaw-memory-janitor
description: Set up and maintain an OpenClaw 3-tier memory system: hot MEMORY.md (≤200 lines) with [P0/P1/P2] priority tags and TTL ([P1]=90d, [P2]=30d), cold archives under memory/archive/ (kept searchable by memory_search), and raw daily logs memory/YYYY-MM-DD.md that are never auto-loaded. Use when a user asks to configure memory retention, archiving, hot/cold memory separation, or to add a daily cron that runs a memory janitor script.
---

# OpenClaw memory system (hot/cold/logs) + janitor

## Goal

Implement:
- **Hot memory**: `MEMORY.md` ≤ 200 lines, curated bullets.
- **Cold memory**: archived items moved to `memory/archive/` so they remain searchable.
- **Raw logs**: `memory/YYYY-MM-DD.md` left untouched and not auto-loaded.
- **Automation**: `memory-janitor.py` + daily cron.

## Why `memory/archive/` (not `archive/`)

OpenClaw `memory_search` indexes `MEMORY.md` + `memory/*.md`. Put archives under `memory/archive/` so semantic recall keeps working.

## Required formats

Hot memory bullets:
- `- [P0] ...` (never expires)
- `- [P1][ts:YYYY-MM-DD] ...` (expires after 90 days)
- `- [P2][ts:YYYY-MM-DD] ...` (expires after 30 days)

Notes:
- Only bullet lines starting with `-` are considered.
- P1/P2 without `[ts:...]` must NOT be auto-archived (avoid accidental deletion).

## Setup workflow

1) **Write hot memory template**
- Copy `references/MEMORY.template.md` to workspace root as `MEMORY.md` (or merge carefully if existing).

2) **Install the janitor script**
- Copy `scripts/memory-janitor.py` to workspace root as `memory-janitor.py`.
- Windows: run with `py memory-janitor.py`.
- macOS/Linux: run with `python3 memory-janitor.py`.

3) **Create archive folder**
- Ensure `memory/archive/` exists.

4) **Add daily cron**
- Use OpenClaw `cron.add` with:
  - `sessionTarget: "isolated"`
  - schedule: `08:39` in `Asia/Taipei` (or user-specified)
  - payload: run `py memory-janitor.py`, then report summary + warnings.

## Recommended agent behavior (to keep logs cold)

If maintaining an `AGENTS.md`-style playbook:
- In main session: load `MEMORY.md`.
- Do **not** auto-load `memory/YYYY-MM-DD.md` unless user requests a retrospective / summarization / archiving task.
