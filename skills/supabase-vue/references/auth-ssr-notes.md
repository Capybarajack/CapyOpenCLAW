# Auth + SSR notes

Source: https://supabase.com/docs/guides/auth/server-side/creating-a-client

## When you need this
- If you do SSR (Nuxt server-rendered pages) and need auth session in server code.

## The idea
- Browser client vs server client need different session storage.
- Cookie-based session management avoids losing auth on SSR.

## Tooling
- `@supabase/supabase-js`
- `@supabase/ssr`

(Implementation differs by framework; treat the Supabase SSR guide as the reference point.)
