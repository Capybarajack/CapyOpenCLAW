# Nuxt SSR/CSR setup notes (Supabase Auth)

## Why you need a special setup
In SSR frameworks (Nuxt SSR pages / server routes), Supabase Auth must store the session in **cookies** (not localStorage), so that:
- Server-side code can read the session.
- Token refresh can be persisted back to the browser.

Supabase recommends using **`@supabase/ssr`** (beta):
- `createBrowserClient()` in browser
- `createServerClient()` on server

Sources:
- https://supabase.com/docs/guides/auth/server-side
- https://supabase.com/docs/guides/auth/server-side/creating-a-client
- https://www.npmjs.com/package/@supabase/ssr

## Package install
```bash
npm i @supabase/supabase-js @supabase/ssr
```

## Nuxt pattern (practical)
### 1) Client plugin
Create a single browser client and provide it.

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
```

### 2) Server utility (per-request)
On the server, create a client per-request, wired to Nuxt/H3 cookies.

```ts
// server/utils/supabaseServerClient.ts
import { createServerClient } from '@supabase/ssr'
import type { H3Event } from 'h3'

export function createSupabaseServerClient(event: H3Event) {
  const config = useRuntimeConfig()

  return createServerClient(
    String(config.public.supabaseUrl),
    String(config.public.supabasePublishableKey),
    {
      cookies: {
        get(name: string) {
          return getCookie(event, name)
        },
        set(name: string, value: string, options: any) {
          setCookie(event, name, value, options)
        },
        remove(name: string, options: any) {
          setCookie(event, name, '', { ...options, maxAge: 0 })
        },
      },
    }
  )
}
```

Then inside any `/server/api/*.ts`:
```ts
export default defineEventHandler(async (event) => {
  const supabase = createSupabaseServerClient(event)
  const { data: { user } } = await supabase.auth.getUser()
  // ...
})
```

### 3) When to call Supabase on server vs client
- SSR page data (useAsyncData), protected pages, server-only aggregation: **server client**
- Realtime subscriptions, UI interactions: **browser client**

## Common pitfalls
- Using `@supabase/supabase-js` directly in SSR without cookie wiring → session seems "missing" on server.
- Accidentally creating many clients → duplicated subscriptions & token refresh weirdness.
- Expecting publishable key to secure data → it does not; **RLS does**.

## Rule of thumb
If you rely on SSR for authenticated data: adopt `@supabase/ssr` early to avoid refactors.
