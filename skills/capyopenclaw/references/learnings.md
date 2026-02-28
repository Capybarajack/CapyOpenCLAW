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

- **Date**: 2026-02-17
  - **Context**: CapyOpenCLAW skills / import anthropics `webapp-testing`
  - **What worked**:
    - Pulling upstream skill folder (`skills/webapp-testing`) directly preserved runnable examples and helper script structure.
  - **What failed / pitfalls**:
    - If imported files are copied from GitHub UI manually, it's easy to miss nested example files.
  - **Decision / rule for next time**:
    - For external skill installs, clone upstream repo then copy the exact skill directory recursively and verify file list before commit.

- **Date**: 2026-02-18
  - **Context**: New Steam documentation skill (`steam-web-api-docs`)
  - **What worked**:
    - Designing the skill around source confidence (official > community > live sanity check) produced stable, implementation-ready summaries.
    - Including a fixed output template improved consistency across multi-link document ingestion.
  - **What failed / pitfalls**:
    - Valve Developer Wiki pages can be blocked by anti-bot challenges, so full text extraction is not always possible.
  - **Decision / rule for next time**:
    - When docs are blocked, verify endpoint contracts directly via `api.steampowered.com` and clearly label confidence level in the final analysis.

- **Date**: 2026-02-21
  - **Context**: CapyOpenCLAW skills / import `react-best-practices` from `vercel-labs/agent-skills`
  - **What worked**:
    - Cloning upstream repo and recursively copying `skills/react-best-practices` preserved all nested `rules/*.md` references and metadata in one pass.
  - **What failed / pitfalls**:
    - N/A
  - **Decision / rule for next time**:
    - For skill imports with many rule files, avoid manual file-by-file copy; use full directory copy and verify recursive file inventory before commit.

- **Date**: 2026-02-21
  - **Context**: CapyOpenCLAW skills / import `ui-ux-pro-max-skill` from `nextlevelbuilder`
  - **What worked**:
    - Using `src/ui-ux-pro-max` as the primary source and copying `.claude/skills/ui-ux-pro-max/SKILL.md` produced a runnable local OpenClaw skill layout.
  - **What failed / pitfalls**:
    - On Windows clones, `.claude/skills/ui-ux-pro-max/data` and `scripts` may appear as plain text symlink targets instead of real folders.
  - **Decision / rule for next time**:
    - For repos using symlinked skill assets, copy concrete source directories (e.g., `src/...`) rather than relying on symlink placeholders.

- **Date**: 2026-02-21
  - **Context**: `ui-ux-pro-max` SKILL.md optimization for OpenClaw triggering/token cost
  - **What worked**:
    - Replacing the long monolithic guide with a concise workflow-first SKILL kept trigger intent while reducing instruction bloat.
  - **What failed / pitfalls**:
    - Overly long descriptions in frontmatter and repeated checklists increase token overhead without improving execution quality.
  - **Decision / rule for next time**:
    - Keep SKILL.md minimal (when-to-use + required workflow + output contract) and keep large references in separate files.

- **Date**: 2026-02-21
  - **Context**: CapyOpenCLAW skills / import `vuejs-ai/skills` bundle
  - **What worked**:
    - Copying each folder from upstream `skills/` into workspace `skills/` installed the whole Vue skill set in one batch.
  - **What failed / pitfalls**:
    - Running `git status skills` can surface unrelated untracked skill dirs (e.g., legacy local folders) that should not be staged accidentally.
  - **Decision / rule for next time**:
    - Stage imported skill directories explicitly by name to avoid committing unrelated untracked folders.

- **Date**: 2026-02-21
  - **Context**: CapyOpenCLAW skills / import `nodejs-backend-patterns` from `wshobson/agents`
  - **What worked**:
    - Cloning upstream repo and copying the exact nested path (`plugins/javascript-typescript/skills/nodejs-backend-patterns`) installed the target skill cleanly.
  - **What failed / pitfalls**:
    - Deep plugin paths are easy to mistype, causing silent installs of wrong folders.
  - **Decision / rule for next time**:
    - For deeply nested skill URLs, resolve and verify source path exists before copying, then stage destination explicitly.

- **Date**: 2026-02-21
  - **Context**: CapyOpenCLAW skills / import non-skill repo `ssengalanto/tailwind-design-system`
  - **What worked**:
    - Wrapping the upstream project under `skills/tailwind-design-system/upstream` plus a concise local `SKILL.md` made a non-native repo usable as an OpenClaw skill.
  - **What failed / pitfalls**:
    - Some GitHub repos are app templates, not agent-skill folders, so direct copy alone won’t trigger skill discovery.
  - **Decision / rule for next time**:
    - When upstream lacks `SKILL.md`, create a lightweight wrapper skill and keep original source in `upstream/` for reference-driven reuse.

- **Date**: 2026-02-21
  - **Context**: Skills taxonomy refactor (`atomic + category naming + router layer`)
  - **What worked**:
    - Adding lightweight router skills (`frontend-ui-playbook`, `frontend-vue-playbook`, `frontend-react-playbook`, `backend-node-playbook`) improved discovery without merging atomic skills.
    - Maintaining a root `skills/INDEX.md` provided a single source of truth for categories and routing entry points.
  - **What failed / pitfalls**:
    - Renaming/moving every atomic folder is high-risk and unnecessary when trigger quality can be improved by router metadata.
  - **Decision / rule for next time**:
    - Prefer non-breaking taxonomy layers (index + routers) over mass folder renames; keep atomic skills stable.

- **Date**: 2026-02-21
  - **Context**: CapyOpenCLAW skills / import `brainstorming` from `obra/superpowers`
  - **What worked**:
    - Copying the exact skill subfolder (`skills/brainstorming`) cleanly installed a focused single-file skill.
  - **What failed / pitfalls**:
    - Repos with many skills can cause accidental bulk imports if source path is not constrained.
  - **Decision / rule for next time**:
    - For one-off installs, always copy only the requested skill folder path and verify destination contents before commit.

- **Date**: 2026-02-21
  - **Context**: CapyOpenCLAW skills / import `smart-illustrator` from `axtonliu/smart-illustrator`
  - **What worked**:
    - Upstream repo already followed skill layout (`SKILL.md` + scripts/references/assets), so full-folder copy worked directly.
  - **What failed / pitfalls**:
    - Copying `.git` metadata into workspace skills can pollute repo state if not excluded.
  - **Decision / rule for next time**:
    - For full-repo skill imports, mirror all content except VCS/runtime folders (`.git`, `node_modules`) and keep folder name kebab-case.

- **Date**: 2026-02-28
  - **Context**: CapyOpenCLAW skills / learned `isdaviddong/HOL_MSAgentFrameworkRC` and packaged as skill
  - **What worked**:
    - Converting a tiny sample app into an atomic skill (`SKILL.md` + `references/quickstart.md`) made the RC workflow reusable.
    - Extracting behavior directly from `Program.cs` (session reuse + `/reset` + `/exit`) produced implementation-accurate guidance.
  - **What failed / pitfalls**:
    - Codex CLI was constrained to `sandbox: read-only`, so it could draft content but not write files.
  - **Decision / rule for next time**:
    - When Codex is read-only, use Codex for analysis/drafting and finalize file writes via OpenClaw file tools, then verify with git diff.
