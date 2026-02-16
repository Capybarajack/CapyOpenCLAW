# Test Suite Template

Use this template to validate a Claude skill before release.

## A. Trigger tests

### Should trigger

- Prompt 1:
- Prompt 2 (paraphrase):
- Prompt 3 (different wording):

Expected: skill loads automatically.

### Should NOT trigger

- Unrelated prompt 1:
- Unrelated prompt 2:
- Adjacent but out-of-scope prompt:

Expected: skill does not load.

## B. Functional tests

### Happy path

- Input:
- Expected steps:
- Expected output:

### Edge case 1

- Input:
- Expected fallback/validation:

### Edge case 2

- Input:
- Expected fallback/validation:

### Error handling

- Simulated failure:
- Expected recovery:
- Expected user-facing message:

## C. Performance comparison

Run each scenario with and without skill.

Capture:

- Conversation turns
- Tool/API calls
- Failed calls
- Token usage
- Time to completion

Record decision:

- Keep as-is / needs iteration
- Highest-impact change to apply next
