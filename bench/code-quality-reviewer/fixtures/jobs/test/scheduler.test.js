import assert from 'node:assert/strict';
import test from 'node:test';

import { backoffMs, pickNext } from '../src/scheduler.js';
import { STATES } from '../src/states.js';

const job = (over) => ({ id: 1, tenant: 't1', priority: 0, runAt: 0, createdAt: 0, state: STATES.QUEUED, ...over });

test('higher priority wins', () => {
  const jobs = [job({ id: 1 }), job({ id: 2, priority: 5 })];
  assert.equal(pickNext(jobs, 10).id, 2);
});

test('skips jobs not yet due or not queued', () => {
  const jobs = [job({ id: 1, runAt: 50 }), job({ id: 2, state: STATES.RUNNING }), job({ id: 3 })];
  assert.equal(pickNext(jobs, 10).id, 3);
  assert.equal(pickNext([job({ runAt: 50 })], 10), null);
});

test('the tenant that ran least recently goes first', () => {
  const jobs = [job({ id: 1, tenant: 'busy' }), job({ id: 2, tenant: 'quiet', createdAt: 5 })];
  assert.equal(pickNext(jobs, 10, new Map([['busy', 9]])).id, 2);
});

test('ties break on age, then id', () => {
  assert.equal(pickNext([job({ id: 2, createdAt: 1 }), job({ id: 1, createdAt: 2 })], 10).id, 2);
  assert.equal(pickNext([job({ id: 2 }), job({ id: 1 })], 10).id, 1);
});

test('backoff stays inside the jittered, capped window', () => {
  assert.equal(backoffMs(1, { random: () => 0.999 }), 999);
  assert.equal(backoffMs(3, { random: () => 0.5 }), 2000);
  assert.equal(backoffMs(500, { random: () => 0.999 }), 59_940);
  assert.equal(backoffMs(1, { random: () => 0 }), 0);
  assert.throws(() => backoffMs(0), RangeError);
});
