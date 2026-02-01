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
