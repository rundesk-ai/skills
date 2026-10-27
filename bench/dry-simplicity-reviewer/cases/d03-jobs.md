+++
subject = "dry-simplicity-reviewer"
kind = "quality"
difficulty = "complex"
fixture = "code-quality-reviewer/jobs"
cases_version = 1
key = """
Complex async code that is mostly well factored, with one copy that has already drifted.
must:
  M1 drift  worker.#fail compares job.state to the literal 'canceled', a hand-written copy of STATES.CANCELLED, which is 'cancelled'. The copies already disagree, so a job cancelled while running is re-queued and runs again. Consolidate: compare with STATES.CANCELLED. Credit needs the drift (the two spellings), not only "use the constant".
good code (no finding expected):
  G1 scheduler.js pickNext and compare: one comparison function, used once, total order; nothing to merge.
  G2 scheduler.js backoffMs: one formula, one place.
  G3 store.js get, list, update and transition each do one thing; the repeated `await tick()` simulates a database round trip per call and is deliberate.
decoys:
  D1 store.update and store.transition both apply a patch, but transition checks state in the same step; merging them loses the guarantee the rules depend on.
  D2 the spread copies ({ ...job }) in get, list and add return snapshots so callers cannot mutate the store; not redundant.
  D3 Worker's constructor takes injected clock, random and timeouts for tests; not unused options.
taste:
  T1 class vs functions; T2 options object length; T3 console.error.
extras (not required of this reviewer; neither hit nor false positive):
  X1 tick claims with update instead of transition, so two workers can take the same job.
  X2 #fail retries one time too many (> instead of >=).
  X3 #withTimeout never clears its timer.
"""
+++
Look for duplication, redundancy and needless complexity in the `src` directory, and tell me what is worth consolidating or simplifying.
