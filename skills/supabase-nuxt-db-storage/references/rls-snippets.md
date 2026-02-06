# RLS snippets (Supabase)

## Storage (storage.objects)

Own-folder access for bucket `meal-photos`:

```sql
bucket_id = 'meal-photos'
AND storage.foldername(name)[1] = auth.uid()::text
```

## DB: food_entries

Allow INSERT for owner:

```sql
create policy "insert own entries"
on public.food_entries
for insert
to authenticated
with check (user_id = auth.uid());
```

Allow SELECT for owner:

```sql
create policy "select own entries"
on public.food_entries
for select
to authenticated
using (user_id = auth.uid());
```

## DB: food_entry_items

Allow INSERT for owner:

```sql
create policy "insert own entry items"
on public.food_entry_items
for insert
to authenticated
with check (user_id = auth.uid());
```

Allow SELECT for owner:

```sql
create policy "select own entry items"
on public.food_entry_items
for select
to authenticated
using (user_id = auth.uid());
```

## Dashboard read checklist

If dashboard shows DB errors (401/403) or images fail to render:

- DB SELECT RLS must allow authenticated users to select their own `food_entries` and `food_entry_items`.
- Storage SELECT policy must allow reading objects under `<uid>/...` for the bucket.
- If using signed URLs:
  - the client still needs Storage SELECT permission for the object.

## Optional hardening (items must match entry owner)

```sql
with check (
  user_id = auth.uid()
  and exists (
    select 1
    from public.food_entries e
    where e.id = entry_id
      and e.user_id = auth.uid()
  )
);
```
