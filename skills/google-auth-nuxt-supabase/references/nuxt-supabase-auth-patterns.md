# Nuxt 3 + Supabase Auth patterns (PKCE)

## Minimal plugin pattern

- Create a Supabase client plugin (client-only) and provide `$supabase`.
- Create an auth init plugin that:
  - `await $supabase.auth.getSession()` once
  - stores session/user into `useState`
  - subscribes to `onAuthStateChange`

## Middleware pattern

- `middleware/require-auth.ts`:
  - if no user: redirect to `/login?next=<fullPath>`

## Login page pattern

- Reads `next` query.
- Calls `signInWithOAuth({ provider:'google', options:{ redirectTo: <login page with next> } })`.
- After returning from Google redirect, rely on auth init plugin to populate session/user, then `navigateTo(next)`.

## Notes

- Keep auth state and checks on the client.
- Avoid SSR auth hydration complexity unless needed.
