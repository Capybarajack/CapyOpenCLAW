# Nuxt quickstart (Supabase)

Source: https://supabase.com/docs/guides/getting-started/quickstarts/nuxtjs

## Minimal setup
- Install: `npm i @supabase/supabase-js`
- Env: `SUPABASE_URL`, `SUPABASE_PUBLISHABLE_KEY`
- Expose via `runtimeConfig.public`.

## Simplest in `app.vue`
```ts
import { createClient } from '@supabase/supabase-js'
const config = useRuntimeConfig()
const supabase = createClient(config.public.supabaseUrl, config.public.supabasePublishableKey)
```

## Recommended improvement
Create a Nuxt plugin to avoid multiple clients + centralize config.
