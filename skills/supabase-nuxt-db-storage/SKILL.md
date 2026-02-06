---
name: supabase-nuxt-db-storage
description: Implement and debug Supabase in Nuxt 3 with supabase-js v2, including Storage upload paths, Storage RLS policies, DB RLS policies, and inserting parent/child rows (entries + items). Use when wiring image upload + analysis persistence to Supabase.
---

# Supabase (Nuxt 3) DB + Storage Playbook

## Goal

Upload meal photos to Supabase Storage and persist analysis results into Supabase tables using supabase-js v2.

## Storage: buckets + path conventions

### Recommended key pattern

Use a per-user top-level folder:

- bucket: `meal-photos`
- object key: `<uid>/<uuid>.<ext>`

This enables simple policies using `storage.foldername(name)[1]`.

### Upload checklist

- Bucket should be **Private**.
- Upload using the authenticated client.
- Store these references in your app state (and DB):
  - `storageBucket`
  - `storagePath`
  - `mimeType`, `fileName`, `fileSize`

## Storage policies (RLS on storage.objects)

Create policies that allow users to access only their own top-level folder named as uid.

Core condition:

```sql
bucket_id = 'meal-photos'
AND storage.foldername(name)[1] = auth.uid()::text
```

Apply to operations: SELECT/INSERT/UPDATE/DELETE with role `authenticated`.

## DB: inserting entry + items (parent/child)

### Pattern

1) Insert parent row and return `id`.
2) Insert children rows referencing the parent.

Example:

- Insert into `food_entries` with `user_id`, `image_bucket`, `image_path`, totals, `result_json`, `raw_text`.
- Then insert into `food_entry_items` with `entry_id` + `user_id`.

## Dashboard: load from DB when logged in; fallback to localStorage when logged out

### Why

- Logged-in users expect their history to be durable and synced.
- Logged-out users can still use a lightweight local demo using localStorage.

### Implementation notes (Nuxt 3)

- Do **not** force auth middleware on the dashboard route.
- Determine mode with `useAuthUser()`:
  - If `user?.id` exists: fetch from DB.
  - Else: `useUploadLog().load()` and render localStorage logs.

### Fetching entries + items

- Query `food_entries` filtered by `user_id`.
- Order by `captured_at desc`.
- Include related `food_entry_items` and order items by `sort_order asc`.

### Showing private images

Buckets are private. To render images in the dashboard, generate signed URLs:

- `supabase.storage.from(image_bucket).createSignedUrl(image_path, expiresInSeconds)`

Cache signed URLs in memory (map by `entry.id`) to avoid regenerating them every render.

### Refresh triggers

Refresh data on:

- route change (e.g. watch `route.fullPath`)
- auth change (e.g. watch `user.id`)

## DB RLS policies (tables)

If you insert from the frontend, you must have RLS policies for `authenticated`.

Typical policy patterns:

- `food_entries`: allow INSERT/SELECT/UPDATE/DELETE where `user_id = auth.uid()`
- `food_entry_items`: allow INSERT/SELECT where `user_id = auth.uid()`
  - Optional hardening: ensure `entry_id` belongs to the same user.

## Debug checklist (when “DB is empty”)

- Confirm the app actually calls `.from('<table>').insert(...)`.
- In DevTools → Network, check requests to `rest/v1/...`.
- Log returned `{ data, error }` and throw on error.
- If you see 401/403:
  - verify user session exists
  - verify RLS policies exist for INSERT

## References

- Read `references/rls-snippets.md` when creating policies for DB + Storage.
- Read `references/nuxt-supabase-insert-patterns.md` for minimal insert examples.
