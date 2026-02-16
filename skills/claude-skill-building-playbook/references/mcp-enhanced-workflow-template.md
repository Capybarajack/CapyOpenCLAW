# MCP-Enhanced Workflow Template

Use this template when a skill must orchestrate one or more MCP services.

## 1) Workflow definition

- Business outcome:
- Primary MCP service:
- Secondary MCP services (if any):
- Required user inputs:
- Expected final artifacts:

## 2) Preflight checks

Run these checks before first MCP call:

1. Confirm each MCP connection is active.
2. Confirm auth/token validity for each service.
3. Confirm required permissions/scopes.
4. Confirm required input fields are present and valid.

If any check fails, stop and provide recovery guidance.

## 3) Phased orchestration design

Design phases with explicit handoff data:

- Phase 1 (source retrieval)
  - MCP tool calls:
  - Output schema passed forward:

- Phase 2 (transformation/decision)
  - MCP tool calls:
  - Validation rules:
  - Output schema passed forward:

- Phase 3 (target write/update)
  - MCP tool calls:
  - Idempotency strategy:

- Phase 4 (notification/audit)
  - MCP tool calls:
  - User confirmation payload:

## 4) Error handling policy

For each phase define:

- Common failure modes:
- Retry policy:
- Fallback behavior:
- Rollback behavior (if write operations already executed):
- User-facing error message format:

## 5) Deterministic guardrails

Use scripts for fragile checks where possible:

- Input schema validation script
- Cross-service ID mapping check script
- Final consistency/audit script

Document script usage in SKILL.md with exact command examples.

## 6) Triggering guidance for frontmatter description

Include:

- Outcome-driven triggers users say ("set up sprint from design handoff").
- Service-specific triggers ("sync Figma assets to Linear tickets").
- Scope boundaries and negative triggers (what this skill should not handle).

## 7) Test matrix (MCP-focused)

### Trigger tests
- Should trigger for outcome and service phrase variants.
- Should not trigger for unrelated single-service tasks.

### Functional tests
- Happy path across all phases.
- Service-A failure before writes.
- Service-B failure after partial writes.
- Permission-denied scenario.
- Rate-limit scenario.

### Reliability tests
- Re-run same request (idempotency).
- Partial rerun from failed phase.
- High-latency tool responses.

## 8) Performance metrics

Capture and compare:

- Calls per MCP service
- Total failed calls
- Completion time
- Token usage
- User clarification turns

Set release thresholds before publishing updates.
