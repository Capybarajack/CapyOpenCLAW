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
