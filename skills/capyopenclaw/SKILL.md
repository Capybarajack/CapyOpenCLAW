---
name: capyopenclaw
description: Apply the CapyOpenCLAW workflow and accumulated learnings when doing programming work for this user. Use this skill for all future development tasks to enforce OpenSpec (OPSX) spec-driven workflow, Codex CLI execution, and the rule that learnings are written back into this skill and pushed to https://github.com/Capybarajack/CapyOpenCLAW.git.
---

# CapyOpenCLAW (User Workflow + Learnings)

## Non-negotiables

1. Use **OpenSpec (OPSX)** for all programming work.
2. Use **Codex CLI** to implement (do not hand-edit code as the primary implementation path).
   - Run Codex with **`pty:true`**.
   - Run inside a **git repo**.
3. For **frontend/UI work**, apply the **`frontend-design`** skill (Anthropic) to drive interface aesthetics and production-grade UI output.
4. After finishing a full workflow cycle (planning → implementation → verification → archive), update learnings:
   - Append to `references/learnings.md`.
   - Keep entries short and actionable.
5. After each skill update, **commit and push** to: https://github.com/Capybarajack/CapyOpenCLAW.git

## Standard workflow (OPSX)

For each change:

- Create change: `/opsx:new <change-name>`
- Create artifacts:
  - Prefer `/opsx:ff` when scope is clear.
  - Prefer `/opsx:continue` when exploring/uncertain.
- Implement: `/opsx:apply`
- Verify: `/opsx:verify`
- Finish: `/opsx:archive` (sync specs if prompted)

## How to write learnings

Append to `references/learnings.md` using this format:

- **Date**: YYYY-MM-DD
- **Context**: project + change name
- **What worked**: 1–3 bullets
- **What failed / pitfalls**: 1–3 bullets
- **Decision / rule for next time**: 1 bullet (actionable)

Keep it practical; avoid essays.
