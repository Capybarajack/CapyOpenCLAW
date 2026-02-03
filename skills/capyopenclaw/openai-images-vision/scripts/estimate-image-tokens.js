#!/usr/bin/env node
/**
 * Quick image token estimator based on OpenAI docs:
 * https://platform.openai.com/docs/guides/images-vision
 *
 * This is for rough estimation / planning, not billing.
 *
 * Examples:
 *   node scripts/estimate-image-tokens.js --model gpt-4.1-mini --width 1024 --height 1024
 *   node scripts/estimate-image-tokens.js --model gpt-4o --detail high --width 1024 --height 1024
 */

function getArg(name, fallback = undefined) {
  const idx = process.argv.indexOf(`--${name}`)
  if (idx === -1) return fallback
  return process.argv[idx + 1] ?? fallback
}

function mustInt(name) {
  const v = Number(getArg(name))
  if (!Number.isFinite(v) || v <= 0) throw new Error(`--${name} must be a positive number`)
  return Math.floor(v)
}

function ceilDiv(a, b) {
  return Math.ceil(a / b)
}

function estimatePatches32(width, height) {
  return ceilDiv(width, 32) * ceilDiv(height, 32)
}

// For GPT-4.1-mini/nano/o4-mini patch-based path.
function estimatePatchModel(width, height, multiplier) {
  let w = width
  let h = height
  let patches = estimatePatches32(w, h)

  if (patches > 1536) {
    // shrink factor from docs
    const r0 = Math.sqrt((32 * 32 * 1536) / (w * h))
    const wScaled = w * r0
    const hScaled = h * r0

    // adjust to whole patches (floor) per docs
    const wP = Math.floor(wScaled / 32)
    const hP = Math.floor(hScaled / 32)
    w = Math.max(32, wP * 32)
    h = Math.max(32, hP * 32)

    patches = estimatePatches32(w, h)
    patches = Math.min(1536, patches)
  }

  const imageTokens = Math.min(1536, patches)
  const totalTokens = Math.ceil(imageTokens * multiplier)

  return { imageTokens, multiplier, totalTokens, resizedWidth: w, resizedHeight: h }
}

// For 4o-style tile-based path.
function estimateTileModel(width, height, baseTokens, tileTokens, detail) {
  if (detail === 'low') {
    return { baseTokens, tileTokens, tiles: 0, totalTokens: baseTokens }
  }

  // 1) fit in 2048x2048
  let w = width
  let h = height
  const s1 = Math.min(2048 / w, 2048 / h, 1)
  w = Math.round(w * s1)
  h = Math.round(h * s1)

  // 2) shortest side becomes 768
  const shortest = Math.min(w, h)
  const s2 = 768 / shortest
  w = Math.round(w * s2)
  h = Math.round(h * s2)

  // 3) count 512 tiles
  const tiles = ceilDiv(w, 512) * ceilDiv(h, 512)
  const totalTokens = baseTokens + tiles * tileTokens

  return { baseTokens, tileTokens, tiles, totalTokens, resizedWidth: w, resizedHeight: h }
}

function main() {
  const model = String(getArg('model', 'gpt-4.1-mini'))
  const detail = String(getArg('detail', 'auto')) // for tile models
  const width = mustInt('width')
  const height = mustInt('height')

  const patchMultipliers = {
    'gpt-5-mini': 1.62,
    'gpt-5-nano': 2.46,
    'gpt-4.1-mini': 1.62,
    'gpt-4.1-nano': 2.46,
    'o4-mini': 1.72,
  }

  const tileModels = {
    // from docs chart
    'gpt-5': { base: 70, tile: 140 },
    'gpt-5-chat-latest': { base: 70, tile: 140 },
    'gpt-4o': { base: 85, tile: 170 },
    'gpt-4.1': { base: 85, tile: 170 },
    'gpt-4.5': { base: 85, tile: 170 },
    'gpt-4o-mini': { base: 2833, tile: 5667 },
    'o1': { base: 75, tile: 150 },
    'o1-pro': { base: 75, tile: 150 },
    'o3': { base: 75, tile: 150 },
    'computer-use-preview': { base: 65, tile: 129 },
  }

  if (patchMultipliers[model] != null) {
    const r = estimatePatchModel(width, height, patchMultipliers[model])
    console.log(JSON.stringify({
      mode: '32px-patches',
      model,
      input: { width, height },
      resized: { width: r.resizedWidth, height: r.resizedHeight },
      imageTokens: r.imageTokens,
      multiplier: r.multiplier,
      totalTokens: r.totalTokens,
    }, null, 2))
    return
  }

  if (tileModels[model] != null) {
    const { base, tile } = tileModels[model]
    const r = estimateTileModel(width, height, base, tile, detail)
    console.log(JSON.stringify({
      mode: '512px-tiles',
      model,
      detail,
      input: { width, height },
      resized: r.resizedWidth && r.resizedHeight ? { width: r.resizedWidth, height: r.resizedHeight } : undefined,
      baseTokens: r.baseTokens,
      tileTokens: r.tileTokens,
      tiles: r.tiles,
      totalTokens: r.totalTokens,
    }, null, 2))
    return
  }

  console.error(`Unknown model '${model}'. Try one of: ${[
    ...Object.keys(patchMultipliers),
    ...Object.keys(tileModels),
  ].join(', ')}`)
  process.exit(2)
}

try {
  main()
} catch (e) {
  console.error(String(e && e.message ? e.message : e))
  process.exit(1)
}
