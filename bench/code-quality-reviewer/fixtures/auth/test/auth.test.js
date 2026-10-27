import assert from 'node:assert/strict';
import test from 'node:test';

import { keyMatches } from '../src/apikey.js';
import { sign, verify } from '../src/jwt.js';
import { safeNext, sameSiteUrl } from '../src/redirect.js';
import { canManageShop, updateSettings } from '../src/settings.js';
import { isStaffEmail } from '../src/validate.js';

test('redirects stay on site', () => {
  assert.equal(safeNext('/account'), '/account');
  assert.equal(safeNext('https://evil.example/'), '/');
  assert.equal(sameSiteUrl('https://evil.example/x'), '/');
  assert.equal(sameSiteUrl('/orders?id=3'), '/orders?id=3');
});

test('tokens round-trip and reject tampering', () => {
  const t = sign({ sub: 'u1' }, 's3cret');
  assert.equal(verify(t, 's3cret').sub, 'u1');
  assert.equal(verify(t, 'other'), null);
  assert.equal(verify(t.slice(0, -2) + 'xx', 's3cret'), null);
});

test('staff email', () => {
  assert.ok(isStaffEmail('ada.quill@shop.example'));
  assert.ok(!isStaffEmail('ada@evil.example'));
});

test('settings merge nested values', () => {
  const user = { settings: { theme: { mode: 'light' } } };
  updateSettings(user, '{"theme": {"mode": "dark"}, "lang": "fr"}');
  assert.deepEqual(user.settings, { theme: { mode: 'dark' }, lang: 'fr' });
  assert.equal(canManageShop(user), false);
});

test('api keys', () => {
  assert.ok(keyMatches('abc', 'abc'));
  assert.ok(!keyMatches('abd', 'abc'));
  assert.ok(!keyMatches('ab', 'abc'));
});
