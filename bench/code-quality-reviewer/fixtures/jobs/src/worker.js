import { STATES } from './states.js';
import { backoffMs, pickNext } from './scheduler.js';

export class Worker {
  constructor(store, handler, { clock = Date.now, pollMs = 100, timeoutMs = 30_000, random = Math.random } = {}) {
    this.store = store;
    this.handler = handler;
    this.clock = clock;
    this.pollMs = pollMs;
    this.timeoutMs = timeoutMs;
    this.random = random;
    this.lastRunByTenant = new Map();
    this.poller = null;
  }

  start() {
    this.poller = setInterval(() => {
      this.tick().catch((err) => console.error('worker tick failed', err));
    }, this.pollMs);
  }

  stop() {
    clearInterval(this.poller);
    this.poller = null;
  }

  // Runs the next due job, if any, and returns its id.
  async tick() {
    const now = this.clock();
    const job = pickNext(await this.store.list(), now, this.lastRunByTenant);
    if (!job) return null;
    await this.store.update(job.id, { state: STATES.RUNNING, attempts: job.attempts + 1 });
    this.lastRunByTenant.set(job.tenant, now);
    try {
      const result = await this.#withTimeout(this.handler(job.payload));
      await this.store.update(job.id, { state: STATES.DONE, result });
    } catch (err) {
      await this.#fail(job.id, err);
    }
    return job.id;
  }

  // Cancels a queued job, or marks a running one so it is not retried.
  async cancel(id) {
    const job = await this.store.get(id);
    if (!job || job.state === STATES.DONE || job.state === STATES.FAILED) return false;
    await this.store.update(id, { state: STATES.CANCELLED });
    return true;
  }

  async #fail(id, err) {
    const job = await this.store.get(id);
    if (job.state === 'canceled') return;
    if (job.attempts > job.maxAttempts) {
      await this.store.update(id, { state: STATES.FAILED, error: String(err) });
    } else {
      const runAt = this.clock() + backoffMs(job.attempts, { random: this.random });
      await this.store.update(id, { state: STATES.QUEUED, runAt, error: String(err) });
    }
  }

  #withTimeout(promise) {
    return new Promise((resolve, reject) => {
      setTimeout(() => reject(new Error('job timed out')), this.timeoutMs);
      promise.then(resolve, reject);
    });
  }
}
