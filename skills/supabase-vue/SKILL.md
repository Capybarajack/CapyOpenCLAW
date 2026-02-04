---
name: supabase-vue
description: Integrate Supabase with Vue 3 / Nuxt (supabase-js v2): client initialization, auth flows, database CRUD/queries, RLS-safe patterns, Storage uploads, Realtime subscriptions, env/runtime config, and local development with Supabase CLI + TypeScript type generation. Use when building Vue/Nuxt features backed by Supabase (Postgres, Auth, Storage, Realtime) or when debugging Supabase integration issues.
---

# Supabase + Vue/Nuxt (practical workflow)

## 0) Mental model (keep this straight)
- **Supabase = Postgres + APIs** (auto-generated) + Auth + Storage + Realtime.
- **Client-side keys are publishable** (anon / publishable). They identify the *app*, not the user.
- **User identity comes from Auth JWT**; database access is enforced with **RLS**.
- **Never** ship `service_role` / secret keys to browser.

If security matters, default to: **RLS ON everywhere** + policies for `anon` / `authenticated`.

## 1) Vue 3 (Vite) quick setup
1. Install:
   - `npm i @supabase/supabase-js`
2. Env (`.env.local`):
   - `VITE_SUPABASE_URL=...`
   - `VITE_SUPABASE_PUBLISHABLE_KEY=...`
3. Create client (singleton):

```ts
// src/lib/supabaseClient.ts
import { createClient } from '@supabase/supabase-js'

export const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL,
  import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY
)
```

## 2) Nuxt (SSR/CSR) recommended pattern

### 2.1 Runtime config
Put in `.env`:
- `SUPABASE_URL=...`
- `SUPABASE_PUBLISHABLE_KEY=...`

In `nuxt.config.ts` expose as public runtime config:
```ts
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      supabaseUrl: process.env.SUPABASE_URL,
      supabasePublishableKey: process.env.SUPABASE_PUBLISHABLE_KEY,
    },
  },
})
```

### 2.2 SSR-aware Auth (cookie-based session)
If you use SSR for authenticated pages/data, don’t rely on localStorage session.
Use `@supabase/ssr`:
- browser client: `createBrowserClient()`
- server client: `createServerClient()` with cookie adapters

See: `references/nuxt-ssr.md`.

### 2.3 Provide a browser client via plugin (single instance)
For CSR usage + Realtime subscriptions.
```ts
// plugins/supabase.client.ts
import { createBrowserClient } from '@supabase/ssr'

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()

  const supabase = createBrowserClient(
    String(config.public.supabaseUrl),
    String(config.public.supabasePublishableKey)
  )

  return { provide: { supabase } }
})

// composables/useSupabase.ts
export const useSupabase = () => useNuxtApp().$supabase
```

## 3) CRUD patterns that play well with RLS
### 3.1 Always filter queries
RLS is an implicit WHERE; still **add filters** to improve plans.

```ts
const { data, error } = await supabase
  .from('todos')
  .select('*')
  .eq('user_id', userId)
```

### 3.2 Prefer server-side for admin operations
If you need cross-user access, do it from:
- server routes / edge functions / backend only
- using a **secret key** (never client)

## 4) Auth essentials (supabase-js v2)
### 4.1 Sign up / sign in
```ts
await supabase.auth.signUp({ email, password })
await supabase.auth.signInWithPassword({ email, password })
await supabase.auth.signOut()
```

### 4.2 Listen to auth changes (wire to app state)
```ts
const { data } = supabase.auth.onAuthStateChange((event, session) => {
  // INITIAL_SESSION / SIGNED_IN / SIGNED_OUT / TOKEN_REFRESHED ...
})
// later: data.subscription.unsubscribe()
```

### 4.3 RLS helper functions
Write policies using:
- `auth.uid()` (current user id)
- `auth.jwt()` (read app_metadata / user_metadata)

See references for policy templates.

## 5) Storage (files)
- Buckets + policies control access.
- Typical flow:
  1) upload
  2) store returned path in a row with RLS
  3) use signed URLs (private) or public URL (public bucket)

## 6) Realtime
- Choose one:
  - **Postgres Changes** (listen to table changes)
  - **Broadcast** (app events)
  - **Presence** (online/participants)

Important: keep subscriptions lifecycle-safe (create on mount, remove on unmount).

## 7) Local development & types
### 7.1 Local stack
```bash
npm i supabase --save-dev
npx supabase init
npx supabase start
# dashboard: http://localhost:54323
```

### 7.2 Generate TypeScript DB types
Cloud project:
```bash
npx supabase gen types typescript --project-id "$PROJECT_REF" --schema public > database.types.ts
```
Local:
```bash
npx supabase gen types typescript --local > database.types.ts
```
Then:
```ts
import type { Database } from './database.types'
const supabase = createClient<Database>(url, key)
```

## 8) Debug checklist
- Wrong key type? (publishable/anon ok, secret/service_role MUST NOT be in browser)
- RLS enabled but no policies → everything denied.
- Policies too broad (anon can read/write) → security issue.
- Missing filters → slow queries even if RLS exists.
- Auth session not persisted where you expect (SSR vs client-only): consider `@supabase/ssr` for cookie-based SSR.

## References (load only when needed)
- `references/vue-quickstart.md`
- `references/nuxt-quickstart.md`
- `references/api-keys-security.md`
- `references/rls-policy-templates.md`
- `references/local-dev-cli.md`
- `references/typescript-types.md`
- `references/auth-ssr-notes.md`
- `references/nuxt-ssr.md`
- `references/storage-notes.md`
- `references/realtime-notes.md`
