---
name: msagent-openai-chat
description: Build, run, and troubleshoot a .NET 10 Microsoft Agents SDK + OpenAI CLI chatbot with multi-turn session context and `/reset`/`/exit` controls. Use when users ask about HOL_MSAgentFrameworkRC, Microsoft.Agents.AI.OpenAI RC setup, or a session-based console chatbot.
---

# msagent-openai-chat

Use this skill when creating or debugging the console chatbot pattern from `HOL_MSAgentFrameworkRC`.

## What this pattern includes

- .NET console app targeting `net10.0`
- `Microsoft.Agents.AI.OpenAI` (`1.0.0-rc2`)
- OpenAI Responses client using model `gpt-4.1`
- Environment-variable auth via `OPENAI_API_KEY`
- Persistent session for multi-turn context
- Control commands:
  - `/reset`: start a fresh session/context
  - `/exit`: quit app

## Implementation checklist

1. Read API key from `OPENAI_API_KEY`; fail fast if missing.
2. Create agent via `OpenAIClient(...).GetResponsesClient("gpt-4.1").AsAIAgent(...)`.
3. Create one session and reuse it for each turn.
4. Handle `/reset` and `/exit` before calling the model.
5. Wrap `RunAsync(...)` in `try/catch` and print readable error messages.
6. Keep console UTF-8 input/output for Chinese interaction quality.

## Reference

See `references/quickstart.md` for setup, run, reset/exit usage, and troubleshooting.
