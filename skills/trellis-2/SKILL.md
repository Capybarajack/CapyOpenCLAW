---
name: trellis-2
description: Use Microsoft TRELLIS.2 (image-to-3D) repo for installation and usage notes.
---

# TRELLIS.2

Use this skill when you need **image → 3D asset** generation (mesh + PBR materials) using Microsoft’s **TRELLIS.2**.

## What it is
TRELLIS.2 is a large 3D generative model (4B parameters) for **high-fidelity image-to-3D**, using a sparse voxel structure (“O‑Voxel”) to represent geometry and material attributes (base color / roughness / metallic / opacity).

## When to use
- Turning a product/photo/concept image into a **textured 3D asset** (GLB) for preview / downstream editing.
- Evaluating a modern image-to-3D pipeline that can handle **thin surfaces / non-manifold / complex topology**.

## Prerequisites (important)
- **OS:** Upstream code is **tested on Linux**.
- **GPU:** NVIDIA GPU with **≥ 24GB VRAM** (verified on A100/H100 upstream).
- **CUDA Toolkit:** recommended **12.4** (used for compiling several deps).
- **Python:** **3.8+**.
- **Conda:** recommended.

## Install (upstream-recommended)
Clone:

```bash
git clone -b main https://github.com/microsoft/TRELLIS.2.git --recursive
cd TRELLIS.2
```

Run setup (creates a new conda env `trellis2` if `--new-env` is provided):

```bash
. ./setup.sh --new-env --basic --flash-attn --nvdiffrast --nvdiffrec --cumesh --o-voxel --flexgemm
```

Notes:
- If you have multiple CUDA toolkits installed, set `CUDA_HOME` to the intended one (example):
  ```bash
  export CUDA_HOME=/usr/local/cuda-12.4
  ```
- Attention backend:
  - Default expects **flash-attn**.
  - For GPUs that don’t support flash-attn (e.g. V100), install **xformers** and set:
    ```bash
    export ATTN_BACKEND=xformers
    ```

## Pretrained weights
- Hugging Face model: https://huggingface.co/microsoft/TRELLIS.2-4B

## Minimal usage
### Option A: run the repo example
```bash
python example.py
```

### Option B: pipeline snippet
```python
from PIL import Image
import torch
from trellis2.pipelines import Trellis2ImageTo3DPipeline

pipe = Trellis2ImageTo3DPipeline.from_pretrained("microsoft/TRELLIS.2-4B")
pipe = pipe.cuda()

img = Image.open("path/to/input.png")
mesh = pipe.run(img)[0]
```

## Outputs / export
Upstream shows exporting to **GLB** via `o_voxel.postprocess.to_glb(...)` (see upstream `example.py`).

## Troubleshooting quick hits
- **Build errors / missing nvcc:** verify CUDA toolkit installed and `CUDA_HOME` set correctly.
- **OOM / CUDA out of memory:** reduce resolution / simplify mesh earlier / use a larger VRAM GPU.
- **flash-attn issues:** switch to `ATTN_BACKEND=xformers` (and ensure xformers is installed).

## Upstream
- GitHub: https://github.com/microsoft/TRELLIS.2
- Project page: https://microsoft.github.io/TRELLIS.2
- Paper: https://arxiv.org/abs/2512.14692
- HF Space: https://huggingface.co/spaces/microsoft/TRELLIS.2
