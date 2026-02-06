# Nuxt 3 + supabase-js v2 insert patterns

## Insert parent and return id

```ts
const { data: entry, error } = await supabase
  .from('food_entries')
  .insert(payload)
  .select('id')
  .single()

if (error) throw error
```

## Insert child rows

```ts
const { error } = await supabase
  .from('food_entry_items')
  .insert(items.map((it, idx) => ({
    entry_id: entry.id,
    user_id: user.id,
    sort_order: idx,
    ...it,
  })))

if (error) throw error
```

## Always surface errors

Do not ignore the `{ error }` return. Throw it and show in UI.
