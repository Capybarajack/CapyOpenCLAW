# Images & Vision — OpenAI API (Reference)

Source: https://platform.openai.com/docs/guides/images-vision

## Contents

- Overview / APIs
- Analyze images (input formats)
- Image input requirements
- Detail level (low/high/auto)
- Limitations
- Calculating costs (token formulas)
- Minimal code examples (Python + JS)

## Overview / APIs

OpenAI supports multimodal workflows:

- **Responses API**: analyze images as input; can also generate images as output (via tools)
- **Images API**: generate images as output, optionally using images as input
- **Chat Completions API**: can analyze images, but Responses is preferred for new work

## Analyze images (input formats)

You can provide images as input via:

1) **URL** (`image_url` is a fully-qualified URL)
2) **Base64 data URL** (`image_url` begins with `data:image/...;base64,`) 
3) **File ID** (`file_id` from Files API)

You can include **multiple images** in one request by adding multiple `input_image` items in the same `content` array.

### Responses API (URL) — Python example

```py
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
  model="gpt-4.1-mini",
  input=[{
    "role": "user",
    "content": [
      {"type": "input_text", "text": "what's in this image?"},
      {"type": "input_image", "image_url": "https://.../image.jpg"}
    ]
  }]
)

print(response.output_text)
```

### Detail parameter

```json
{
  "type": "input_image",
  "image_url": "https://.../image.jpg",
  "detail": "high"
}
```

- `low`: model receives a 512×512 low-res representation; costs a fixed small budget for some model families.
- `high`: more detailed processing; higher token cost.
- `auto`: default.

## Image input requirements

Supported file types:
- PNG
- JPEG (.jpeg/.jpg)
- WEBP
- Non-animated GIF

Size limits:
- Up to **50 MB total payload** per request
- Up to **500 images** per request

Other requirements:
- No watermarks/logos
- No NSFW content
- Must be clear enough for a human to understand

## Limitations (high level)

Known limitations called out in the docs:

- Not suitable for specialized medical image interpretation (no medical advice)
- Non-English text (non‑Latin alphabets) may be weaker
- Small text → enlarge / improve readability, avoid cropping key details
- Rotation can cause misinterpretation
- Some charts/graphs (style/color/dashed) can be hard
- Precise spatial localization is weak (e.g., chess positions)
- Can hallucinate / be inaccurate; verify if critical
- Panoramic/fisheye images can be difficult
- Metadata/filenames are not processed; images are resized before analysis
- Counting objects may be approximate
- CAPTCHA inputs are blocked

## Calculating costs (token rules)

Image inputs are metered in **tokens**.

### GPT‑4.1‑mini / GPT‑4.1‑nano / o4‑mini

Token cost is based on **32×32 patches** with a cap:

A) raw patches:

`raw_patches = ceil(width/32) × ceil(height/32)`

B) if `raw_patches > 1536`, scale down to fit ≤ 1536 patches (preserve aspect ratio; then adjust to whole patches).

C) patches after resizing:

`image_tokens = ceil(resized_width/32) × ceil(resized_height/32)` (capped at 1536)

D) multiply by model family multiplier:

- gpt-5-mini: 1.62
- gpt-5-nano: 2.46
- gpt-4.1-mini: 1.62
- gpt-4.1-nano: 2.46
- o4-mini: 1.72

### GPT‑4o / GPT‑4.1 / GPT‑4o‑mini / CUA / o‑series (except o4‑mini)

Token cost depends on **detail**:

- `detail: low`: fixed base tokens per image (model-dependent)
- `detail: high`:
  1) scale to fit in 2048×2048
  2) scale so shortest side = 768
  3) count number of 512×512 tiles → each tile costs `tile_tokens`
  4) add `base_tokens`

Chart from docs (example values):

- gpt‑5 / gpt‑5‑chat‑latest: base 70, tile 140
- 4o / 4.1 / 4.5: base 85, tile 170
- 4o‑mini: base 2833, tile 5667
- o1 / o1‑pro / o3: base 75, tile 150
- computer-use-preview: base 65, tile 129

### GPT Image 1

Similar to above, but shortest side target is **512px** instead of 768px, plus extra tokens depending on input fidelity and aspect ratio.

## Minimal JS example (Responses)

```js
import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

const resp = await client.responses.create({
  model: "gpt-4.1-mini",
  input: [{
    role: "user",
    content: [
      { type: "input_text", text: "Describe the image briefly." },
      { type: "input_image", image_url: "https://.../image.jpg", detail: "auto" }
    ]
  }]
});

console.log(resp.output_text);
```
