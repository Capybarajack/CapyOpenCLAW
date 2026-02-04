# Vue (Vite) quickstart (Supabase)

Source: https://supabase.com/docs/guides/getting-started/quickstarts/vue

## Minimal setup
- Install: `npm i @supabase/supabase-js`
- Env: `VITE_SUPABASE_URL`, `VITE_SUPABASE_PUBLISHABLE_KEY`
- Create a singleton `supabaseClient.ts` and import it anywhere.

## Typical first query
```ts
const { data, error } = await supabase.from('instruments').select('*')
```

## First RLS policy for public read
```sql
alter table public.instruments enable row level security;
create policy "public can read instruments"
on public.instruments
for select to anon
using (true);
```
