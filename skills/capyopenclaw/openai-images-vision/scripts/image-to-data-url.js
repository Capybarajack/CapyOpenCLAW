#!/usr/bin/env node
/**
 * Convert a local image file into a Base64 data URL suitable for OpenAI vision input.
 *
 * Usage:
 *   node scripts/image-to-data-url.js path/to/image.jpg
 */

import fs from 'node:fs'
import path from 'node:path'

const filePath = process.argv[2]
if (!filePath) {
  console.error('Usage: node scripts/image-to-data-url.js <path/to/image>')
  process.exit(1)
}

const buf = fs.readFileSync(filePath)
const ext = path.extname(filePath).toLowerCase().replace('.', '')

const mime = (() => {
  if (ext === 'png') return 'image/png'
  if (ext === 'jpg' || ext === 'jpeg') return 'image/jpeg'
  if (ext === 'webp') return 'image/webp'
  if (ext === 'gif') return 'image/gif'
  // default; user should ensure supported type
  return 'application/octet-stream'
})()

const base64 = buf.toString('base64')
process.stdout.write(`data:${mime};base64,${base64}`)
