// World News — 24 November 2026 (Node 22, standard library only).
// The entry image lives beside this file as entry.png; the program copies
// it to /output/entry.png and verifies the copy is a whole 1024x1024 PNG
// under the 1 MiB limit before exiting. Outside the grader's container,
// MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = new URL('./entry.png', import.meta.url);
const dest = join(outDir, 'entry.png');

copyFileSync(src, dest);

const bytes = readFileSync(dest);
const pngSignature = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(pngSignature)) {
  throw new Error('entry.png is not a PNG file');
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
// The file must be a whole PNG: its last 12 bytes are the IEND chunk
// (4-byte length 0, "IEND", 4-byte CRC 0xAE426082).
const iend = bytes.subarray(bytes.length - 12);
if (
  iend.readUInt32BE(0) !== 0 ||
  iend.subarray(4, 8).toString('ascii') !== 'IEND' ||
  iend.readUInt32BE(8) !== 0xae426082
) {
  throw new Error('entry.png is truncated: missing IEND chunk');
}
console.log(
  `wrote ${dest} (${width}x${height} PNG, ${statSync(dest).size} bytes)`
);
