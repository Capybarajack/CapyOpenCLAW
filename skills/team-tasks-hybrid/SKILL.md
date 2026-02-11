---
name: team-tasks-hybrid
description: Run Team-Tasks in dual mode (Local workers + Telegram workers) with one shared pipeline model. Use when you want stable local orchestration by default, keep Telegram worker groups as a fallback/visibility channel, and switch dispatch backend without changing task_manager project structure.
---

# Team-Tasks Hybrid (Local + Telegram)

Operate one `team-tasks` workflow with two interchangeable dispatch backends:

- **Local mode**: dispatch with `sessions_spawn(agentId=...)`
- **Telegram mode**: dispatch with `sessions_send(sessionKey="agent:<agent>:telegram:group:<id>", ...)`

Use the same `task_manager.py` JSON state for both modes.

## Baseline architecture

- Orchestrator: `main`
- Workers: `code-agent`, `test-agent`, `docs-agent`, `monitor-bot`
- Shared pipeline state: `task_manager.py`

## Required config (minimum)

1. Define worker agents in `agents.list`
2. Allow orchestrator cross-agent spawn:
   - `agents.list[id=main].subagents.allowAgents = ["code-agent","test-agent","docs-agent","monitor-bot"]`
3. Keep Telegram bindings for worker groups (optional at runtime, preserved for fallback)
4. For Telegram reliability, enforce:
   - `channels.telegram.retry.attempts = 3`

## Standard pipeline (unchanged across modes)

1. `init` project
2. `assign` tasks to stage/agent
3. Dispatch stage task
4. Save `result` (use fixed envelope format below)
5. Mark `done`
6. Continue until complete

Only step 3 changes by mode.

## Visible result envelope (fixed format)

To make stage outputs readable in CLI/JSON and easy to scan, always write `task_manager result` using this envelope:

```text
[TT_RESULT]
stage: <code-agent|test-agent|docs-agent|monitor-bot>
status: <ok|warn|fail>
summary: <1 sentence>
deliverables:
- <artifact or action 1>
- <artifact or action 2>
risks:
- <risk or none>
next:
- <next step>
[/TT_RESULT]
```

Example:

```text
[TT_RESULT]
stage: test-agent
status: ok
summary: Smoke checks passed for feature X.
deliverables:
- Added 6 integration tests
- Updated CI test matrix
risks:
- None
next:
- Hand off to docs-agent for changelog update
[/TT_RESULT]
```

Write this full block into `task_manager.py result <project> <stage> "..."`.

## Dispatch step by mode

### Local mode (default for stability)

- `sessions_spawn(task=<task text>, agentId=<stage-agent>, label="tt:<project>:<stage>")`

Use when you want lower latency and no Telegram transport dependency.

### Telegram mode (fallback / visibility)

- `sessions_send(sessionKey="agent:<agent>:telegram:group:<chatId>", message=<task text>)`

Use when you want human-visible worker activity in Telegram groups.

## Mode switch rule

- Keep one project file and one stage model.
- Switch only dispatch transport.
- Never duplicate project state per channel.

## Failure handling

### Local mode failure

1. `update <project> <stage> failed`
2. `log <project> <stage> "<error>"`
3. `reset <project> <stage>`
4. Re-dispatch locally

### Telegram mode failure

1. Apply `telegram-retry-guard`
2. Verify retry cap = 3
3. If transient channel issue persists, switch current stage to Local mode and continue pipeline

## Practical lessons (codified)

- Treat Telegram as a dispatch backend, not the workflow source of truth.
- Keep pipeline truth in `task_manager.py` only.
- Keep both backends configured; choose transport per run.
- Prefer Local mode for reliability; use Telegram mode for team visibility.

## Smoke test checklist

1. Run one 4-stage linear project in Local mode to completion
2. Run one stage in Telegram mode and capture result
3. Switch back to Local mode for remaining stages
4. Confirm final status = complete and results persisted
