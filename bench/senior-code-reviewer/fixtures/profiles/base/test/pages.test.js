import assert from 'node:assert/strict';
import test from 'node:test';

import { memberCard } from '../src/pages.js';

test('member card escapes the name', () => {
  assert.equal(memberCard({ name: '<b>Ada</b>' }), '<li class="member">&lt;b&gt;Ada&lt;/b&gt;</li>');
});
