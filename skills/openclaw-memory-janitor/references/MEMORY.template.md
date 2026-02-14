# MEMORY.md — Hot Memory (keep ≤ 200 lines)

**Purpose:** fast, high-signal memory that can be loaded every main-session turn.

**Format rules**
- Each bullet should be one idea (prefer single-line bullets).
- Prefix with a priority tag: **[P0] [P1] [P2]**
- For **P1/P2**, include a timestamp: **[ts:YYYY-MM-DD]** (last confirmed relevant).
- Expiry policy (enforced by `memory-janitor.py`):
  - **P0**: never expires
  - **P1**: expires after **90 days**
  - **P2**: expires after **30 days**
- Expired P1/P2 items are moved to: `memory/archive/` (cold memory; still searchable).

---

## [P0] Core identity (never expires)
- [P0] ...

## [P0] Working style / conventions
- [P0] ...

## [P1] Active projects (90d)
- [P1][ts:YYYY-MM-DD] ...

## [P2] Temporary (30d)
- [P2][ts:YYYY-MM-DD] ...
