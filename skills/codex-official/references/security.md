# Security / sandbox / approvals (distilled)

Source: https://developers.openai.com/codex/security/

## Two layers
1) **Sandbox mode**: what can happen technically (filesystem/network boundaries)
2) **Approval policy**: when Codex must ask

## Common combinations
- Auto preset: `--full-auto` (workspace-write + approvals on-request)
- Safe browsing: `--sandbox read-only --ask-for-approval on-request`
- CI read-only: `--sandbox read-only --ask-for-approval never`
- Dangerous: `--yolo` / `--sandbox danger-full-access` (avoid unless explicitly requested)

## Config snippets
```toml
approval_policy = "untrusted"
sandbox_mode = "read-only"

[sandbox_workspace_write]
network_access = true

web_search = "cached" # default; treat results as untrusted
# web_search = "disabled"
# web_search = "live"
```

## Prompt injection warning
- Be cautious when enabling network access or live web search.
- Web results can contain malicious instructions.

## Enterprise governance (high level)
- Admins can enforce requirements via requirements.toml (allowed sandboxes/approval policies, restrictive command rules).
- Managed defaults via managed_config.toml set startup defaults but can be changed per-session (reapplied next launch).
