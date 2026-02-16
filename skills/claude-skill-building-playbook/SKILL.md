---
name: claude-skill-building-playbook
description: Design, write, test, and iterate Claude Agent Skills with reliable triggering and low token overhead. Use when creating a new skill, refining an existing SKILL.md, fixing over/under-triggering, defining skill success metrics, or packaging/distributing skill folders.
---

# Claude Skill Building Playbook

Create robust Claude skills by following this workflow:

1. Define concrete use cases before writing files.
2. Write high-signal frontmatter (name + description) for correct triggering.
3. Keep SKILL.md focused on execution; move heavy detail to references.
4. Test triggering, functional behavior, and performance against a baseline.
5. Iterate based on observed under/over-triggering and execution failures.

## 1) Define the use cases first

Define 2-3 concrete workflows using this template:

- Use case:
- Trigger phrases users actually say:
- Required steps:
- Required tools/services:
- Expected final result:

Reject vague goals. Require explicit user intent and observable output.

## 2) Write frontmatter that triggers correctly

Use only this minimal schema:

```yaml
---
name: skill-name-in-kebab-case
description: What the skill does and when to use it, including concrete trigger phrases.
---
```

Apply strict rules:

- Use kebab-case for `name`.
- Keep `description` under 1024 characters.
- Include both:
  - task scope (what it does)
  - trigger conditions (when to use it)
- Include realistic trigger phrases users might type.
- Avoid vague language (for example: "helps with projects").
- Do not use XML angle brackets in frontmatter.

## 3) Structure the skill for progressive disclosure

Keep SKILL.md concise and procedural.

- Put critical execution steps in SKILL.md.
- Put extended detail in `references/`.
- Put deterministic logic in `scripts/` when language-only instructions are fragile.
- Put templates/boilerplate in `assets/` when outputs need consistency.

Directory pattern:

```text
skill-name/
├── SKILL.md
├── scripts/        (optional)
├── references/     (optional)
└── assets/         (optional)
```

## 4) Use durable workflow patterns

Select one or more patterns:

- Sequential workflow orchestration: fixed order, explicit step dependencies.
- Multi-service coordination: phase-by-phase handoff across services.
- Iterative refinement: draft -> validate -> fix loop until quality threshold.
- Context-aware tool selection: choose tool path using decision rules.
- Domain-specific governance: apply compliance/business rules before action.

## 5) Define success criteria before testing

Track quantitative and qualitative outcomes.

Quantitative targets (adjust per domain):

- Trigger accuracy on relevant prompts (target around 90%).
- Workflow completion in fewer turns/tool calls than baseline.
- API/tool failure rate near zero during standard workflow.
- Token usage lower than prompt-only baseline.

Qualitative checks:

- User does not need to repeatedly re-explain next steps.
- Output structure is consistent across repeated runs.
- New user can complete the workflow on first attempt.

## 6) Run the testing loop

Run in this order:

1. Trigger tests (should trigger / should not trigger).
2. Functional tests (correct outputs, edge cases, error handling).
3. Performance comparison (with-skill vs without-skill).

Use `references/test-suite-template.md` for reusable cases.

## 7) Troubleshoot systematically

When behavior is wrong, inspect in this order:

1. Upload/format correctness (SKILL.md naming, YAML validity).
2. Trigger quality (`description` specificity, trigger phrase coverage).
3. Scope boundaries (add negative triggers to avoid over-triggering).
4. Instruction quality (move ambiguous prose to explicit checks).
5. Tool connectivity and auth (if external tools/services are involved).

Use `references/troubleshooting-playbook.md`.

## 8) Iteration rules

After each real usage cycle:

1. Capture failure mode or friction point.
2. Decide whether fix belongs in frontmatter, SKILL.md, scripts, or references.
3. Update the smallest correct layer.
4. Re-run the same failing case and confirm improvement.
5. Keep only proven instructions; remove speculative guidance.

## 9) Packaging and distribution checklist

Before distribution:

- Verify folder name and SKILL.md naming rules.
- Verify frontmatter quality and trigger clarity.
- Verify trigger + functional + performance tests pass.
- Zip only the skill folder contents.

After distribution:

- Monitor under/over-triggering signals.
- Collect user feedback and iteration requests.
- Re-test before each update.
