---
name: google-auth-nuxt-supabase
description: Implement Google OAuth sign-in in Nuxt 3 using Supabase Auth (PKCE) including callback handling, session persistence, route middleware protection, and common redirect/state pitfalls. Use when adding or debugging Google login/logout flows.
---

# Google OAuth (Nuxt 3 + Supabase Auth) Playbook

## Goal

Enable Google sign-in in a Nuxt 3 SPA using Supabase Auth with PKCE, keep the session stable across redirects, and protect routes with middleware.

## Baseline setup (Nuxt)

- Prefer SPA mode (`ssr:false`) when keeping the auth flow simple.
- Create Supabase client plugin with:
  - `flowType: 'pkce'`
  - `persistSession: true`
  - `autoRefreshToken: true`
  - `detectSessionInUrl: false` (if you handle callback explicitly or if you don’t want Supabase to auto-parse)

## Google provider setup (Supabase)

- Supabase Dashboard → Auth → Providers → Google
- Add **Redirect URLs**:
  - Local: `http://localhost:3000/login` (or your chosen callback page)
  - Prod: `https://<your-domain>/login`
- Ensure the Google Cloud OAuth client has matching Authorized redirect URIs.

## Frontend flow

### 1) Trigger sign-in

Call:
- `supabase.auth.signInWithOAuth({ provider: 'google', options: { redirectTo } })`

Use `redirectTo` pointing to a page that can finalize auth and then navigate to the intended destination.

### 2) Maintain “where to go next”

- Put `next` in query string: `/login?next=/dashboard`
- After auth finishes, navigate to `next`.

### 3) Initialize auth state (single source of truth)

- On app start, call `supabase.auth.getSession()` and store:
  - `session`
  - `user`
- Subscribe to `onAuthStateChange` to keep state in sync.

## Route protection

- Use Nuxt route middleware (kebab-case naming).
  - File: `middleware/require-auth.ts`
  - Usage: `definePageMeta({ middleware: 'require-auth' })`

Middleware checks `useAuthUser()` (or session) and redirects to `/login?next=<path>`.

## Common pitfalls + fixes

- **Unknown route middleware**: Nuxt derives name from filename (kebab-case). Use `require-auth` not `requireAuth`.
- **Login works but user becomes null after redirect**:
  - Ensure `persistSession:true`
  - Ensure you call `getSession()` on startup (plugin)
- **Redirect loop**:
  - Ensure login page does not run require-auth middleware.
  - Ensure `next` defaults safely.
- **Callback not completing**:
  - If `detectSessionInUrl:false`, you must call `supabase.auth.getSession()` after redirect (or handle tokens). In SPA, easiest is to let Supabase parse URL by setting `detectSessionInUrl:true` OR keep false but ensure your auth-init plugin runs on load.

## Debug checklist

- Verify provider redirect URL list in Supabase.
- Confirm the browser has a Supabase session in localStorage.
- Log:
  - `await supabase.auth.getSession()`
  - `await supabase.auth.getUser()`
- Check DevTools → Network for `/auth/v1/token` responses.

## References

- Read `references/nuxt-supabase-auth-patterns.md` when updating the plugin/middleware structure or debugging redirect/session issues.
