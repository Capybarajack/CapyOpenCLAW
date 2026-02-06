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

## Fetch entries with nested items (Dashboard)

```ts
const { data, error } = await supabase
  .from('food_entries')
  .select('id,captured_at,image_bucket,image_path,ai_summary,ai_confidence,total_calories_kcal,total_protein_g,total_carbs_g,total_fat_g,food_entry_items(id,sort_order,name,estimated_portion,calories_kcal,protein_g,carbs_g,fat_g)')
  .eq('user_id', user.id)
  .order('captured_at', { ascending: false })
  .order('sort_order', { foreignTable: 'food_entry_items', ascending: true })

if (error) throw error
```

## Create signed URLs for private Storage objects

```ts
const { data, error } = await supabase.storage
  .from(entry.image_bucket)
  .createSignedUrl(entry.image_path, 60 * 60)

if (error) throw error
const url = data.signedUrl
```

Cache `url` by `entry.id` in a local map to avoid repeated calls.

