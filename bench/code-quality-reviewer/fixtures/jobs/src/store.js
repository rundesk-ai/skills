import { STATES } from './states.js';

// Stands in for the database: every call yields to the event loop, as a real query would.
const tick = () => new Promise((resolve) => setImmediate(resolve));

export class MemoryStore {
  #jobs = new Map();
  #seq = 0;

  async add({ tenant, payload, priority = 0, maxAttempts = 3, runAt = 0, now = 0 }) {
    await tick();
    const job = {
      id: ++this.#seq,
      tenant,
      payload,
      priority,
      maxAttempts,
      runAt,
      createdAt: now,
      attempts: 0,
      state: STATES.QUEUED,
    };
    this.#jobs.set(job.id, job);
    return { ...job };
  }

  async get(id) {
    await tick();
    const job = this.#jobs.get(id);
    return job && { ...job };
  }

  async list() {
    await tick();
    return [...this.#jobs.values()].map((job) => ({ ...job }));
  }

  async update(id, patch) {
    await tick();
    Object.assign(this.#jobs.get(id), patch);
  }

  // Applies `patch` only while the job is still in state `from`, checked and set in one step.
  // Returns whether it applied.
  async transition(id, from, patch) {
    await tick();
    const job = this.#jobs.get(id);
    if (!job || job.state !== from) return false;
    Object.assign(job, patch);
    return true;
  }
}
