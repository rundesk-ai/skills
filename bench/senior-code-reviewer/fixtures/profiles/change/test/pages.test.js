import assert from 'node:assert/strict';
import test from 'node:test';

import { memberCard, profilePage } from '../src/pages.js';

test('member card escapes the name', () => {
  assert.equal(memberCard({ name: '<b>Ada</b>' }), '<li class="member">&lt;b&gt;Ada&lt;/b&gt;</li>');
});

test('profile page shows name, bio and join date', () => {
  const html = profilePage({ name: 'Ada', bio: 'Tea & <b>cake</b>', joined: '2026-01-04' });
  assert.match(html, /<h1>Ada<\/h1>/);
  assert.match(html, /Tea &amp; &lt;b&gt;cake&lt;\/b&gt;/);
  assert.match(html, /Member since 2026-01-04/);
});
