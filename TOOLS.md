# TOOLS.md — Local Environment Notes

Use this file as a **machine-specific cheat sheet**.
Put only local facts here (not general skill docs).

## Quick Rules

- Keep entries short and actionable
- Prefer stable identifiers over descriptions
- Update immediately after environment changes
- Never store secrets in plain text

---

## SSH Hosts

- `home-server` → host: `<ip-or-domain>`, user: `<user>`, auth: `<key/passwordless>`
- `vps-main` → host: `<ip-or-domain>`, user: `<user>`, notes: `<port/alias>`

## Devices / Cameras

- `living-room-cam` → id: `<device-id>`, location: `living room`
- `front-door-cam` → id: `<device-id>`, location: `front door`

## TTS / Audio

- provider: `<provider>`
- preferred voice: `<voice-name-or-id>`
- default output target: `<speaker/device>`

## OpenClaw Runtime Preferences

- preferred model: `openai-codex/gpt-5.3-codex`
- coding execution style: `small steps (<=8 min), report change/verify/next`

## Repo Shortcuts

- main workspace: `C:\Users\asdfg\.openclaw\workspace`
- Star-Office-UI (active path): `F:\openClaw\Star-Office-UI`

## Known Local Quirks

- PowerShell doesn’t support bash-style `<` redirection
- For Nuxt/Vite client checks, prefer `import.meta.client`

---

Last updated: 2026-03-13