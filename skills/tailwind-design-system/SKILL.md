---
name: tailwind-design-system
description: Reuse and adapt the ssengalanto/tailwind-design-system patterns for React + Tailwind UI implementation. Use when users ask to build or refine design-system-style components, tokenized UI foundations, Storybook-style component libraries, or consistent Tailwind-based visual systems from an existing reference codebase.
---

# Tailwind Design System (Reference Skill)

Use this skill when UI work should follow patterns from the bundled upstream project.

## Source bundle

- Upstream snapshot path: `skills/tailwind-design-system/upstream/`
- Key files:
  - `upstream/tailwind.config.js`
  - `upstream/src/` (components + styles)
  - `upstream/.storybook/` (component documentation setup)

## Workflow

1. Identify requested UI scope (component, page section, design token, or full UI system).
2. Read relevant upstream files for matching patterns and naming conventions.
3. Reproduce/adapt patterns in the target project (do not copy blindly; align with target architecture).
4. Keep accessibility and interaction quality (focus, contrast, keyboard, hover/active states).
5. Return:
   - What pattern was reused
   - What was adapted for the target stack/codebase
   - Any intentional deviations

## Boundaries

- Treat upstream as reference, not strict lock-in.
- Prefer small reusable components and consistent Tailwind utilities.
- If target project already has a design system, merge conventions instead of replacing wholesale.
