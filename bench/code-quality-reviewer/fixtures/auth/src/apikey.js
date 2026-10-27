import crypto from 'node:crypto';

// Compares a presented API key with the stored one in constant time.
export function keyMatches(presented, stored) {
  const a = Buffer.from(String(presented));
  const b = Buffer.from(String(stored));
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}
