---
name: markitdown
description: Convert files and URLs into Markdown using Microsoft MarkItDown (CLI or Python API). Use when extracting text/structure from PDFs, Office files, images, audio, HTML, CSV/JSON/XML, ZIP bundles, EPUB, or YouTube content for LLM ingestion, summarization, indexing, or downstream analysis.
---

# MarkItDown

Use this skill to convert source content into Markdown for LLM workflows.

## Preferred workflow

1. Ensure Python 3.10+ is available.
2. Install MarkItDown in the active environment:
   - Minimal: `pip install markitdown`
   - Full format support: `pip install "markitdown[all]"`
3. Convert with CLI or Python API.
4. Save output to `.md` and continue downstream analysis.

## CLI usage

Convert a file and print to stdout:

```bash
markitdown path-to-file.pdf > output.md
```

Write directly to output file:

```bash
markitdown path-to-file.pdf -o output.md
```

Pipe binary input:

```bash
cat path-to-file.pdf | markitdown > output.md
```

List plugins:

```bash
markitdown --list-plugins
```

Enable plugins for conversion:

```bash
markitdown --use-plugins path-to-file.pdf -o output.md
```

## Python API usage

```python
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False)
result = md.convert("input.pdf")
print(result.text_content)
```

## Optional dependency groups

Install only needed format groups when `all` is unnecessary:

- `pptx`, `docx`, `xlsx`, `xls`, `pdf`, `outlook`
- `az-doc-intel`
- `audio-transcription`, `youtube-transcription`

Example:

```bash
pip install "markitdown[pdf,docx,pptx]"
```

## Notes

- If conversion quality is low, retry with relevant optional dependency groups.
- For Azure Document Intelligence mode, pass endpoint via CLI/API as documented in upstream README.
- For image-description workflows with LLMs, provide `llm_client` and `llm_model` to `MarkItDown`.

## Upstream

- Repo: `https://github.com/microsoft/markitdown`
- Local source included in this skill folder for reference and updates.
