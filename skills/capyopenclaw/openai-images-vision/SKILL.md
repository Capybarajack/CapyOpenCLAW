---
name: openai-images-vision
description: Use OpenAI vision (image understanding) and image generation APIs. Use when you need to send images (URL/base64/file id) to the Responses API or Chat Completions API, choose image detail level (low/high/auto), estimate image token costs, or handle common vision limitations.
---

# OpenAI Images & Vision (Reusable Playbook)

## Use the right API

- **Analyze images (most common):** use **Responses API**.
- **Generate/edit images:** use **Responses API** (tool `image_generation`) or **Images API**.
- **Legacy/compat:** Chat Completions can also accept images, but prefer Responses for new work.

## Canonical request pattern (Responses API)

Send image(s) in the `content` array with `type: "input_image"`.

- URL image:
  - `{"type":"input_image","image_url":"https://..."}`
- Base64 data URL:
  - `{"type":"input_image","image_url":"data:image/png;base64,..."}`
- File id:
  - `{"type":"input_image","file_id":"file_..."}`

Also include a text instruction:
- `{"type":"input_text","text":"..."}`

Read: `references/vision-guide.md` for exact examples + constraints.

## Detail level

Set `detail` on each `input_image`:
- `low` → faster/cheaper, good for coarse questions
- `high` → more detail, higher cost
- `auto` (default)

## Cost / token estimation

Rules differ by model families. Use the scripts when you need quick estimates:

- Node: `node scripts/estimate-image-tokens.js --model gpt-4.1-mini --width 1024 --height 1024`
- Node: `node scripts/estimate-image-tokens.js --model gpt-4o --detail high --width 1024 --height 1024`

(See `references/vision-guide.md` → “Calculating costs”.)

## Utilities

Create Base64 data URL from a local image:
- `node scripts/image-to-data-url.js path/to/image.jpg`

## Quality / reliability checklist

- If text is small: ask user for higher-res / zoomed image (avoid cropping key context).
- If rotated: rotate upright before sending.
- For multi-image comparisons: include multiple `input_image` items + explicit per-image labels in your text.
- Avoid medical diagnosis; call out limitations when relevant.
