# Learnings (CapyOpenCLAW)

- **Date**: 2026-02-01
  - **Context**: OpenClaw setup / workflow decision
  - **What worked**:
    - Switching GitHub reads to `raw.githubusercontent.com` avoided GitHub UI rate-limit blocks.
  - **What failed / pitfalls**:
    - Fetching multiple GitHub `blob` pages quickly can trigger GitHub abuse-rate-limits (HTTP 429).
  - **Decision / rule for next time**:
    - Prefer `raw.githubusercontent.com/<org>/<repo>/<branch>/<path>` for docs ingestion.
