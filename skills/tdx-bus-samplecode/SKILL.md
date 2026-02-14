---
name: tdx-bus-samplecode
description: Use Taiwan TDX (tdx.transportdata.tw) Bus APIs to query bus arrival/ETA and real-time status, following the official tdxmotc/SampleCode patterns (OIDC client_credentials token, Authorization Bearer header, optional Accept-Encoding br/gzip compression, and safe secret handling). Use when integrating TDX auth + making Bus EstimatedTimeOfArrival (ETA/N1), RealTimeByFrequency (A1), or RealTimeNearStop (A2) calls in Python/JS/C# and when you want copy/paste-ready templates.
---

# TDX Bus arrival/status — skill (based on official SampleCode)

This skill distills the official integration patterns from:
- https://github.com/tdxmotc/SampleCode

## Core pattern (all languages)

1) **Get access token** via OIDC client credentials
- POST `https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token`
- `content-type: application/x-www-form-urlencoded`
- body:
  - `grant_type=client_credentials`
  - `client_id=<TDX_CLIENT_ID>`
  - `client_secret=<TDX_CLIENT_SECRET>`

2) **Call API** with bearer token
- Add header: `Authorization: Bearer <access_token>`
- Base server (Basic): `https://tdx.transportdata.tw/api/basic`

3) **(Optional) Enable compression**
- SampleCode sets `Accept-Encoding: br,gzip`.
- If your HTTP client cannot decode Brotli, prefer `gzip` only.

## Bus endpoints you usually want

ETA (N1):
- `GET /v2/Bus/EstimatedTimeOfArrival/City/{City}`

Real-time vehicle dynamic (A1):
- `GET /v2/Bus/RealTimeByFrequency/City/{City}`

Near-stop events (A2):
- `GET /v2/Bus/RealTimeNearStop/City/{City}`

Always append:
- `?$format=JSON`

Common OData helpers (when supported):
- `$top`, `$select`, `$filter`, `$orderby`

## Quick start (curl)

```bash
# 1) token
TOKEN=$(curl -s -X POST \
  'https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -d 'grant_type=client_credentials' \
  -d "client_id=${TDX_CLIENT_ID}" \
  -d "client_secret=${TDX_CLIENT_SECRET}" \
  | python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# 2) ETA example
curl -s -H "authorization: Bearer ${TOKEN}" \
  'https://tdx.transportdata.tw/api/basic/v2/Bus/EstimatedTimeOfArrival/City/NewTaipei?$top=5&$format=JSON'
```

PowerShell note: `$top` is a variable in PowerShell; use single quotes for URLs.

## Reference notes from SampleCode

Read: `references/samplecode-notes.md`.

## Runnable script templates

- Python CLI example: `scripts/tdx_bus.py`
  - Uses env vars `TDX_CLIENT_ID`, `TDX_CLIENT_SECRET`
  - Caches token to avoid hammering the token endpoint

Run:

```bash
py skills/tdx-bus-samplecode/scripts/tdx_bus.py eta-city --city NewTaipei --top 5
```
