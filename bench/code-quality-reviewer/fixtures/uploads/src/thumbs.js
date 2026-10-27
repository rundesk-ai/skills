import fs from 'node:fs/promises';
import path from 'node:path';

const ROOT = path.resolve('uploads');

// The path of `name` inside uploads/, or an error when it would land outside it. Resolving first
// and comparing with the separator rejects both "../x" and a sibling such as "uploads-old/x".
export function insideUploads(name) {
  const full = path.resolve(ROOT, name);
  if (!full.startsWith(ROOT + path.sep)) throw new Error('outside uploads');
  return full;
}

export async function thumbnailSize(name) {
  const { size } = await fs.stat(insideUploads(name));
  return Math.min(size, 64 * 1024);
}
