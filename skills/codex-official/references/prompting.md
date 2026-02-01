# Prompting (distilled)

Source: https://developers.openai.com/codex/prompting/

## High-yield prompting rules
- Ask for a plan when scope is unclear.
- Provide verification steps (repro, tests, lint, pre-commit).
- Break large work into smaller steps.
- Avoid two threads editing the same files.

## Thread concept
- A thread is the running session: prompt + tool calls.
- Threads can be local (sandboxed) or cloud (isolated env).
- Codex may compact context on long runs.
