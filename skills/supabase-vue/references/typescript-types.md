# TypeScript type generation

Source: https://supabase.com/docs/guides/api/rest/generating-types

## Generate
Cloud:
```bash
npx supabase gen types typescript --project-id "$PROJECT_REF" --schema public > database.types.ts
```
Local:
```bash
npx supabase gen types typescript --local > database.types.ts
```

## Use in supabase-js
```ts
import { createClient } from '@supabase/supabase-js'
import type { Database } from './database.types'

export const supabase = createClient<Database>(url, key)
```

## Tip
If view types are too nullable, merge overrides with `type-fest`'s `MergeDeep`.
