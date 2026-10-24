import { test } from 'node:test';
import assert from 'node:assert/strict';
import { total } from '../index.js';

test('sums the amount column', () => {
  assert.equal(total('id,amount\n1,10\n2,32\n'), 42);
});
