import { STATES } from './states.js';

// The next job to run at `now`: highest priority first; among equal priorities, the tenant that
// ran least recently, so one busy tenant cannot starve the rest; then the oldest job, then the
// lowest id, so the order is total and the same on every worker.
export function pickNext(jobs, now, lastRunByTenant = new Map()) {
  let best = null;
  for (const job of jobs) {
    if (job.state !== STATES.QUEUED || job.runAt > now) continue;
    if (best === null || compare(job, best, lastRunByTenant) < 0) best = job;
  }
  return best;
}

function compare(a, b, lastRunByTenant) {
  if (a.priority !== b.priority) return b.priority - a.priority;
  const ranA = lastRunByTenant.get(a.tenant) ?? -Infinity;
  const ranB = lastRunByTenant.get(b.tenant) ?? -Infinity;
  if (ranA !== ranB) return ranA < ranB ? -1 : 1;
  if (a.createdAt !== b.createdAt) return a.createdAt - b.createdAt;
  return a.id - b.id;
}

// Delay before retry number `attempt` (1 for the first retry): "full jitter", a uniform draw
// from [0, min(capMs, baseMs * 2^(attempt - 1))), which spreads retries from many workers apart.
export function backoffMs(attempt, { baseMs = 1000, capMs = 60_000, random = Math.random } = {}) {
  if (!Number.isInteger(attempt) || attempt < 1) {
    throw new RangeError(`attempt must be a positive integer, got ${attempt}`);
  }
  // Clamp the exponent: 2 ** 1100 is Infinity, and the cap applies long before 2 ** 30 anyway.
  const ceiling = Math.min(capMs, baseMs * 2 ** Math.min(attempt - 1, 30));
  return Math.floor(random() * ceiling);
}
