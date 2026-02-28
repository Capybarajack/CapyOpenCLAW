# Quickstart

## Setup

Prerequisites:

- .NET SDK `10.0` or newer (`TargetFramework` is `net10.0`)
- Valid OpenAI API key

Set API key (PowerShell, current session only):

```powershell
$env:OPENAI_API_KEY = "sk-..."
```

Set API key persistently (PowerShell, user env):

```powershell
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-...", "User")
```

After persistent set, open a new terminal.

## Run

From repo root (`HOL_MSAgentFrameworkRC`):

```powershell
dotnet restore
dotnet run
```

You should see a greeting from `HelloBot`, then prompt input.

## Reset Conversation

Type:

```text
/reset
```

Behavior: app creates a new session (`CreateSessionAsync`) and clears prior context.

## Exit

Type:

```text
/exit
```

Behavior: loop ends and app prints goodbye message.

## Troubleshooting

- Missing key error (`請設置 OPENAI_API_KEY 環境變數。`):
  - Set `OPENAI_API_KEY` and rerun.
- SDK mismatch (for `net10.0`, e.g., `NETSDK1045`):
  - Install .NET 10 SDK, or retarget project to installed SDK version.
- NuGet restore failures:
  - Check internet/proxy/TLS access to NuGet and rerun `dotnet restore`.
- OpenAI auth/rate/model errors shown as `[錯誤] ...`:
  - Verify API key validity, billing/quota, and model access for `gpt-4.1`.
- Chinese text appears garbled:
  - Use a UTF-8 capable terminal/font; app already sets `Console.InputEncoding` and `Console.OutputEncoding` to UTF-8.
- Blank input does nothing:
  - Expected behavior; whitespace input is ignored by design.
