# Notes distilled from tdxmotc/SampleCode

Source repo:
- https://github.com/tdxmotc/SampleCode

## Auth (OIDC client_credentials)

All samples use the same token endpoint:
- `https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token`

Request:
- `POST`
- `content-type: application/x-www-form-urlencoded`
- body fields:
  - `grant_type=client_credentials`
  - `client_id=...`
  - `client_secret=...`

## Calling APIs

Samples call a TDX endpoint with:
- `Authorization: Bearer <access_token>`

They also frequently include:
- `Accept-Encoding: br,gzip`

## Compression handling patterns

- **Browser/JS (jQuery)**: sets `Accept-Encoding: br,gzip` and relies on the browser/network stack to decode.
- **Google Apps Script**: uses `UrlFetchApp.fetch` and reads `response.getContentText()` (decoding handled by platform).
- **C#**:
  - Either uses `HttpClientHandler.AutomaticDecompression = Brotli | GZip` (recommended), OR
  - Manually checks `Content-Encoding` and wraps the stream in `BrotliStream` / `GZipStream`.

Practical advice:
- If you control the client and can decode Brotli, request `br,gzip`.
- If not, request `gzip` only (still reduces payload).

## Secret handling

Some samples show placeholders in code. Preferred practice:
- Store `client_id` / `client_secret` in env vars or a secret manager.
- Never commit secrets.

## Rate limits / caching

The SampleCode README warns:
- Token endpoint is rate-limited (commonly 20/min/IP).
- The token has `expires_in` (often 86400 seconds).

Implement token caching (in memory or file) and refresh before expiry.
