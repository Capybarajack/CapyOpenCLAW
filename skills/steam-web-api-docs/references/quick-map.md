# Steam Web API Quick Map

## Core URL format

`https://api.steampowered.com/{interface}/{method}/v{version}/?key={api_key}&format=json&...`

Notes:
- `format` supports `json`, `xml`, `vdf` (default usually JSON).
- Method versions are per-method (`v1`, `v2`, `v0002`, etc.).

## Practical core interfaces

1. `ISteamUser`
- `GetPlayerSummaries` (player profile/public presence)
- `GetFriendList` (subject to privacy)

2. `IPlayerService`
- `GetOwnedGames`
- `GetRecentlyPlayedGames`

3. `ISteamUserStats`
- Global achievements/stat APIs

4. `ISteamNews`
- `GetNewsForApp`

5. `ISteamApps`
- App/server utility endpoints (`UpToDateCheck`, etc.)

6. `ISteamWebAPIUtil`
- `GetSupportedAPIList` for discoverability and contract introspection

## Verification strategy

- First pass: read provided docs and extract claimed parameters/response fields.
- Second pass: perform real endpoint check with public-safe sample parameters.
- Third pass: report drift (doc says X, endpoint returns Y).

## Common pitfalls

- Hidden/private profile can make user-related calls appear empty.
- Version mismatch: old docs may reference obsolete version formats.
- Some community docs list endpoints with sparse/empty descriptions.
- Anti-bot protections may block scraping certain wiki pages; prefer direct API contract checks.
