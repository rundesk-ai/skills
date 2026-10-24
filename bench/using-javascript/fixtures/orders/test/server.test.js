import test from 'node:test';
import assert from 'node:assert/strict';
import { createServer } from '../src/server.js';

test('saves settings over the defaults', async (t) => {
  const server = createServer().listen(0);
  t.after(() => server.close());
  const { port } = server.address();
  const res = await fetch(`http://localhost:${port}/settings`, { method: 'POST', body: '{"pageSize":50}' });
  assert.equal((await res.json()).pageSize, 50);
});

test('rejects an invalid email', async (t) => {
  const server = createServer().listen(0);
  t.after(() => server.close());
  const { port } = server.address();
  const res = await fetch(`http://localhost:${port}/subscribe`, { method: 'POST', body: '{"email":"nope"}' });
  assert.equal(res.status, 400);
});
