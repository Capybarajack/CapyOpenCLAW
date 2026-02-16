# Troubleshooting Playbook

## 1) Skill fails to upload

Check:

- File is exactly `SKILL.md` (case-sensitive).
- Frontmatter exists and is valid YAML between `---` delimiters.
- `name` uses kebab-case.

## 2) Skill never triggers

Likely issue: description too generic.

Fix:

- Add explicit trigger phrases users actually say.
- State exact scope and outcomes.
- Mention relevant files/formats/services when applicable.

## 3) Skill triggers too often

Likely issue: description too broad.

Fix:

- Tighten scope language.
- Add disambiguation constraints and negative triggers.
- Separate adjacent workflows into different skills.

## 4) Skill triggers but instructions are ignored

Likely issues:

- Critical rules buried too deep.
- Instructions are ambiguous.
- Too much non-procedural prose.

Fix:

- Move critical checks near top.
- Convert vague guidance to explicit pass/fail checks.
- Use scripts for deterministic validations.

## 5) Tool/API failures in workflow

Check:

- Service connection status
- Authentication validity
- Tool name correctness
- Parameter shape and required fields

Fix:

- Add explicit retry/fallback logic where appropriate.
- Add preflight validation before first tool call.
- Improve error messaging with next action.

## 6) Context bloat and degraded responses

Fix:

- Keep SKILL.md short and procedural.
- Move detail to references.
- Reduce simultaneously enabled overlapping skills.
- Avoid duplicate instructions across SKILL.md and references.
