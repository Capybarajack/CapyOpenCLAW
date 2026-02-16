---
name: spec-kit
description: Use GitHub Spec Kit (Specify CLI + /speckit.* flow) as a practical companion to OpenSpec (OPSX). Use when you want fast spec artifacts, planning prompts, and task breakdowns before or alongside OPSX execution.
---

# Spec Kit (Vendored Upstream)

`spec-kit` is GitHub's open-source toolkit for spec-driven development using the `specify` CLI and `/speckit.*` commands.

Upstream source is vendored at:
- `skills/spec-kit/upstream`

Treat `skills/spec-kit/upstream` as upstream code. Do not hand-edit it unless you are intentionally patching upstream.

## Practical use with OpenSpec (OPSX)

1. If `specify` is not installed yet, install from the vendored upstream:
```bash
uv tool install specify-cli --from ./skills/spec-kit/upstream
```
2. Initialize Spec Kit in your target project:
```bash
specify init --here --ai codex
```
3. Generate artifacts with Spec Kit:
```bash
/speckit.constitution
/speckit.specify
/speckit.plan
/speckit.tasks
```
4. Execute with OPSX:
```bash
/opsx:new <change-name>
/opsx:ff
/opsx:apply
/opsx:verify
/opsx:archive
```

Use Spec Kit to shape requirements and plans; use OPSX to run the full implementation and verification loop.

## Updating vendored upstream

```bash
git subtree pull --prefix=skills/spec-kit/upstream https://github.com/github/spec-kit.git main --squash
```
