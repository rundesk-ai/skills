import test from 'node:test';
import assert from 'node:assert/strict';
import { dueDate, formatDate } from '../src/dates.js';

test('net 30 due date', () => {
  assert.equal(formatDate(dueDate('2026-03-01', 30)), '2026-03-31');
});
