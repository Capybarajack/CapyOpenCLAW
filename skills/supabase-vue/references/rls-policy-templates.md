# RLS policy templates (Supabase Postgres)

Source: https://supabase.com/docs/guides/database/postgres/row-level-security

## Enable RLS
```sql
alter table public.<table> enable row level security;
```

## Ownership-based policies
### SELECT own rows
```sql
create policy "read own"
on public.todos
for select
to authenticated
using ((select auth.uid()) = user_id);
```

### INSERT own rows
```sql
create policy "insert own"
on public.todos
for insert
to authenticated
with check ((select auth.uid()) = user_id);
```

### UPDATE own rows
```sql
create policy "update own"
on public.todos
for update
to authenticated
using ((select auth.uid()) = user_id)
with check ((select auth.uid()) = user_id);
```

### DELETE own rows
```sql
create policy "delete own"
on public.todos
for delete
to authenticated
using ((select auth.uid()) = user_id);
```

## Performance tips
- Add indexes for columns used in policies (e.g. `user_id`).
- Wrap helper functions in `select` to avoid per-row execution:
  - `(select auth.uid()) = user_id`
