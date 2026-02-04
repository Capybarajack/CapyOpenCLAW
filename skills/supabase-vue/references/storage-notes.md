# Storage notes

Source: https://supabase.com/docs/guides/storage

## Practical guidance
- Decide bucket type: typically **Files bucket** for app uploads.
- Access control: bucket policies + DB rows with RLS.
- Prefer storing file metadata/path in a table (RLS protected).
- For private files: use signed URLs.
