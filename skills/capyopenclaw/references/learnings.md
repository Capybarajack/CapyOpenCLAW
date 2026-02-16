# Learnings (CapyOpenCLAW)

- **Date**: 2026-02-01
  - **Context**: OpenClaw setup / workflow decision
  - **What worked**:
    - Switching GitHub reads to `raw.githubusercontent.com` avoided GitHub UI rate-limit blocks.
  - **What failed / pitfalls**:
    - Fetching multiple GitHub `blob` pages quickly can trigger GitHub abuse-rate-limits (HTTP 429).
  - **Decision / rule for next time**:
    - Prefer `raw.githubusercontent.com/<org>/<repo>/<branch>/<path>` for docs ingestion.

- **Date**: 2026-02-01
  - **Context**: Skill installation / frontend UI quality
  - **What worked**:
    - Installed Anthropic `frontend-design` skill via git sparse-checkout and copied into `skills/frontend-design/`.
  - **What failed / pitfalls**:
    - None noted yet.
  - **Decision / rule for next time**:
    - For frontend/UI tasks, always apply `frontend-design` to avoid generic UI output.

- **Date**: 2026-02-01
  - **Context**: Codex official docs → reusable skill
  - **What worked**:
    - Summarized Codex official docs into a small, referencable skill with separate reference files.
  - **What failed / pitfalls**:
    - N/A
  - **Decision / rule for next time**:
    - Keep SKILL.md concise; put long doc excerpts into `references/*` and link back to official docs.

- **Date**: 2026-02-03
  - **Context**: ProteinCare UI refactor / Codex CLI sandbox restrictions
  - **What worked**:
    - When aligning page UI, reusing existing design system classes (pc-frame / pc-topbar / pc-bottombar / pc-card / preview-frame) keeps styles consistent across pages.
  - **What failed / pitfalls**:
    - Codex CLI runs may be forced into `sandbox: read-only` + `approval: never` in this environment, preventing file writes even when passing `-s workspace-write`.
  - **Decision / rule for next time**:
    - If Codex cannot write due to enforced read-only sandbox, fall back to OpenClaw file tools (write/edit) and then verify via `npm run build` + git commit/push.

- **Date**: 2026-02-04
  - **Context**: ProteinCare UX improvement (one-click analysis) + blue palette refresh
  - **What worked**:
    - Driving the flow via a query flag (`/analysis?autostart=1`) allows “one click” UX without removing the Analysis page’s manual trigger (safer for cost control).
    - Refactoring accent color usages to `rgba(var(--accent-rgb), …)` keeps the palette consistent and makes future theme swaps much easier.
  - **What failed / pitfalls**:
    - Hard-coded inline RGBA values can easily drift from the global theme; prefer CSS variables whenever possible.
  - **Decision / rule for next time**:
    - For UX auto-actions that have cost (API tokens), gate them behind an explicit route flag instead of auto-running on page visit.

- **Date**: 2026-02-11
  - **Context**: CapyOpenCLAW `team-tasks` skill ingestion and normalization
  - **What worked**:
    - Rewriting SKILL instructions to be cross-platform (`python`/`python3`) made usage clearer for Windows + Linux users.
    - Replacing hardcoded host paths and Telegram IDs with placeholders and environment guidance reduced portability risk.
  - **What failed / pitfalls**:
    - Imported third-party skills often include environment-specific paths and IDs that do not match local deployments.
  - **Decision / rule for next time**:
    - After importing external skills, immediately run a portability pass (paths, interpreter command, identifiers) before marking as production-ready.

- **Date**: 2026-02-11
  - **Context**: Installing `microsoft/markitdown` as a reusable OpenClaw skill
  - **What worked**:
    - Importing upstream source into `skills/markitdown` and adding a concise `SKILL.md` made the repo discoverable by OpenClaw skill scanning.
    - Verifying with `openclaw status --all` immediately confirmed skill eligibility count increase.
  - **What failed / pitfalls**:
    - On Windows, `python` was unavailable in PATH while `py` worked; installation commands must account for launcher differences.
  - **Decision / rule for next time**:
    - For Python-based skills on Windows, try `py -m pip ...` first and include cross-platform launcher notes in SKILL instructions.

