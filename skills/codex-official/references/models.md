# Models (distilled)

Source: https://developers.openai.com/codex/models/

Recommended:
- `gpt-5.2-codex`
- `gpt-5.1-codex-mini`

Change model:
- Start: `codex -m <model>`
- Non-interactive: `codex exec -m <model> "..."`

Default model set in `~/.codex/config.toml`:
```toml
model = "gpt-5.2"
```

Note: Chat Completions API support is deprecated in Codex and will be removed in future releases.
