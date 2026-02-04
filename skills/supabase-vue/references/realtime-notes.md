# Realtime notes

Source: https://supabase.com/docs/guides/realtime

## Options
- Broadcast: low-latency app events.
- Presence: online/active participants.
- Postgres Changes: listen to DB changes.

## Vue/Nuxt lifecycle rule
- Subscribe on mount.
- Unsubscribe on unmount.
- Avoid duplicating subscriptions across hot reloads/components.
