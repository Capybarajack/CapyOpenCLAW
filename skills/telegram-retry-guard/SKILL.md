---
name: telegram-retry-guard
description: Stabilize Telegram reliability in OpenClaw with a strict 3-attempt retry policy. Use when Telegram send/receive intermittently fails, when logs show `sendMessage failed` or `fetch failed`, or when you need to enforce and verify retry-up-to-3 behavior.
---

# Telegram Retry Guard (3 attempts)

Enforce and operate Telegram message reliability with **max 3 attempts**.

## Scope

- **Outbound (OpenClaw -> Telegram):** enforce provider retry config with `attempts: 3`.
- **Inbound (Telegram -> OpenClaw):** there is no per-message replay API in OpenClaw, so apply a **3-cycle recovery check** and request up to 3 resend attempts from the user when needed.

## Outbound policy (must be 3)

Use config:

```json5
{
  channels: {
    telegram: {
      retry: {
        attempts: 3,
        minDelayMs: 400,
        maxDelayMs: 30000,
        jitter: 0.1
      }
    }
  }
}
```

If not set or mismatched, patch config to this policy, then restart gateway.

## Inbound recovery policy (3 cycles)

When user reports “Telegram message not received by OpenClaw”, run up to **3 cycles**:

1. Check `openclaw status --deep` (Telegram channel/account health).
2. Scan recent logs for `fetch failed`, `sendMessage failed`, transport reset/timeout.
3. Ask user to send a probe text (`PING-1`, `PING-2`, `PING-3`) and verify arrival.
4. If failed in this cycle, wait briefly and continue next cycle.
5. If still failing after cycle 3, restart gateway and report root-cause candidates.

## Standard diagnostic commands (read-only)

```bash
openclaw status --deep
openclaw logs --limit 300 --plain
```

Windows network spot-checks:

```powershell
Test-NetConnection api.telegram.org -Port 443
1..6 | % { try { (Invoke-WebRequest https://api.telegram.org -Method Head -TimeoutSec 8 -UseBasicParsing).StatusCode } catch { $_.Exception.Message }; Start-Sleep -Milliseconds 700 }
```

## Common root causes and mitigations

1. **Transient egress failure** (most common): keep retry=3, observe if self-recovers.
2. **IPv6 path unstable**: set `channels.telegram.network.autoSelectFamily: false` to prefer safer behavior on affected hosts.
3. **Proxy/VPN/firewall intermittency**: verify no unstable outbound filter for `api.telegram.org:443`.
4. **Host DNS jitter**: verify repeated DNS resolution stability.

## Response template

When finishing a run, report:

- Outbound retry policy state (pass/fail; expected 3)
- Inbound probe results (`PING-1..3`)
- Whether restart was required
- Current Telegram health (`status --deep`)
- Next action (monitor / restart / network fix)

## Guardrails

- Do not claim inbound Telegram messages can be replayed exactly by OpenClaw.
- Do not change config or restart gateway without explicit user approval.
- Keep retries capped at 3 (do not silently exceed).