- **Date**: 2026-02-11
  - **Context**: New Telegram reliability skill (`telegram-retry-guard`)
  - **What worked**:
    - Mapping outbound reliability to built-in `channels.telegram.retry` made the 3-attempt requirement explicit and enforceable.
    - Separating inbound handling into a 3-cycle recovery/probe flow avoided promising impossible per-message replay.
  - **What failed / pitfalls**:
    - Inbound Telegram delivery cannot be force-retried message-by-message from OpenClaw alone.
  - **Decision / rule for next time**:
    - For channel reliability skills, codify what is configurable (retry policy) and explicitly define an operational recovery loop for non-replayable failures.

- **Date**: 2026-02-11
  - **Context**: Team-tasks local-mode template while preserving Telegram worker mode
  - **What worked**:
    - Adding a Mode C (local workers) to SKILL guidance enabled channel-independent orchestration using the same task-manager state machine.
    - Keeping Telegram and local dispatch as interchangeable execution backends reduced migration risk.
  - **What failed / pitfalls**:
    - Team instructions can drift toward channel-specific assumptions unless explicitly documenting both dispatch paths.
  - **Decision / rule for next time**:
    - For multi-agent skills, always document at least one non-channel fallback workflow (local/session-based) next to channel-based mode.

- **Date**: 2026-02-11
  - **Context**: New hybrid knowledge skill (`team-tasks-hybrid`) for reusable execution experience
  - **What worked**:
    - Encapsulating "local default + Telegram fallback" as a separate skill made the operating model reusable across projects.
    - Keeping transport-switch logic explicit prevented state duplication between local and Telegram runs.
  - **What failed / pitfalls**:
    - Without a hard rule, operators may accidentally split truth across channels instead of task_manager state.
  - **Decision / rule for next time**:
    - Define a single source of truth (task_manager JSON) and treat all channels as dispatch backends only.

- **Date**: 2026-02-11
  - **Context**: Team-tasks output visibility enhancement (fixed result envelope)
  - **What worked**:
    - Defining a strict `[TT_RESULT]...[/TT_RESULT]` block made stage outputs consistently readable across CLI, JSON state, and chat summaries.
    - Applying the same format to both local and Telegram-backed flows kept reporting uniform when switching transport.
  - **What failed / pitfalls**:
    - Free-form `result` text quickly becomes hard to scan and compare between stages.
  - **Decision / rule for next time**:
    - For multi-stage pipelines, standardize `result` payloads with a small fixed schema before scaling usage.

- **Date**: 2026-02-16
  - **Context**: CapyOpenCLAW skills / vendoring github/spec-kit
  - **What worked**:
    - Using `git subtree add --prefix=skills/spec-kit/upstream ... --squash` cleanly vendors upstream while keeping a local wrapper at `skills/spec-kit/SKILL.md`.
  - **What failed / pitfalls**:
    - Codex CLI global flags must be placed **before** the subcommand (e.g. `codex --full-auto exec "..."`), otherwise they may not take effect.
    - PowerShell does not support `&&` for command chaining; use `;` instead.
  - **Decision / rule for next time**:
    - Prefer vendoring external skill sources under `skills/<name>/upstream` via subtree, and keep OpenClaw wrapper docs in `skills/<name>/SKILL.md`.

- **Date**: 2026-02-16
  - **Context**: CapyOpenCLAW skills / add microsoft/TRELLIS.2
  - **What worked**:
    - Adding TRELLIS.2 as a docs-only wrapper skill (install + usage + upstream links) keeps the skills repo lightweight while still being actionable.
  - **What failed / pitfalls**:
    - Codex CLI may be constrained to `sandbox: read-only` in this environment and cannot create/modify files.
  - **Decision / rule for next time**:
    - For large ML research repos, prefer a concise wrapper skill with copy/paste commands instead of vendoring the full upstream source.
