---
name: ui-ux-pro-max
description: Generate implementation-ready UI/UX direction for web and app work using local design datasets + Python search scripts. Use when users ask to design/build/review/improve interfaces (landing pages, dashboards, SaaS apps, e-commerce, mobile UI), choose styles/colors/typography, enforce accessibility/performance, or pick stack-specific UI practices (React, Next.js, Vue, Nuxt, Svelte, Tailwind, Flutter, SwiftUI, React Native, Jetpack Compose).
---

# UI/UX Pro Max (OpenClaw Edition)

Use this skill to turn vague UI requests into concrete design-system guidance before coding.

## When to apply

Apply when the user asks things like:
- "幫我做 landing page / dashboard / app UI"
- "這個介面醜，幫我改好看"
- "幫我選配色、字體、風格"
- "幫我做 UI code review / UX 優化"

Do **not** apply for backend-only, infra-only, or non-UI tasks.

## Required workflow

1. **Identify context**
   - Product type (SaaS, fintech, beauty, healthcare, etc.)
   - Goal (conversion, trust, clarity, speed, accessibility)
   - Stack (if missing, default to `html-tailwind`)

2. **Generate design system first (required)**
   - Run:
     ```bash
     python skills/ui-ux-pro-max/scripts/search.py "<product> <industry> <keywords>" --design-system -p "<ProjectName>"
     ```
   - Use the output as the visual source of truth (pattern, style, colors, typography, effects, anti-patterns).

3. **Pull targeted supplements (optional but recommended)**
   - Domain search:
     ```bash
     python skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <style|color|typography|landing|chart|ux|product>
     ```
   - Stack search:
     ```bash
     python skills/ui-ux-pro-max/scripts/search.py "<keyword>" --stack <html-tailwind|react|nextjs|vue|svelte|swiftui|react-native|flutter|shadcn|jetpack-compose>
     ```

4. **Implement/review using these guardrails**
   - Accessibility first (contrast, focus states, keyboard flow, form labels)
   - Interaction quality (44x44 targets, hover/tap feedback, loading/error states)
   - Performance basics (image optimization, reduced motion, avoid layout shift)
   - Consistent system (single style language, coherent spacing/typography)

## Optional persistence mode

When the user wants reusable design rules across sessions:

```bash
python skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "<ProjectName>"
```

Optional page override:

```bash
python skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "<ProjectName>" --page "<page-name>"
```

This creates a hierarchical design-system folder (`MASTER.md` + page overrides).

## Output contract (what to return)

When using this skill, structure your response as:
1. Recommended design system (style + palette + typography + layout pattern)
2. Key UI decisions and anti-patterns to avoid
3. Stack-specific implementation notes
4. A short pre-delivery checklist

## Files in this skill

- `data/` → design knowledge tables
- `scripts/search.py` → search + design-system generator
- `scripts/design_system.py` → composed recommendations
- `templates/` → helper templates from upstream project
