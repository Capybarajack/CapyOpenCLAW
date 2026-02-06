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
