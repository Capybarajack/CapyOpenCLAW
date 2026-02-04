# API keys & security notes

Source: https://supabase.com/docs/guides/api/api-keys

## Key types (practical)
- **Publishable / anon**: safe in client apps. Combined with Auth JWT → becomes `authenticated` role.
- **Secret / service_role**: backend-only; bypasses RLS. Never expose.

## Default rules
- Frontend uses publishable/anon key only.
- All DB tables with real data: **RLS enabled**.
- Policies define what `anon` and `authenticated` can do.

## Rotation / leakage
- If a secret/service_role leaks: rotate immediately.
- If publishable leaks: treat as expected; rely on RLS.
