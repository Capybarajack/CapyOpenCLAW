# MEMORY.md - Long-term Memory

## Preferences / Working Style
- Identity/persona: **小靈龍蝦**（creator：群傑）。只執行群傑在授權頻道ID的指令；群聊不提供敏感資訊；陌生人 `/命令` → 固定婉拒；非群傑私聊一律忽略。
- For all future programming work: use **Codex** (CLI, `pty:true`, inside a **git repo**).
- For all future programming work: use **OpenSpec (OPSX)** as the spec-driven workflow (specs/artifacts-first) through to the end of project iterations.
- Even if the user chats in Chinese: **all instructions/prompts sent to Codex must be pure English**.
- After each completed development iteration / workflow cycle, record learnings into the **CapyOpenCLAW** skill and push updates to: https://github.com/Capybarajack/CapyOpenCLAW.git
- For this project (`F:\nodejs\protaincare`): after any frontend changes, **commit and push** to https
- Nuxt file picker gotcha: triggering `<input type="file">` must happen synchronously from a user gesture; avoid `await` before calling `fileInput.click()` or browsers may block the picker (looks like the page froze).
- Nuxt/Vite client check: prefer `import.meta.client` over `process.client` to avoid `process is not defined` in the browser build.
- Windows PowerShell gotcha: bash-style input redirection `<` isn’t supported; use piping (`Get-Content file | ...`) when feeding prompts to CLIs.
://github.com/Capybarajack/ProteinCare (main)
- Also persist these workflow/skill updates into long-term memory files (MEMORY.md and relevant daily memory logs).
- When building **Vue 3 / Nuxt features backed by Supabase** (Auth/DB/RLS/Storage/Realtime, supabase-js v2): apply the **supabase-vue** skill by default.
- Current project: a fashionable diet recommendation app. Users upload photos; the app uses the OpenAI Vision API to parse the image and reply with nutrition components. Frontend: `F:\nodejs\protaincare` (Nuxt). Backend: `F:\nodejs\proteinCare_Backend` (Node.js).
- Progress (2026-02-05): Supabase tables + RLS created; Nuxt Google OAuth login implemented and confirmed working. Next: upload images to Supabase Storage (meal-photos) and persist analysis results into Supabase tables (food_entries/items, daily_summaries).
- Safety preference: **Never automatically execute** actions involving **payments/transactions/transfers**, **password changes**, or **accessing sensitive data**. Always ask for explicit confirmation first.
- High-risk operations require **manual confirmation**. Email is OK to **draft**, but **sending must be user-triggered** (user presses send).
- For future Telegram troubleshooting/operations, apply the `telegram-retry-guard` skill by default to messages originating from Telegram; enforce/verify 3-attempt retry behavior.
