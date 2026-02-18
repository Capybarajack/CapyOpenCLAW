---
name: steam-web-api-docs
description: Analyze Steam Web API documentation and turn it into implementation-ready guidance. Use when users share Steam Web API links, ask to extract endpoint parameters/response fields, compare official vs community docs, or request ready-to-run request examples.
---

# Steam Web API Docs Skill

## Use cases

1. **Doc digestion from links**
- Trigger phrases: "幫我讀這份 Steam API 文件", "summarize this Steam Web API page"
- Result: clean summary with endpoint, params, response schema, caveats.

2. **Implementation prep**
- Trigger phrases: "給我可直接用的範例", "I need JS/Python call examples"
- Result: copy/paste request examples + minimal wrapper snippet.

3. **Source reconciliation**
- Trigger phrases: "official 跟社群文件哪個準", "verify this method still works"
- Result: confidence-rated answer with live endpoint sanity checks.

## Execution workflow

1. **Classify source quality**
- Official (steamcommunity.com/dev, api.steampowered.com, partner docs) = primary.
- Community mirrors/aggregators = secondary; use for discoverability only.

2. **Extract method contract**
- Capture: interface, method, version, HTTP method, required/optional params, response envelope.
- Normalize URL pattern:
  - `https://api.steampowered.com/{interface}/{method}/v{version}/?{query}`

3. **Run live sanity check when possible**
- Call the endpoint with safe public params (no user secrets).
- Confirm at least: method reachable, response shape, key field names.
- If blocked by anti-bot pages, explicitly say so and continue with best available sources.

4. **Produce implementation-ready output**
- Always include:
  - What this endpoint is for
  - Required params vs optional params
  - Response schema highlights
  - One working URL example
  - Common pitfalls (privacy, hidden profiles, key scopes, format/version mismatches)

5. **Confidence labeling**
- `High`: official docs + live endpoint check agree.
- `Medium`: live endpoint check only or official docs only.
- `Low`: community-only evidence.

## Output template

Use this structure:

- Endpoint: `{interface}/{method}/v{version}`
- Purpose:
- Required params:
- Optional params:
- Response fields:
- Working example:
- Pitfalls:
- Confidence: High/Medium/Low (+ why)

## Guardrails

- Never expose or echo private API keys.
- Treat community docs as hints, not ground truth.
- Prefer JSON in examples unless user requests XML/VDF.
- If endpoint set is broad, prioritize: `ISteamUser`, `IPlayerService`, `ISteamUserStats`, `ISteamNews`, `ISteamApps`, `ISteamWebAPIUtil`.
