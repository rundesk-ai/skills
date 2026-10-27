import assert from 'node:assert/strict';
import test from 'node:test';

import { STATES } from '../src/states.js';
import { MemoryStore } from '../src/store.js';
import { Worker } from '../src/worker.js';

test('a successful job is done', async () => {
  const store = new MemoryStore();
  const { id } = await store.add({ tenant: 't1', payload: 21 });
  const worker = new Worker(store, async (n) => n * 2, { clock: () => 0, timeoutMs: 50 });
  assert.equal(await worker.tick(), id);
  const job = await store.get(id);
  assert.equal(job.state, STATES.DONE);
  assert.equal(job.result, 42);
});

test('a failing job is queued again with a delay', async () => {
  const store = new MemoryStore();
  const { id } = await store.add({ tenant: 't1', payload: null });
  const worker = new Worker(store, async () => { throw new Error('boom'); }, { clock: () => 0, timeoutMs: 50, random: () => 0.5 });
  await worker.tick();
  const job = await store.get(id);
  assert.equal(job.state, STATES.QUEUED);
  assert.equal(job.runAt, 500);
});
