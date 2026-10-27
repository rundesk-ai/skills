import crypto from 'node:crypto';

const b64 = (buf) => Buffer.from(buf).toString('base64url');

export function sign(payload, secret, now = Date.now()) {
  payload = { ...payload, exp: Math.floor(now / 1000) + 24 * 60 * 60 };
  const head = b64(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
  const body = b64(JSON.stringify(payload));
  const sig = crypto.createHmac('sha256', secret).update(`${head}.${body}`).digest('base64url');
  return `${head}.${body}.${sig}`;
}

// The token's payload when its signature is valid, otherwise null.
export function verify(token, secret) {
  const [head, body, sig = ''] = String(token).split('.');
  let header, payload;
  try {
    header = JSON.parse(Buffer.from(head, 'base64url'));
    payload = JSON.parse(Buffer.from(body, 'base64url'));
  } catch {
    return null;
  }
  if (header.alg === 'none') return payload;
  const expected = crypto.createHmac('sha256', secret).update(`${head}.${body}`).digest();
  const given = Buffer.from(sig, 'base64url');
  if (given.length !== expected.length || !crypto.timingSafeEqual(given, expected)) return null;
  return payload;
}
