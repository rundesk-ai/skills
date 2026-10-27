+++
subject = "code-quality-reviewer"
kind = "quality"
difficulty = "complex"
fixture = "jobs"
cases_version = 1
key = """
must:
  M1 bug+rule  src/worker.js tick: claims the job with store.update after reading it via list(); both await, so two workers that read the same queued job both run it (reproduced: 2 runs of one job). Breaks "only through store.transition"; fix: transition(id, QUEUED, {...}) and skip the job when it returns false.
  M2 bug+rule  src/worker.js #fail: `job.attempts > job.maxAttempts` with attempts already incremented runs a job maxAttempts + 1 times (reproduced: 4 runs at maxAttempts 3). Fix: `>=`.
  M3 bug+rule  src/worker.js #fail: compares state to the literal 'canceled' while STATES.CANCELLED is 'cancelled'; a job cancelled while running is re-queued and runs again (reproduced). Breaks the STATES rule. This is the drifted-duplication case: a second copy of a constant that already disagrees.
  M4 bug+rule  src/worker.js #withTimeout: the timeout timer is never cleared, so every job leaves a live timer for timeoutMs, and stop() does not clear them; a stopped worker holds the process open (reproduced: 1.5 s at timeoutMs 1500). Breaks the timer rule.
good code (must receive no bug, rule or improvement finding):
  G1 src/scheduler.js pickNext and compare: total order, fairness, filtering are correct and tested.
  G2 src/scheduler.js backoffMs: full jitter, capped, exponent clamp commented, input validated.
  G3 src/store.js transition: check and set in one synchronous step after the yield; atomic.
decoys:
  D1 start(): tick().catch(...) handles rejections; not an unhandled rejection.
  D2 the exponent clamp at 30 in backoffMs looks like a magic number but is commented and correct.
  D3 -Infinity as the "never ran" value in compare: correct.
taste:
  T1 class vs functions; T2 constructor options object length; T3 console.error rather than a logger; T4 lastRunByTenant held per worker.
extras:
  X1 cancel() itself is get-then-update, so a job can finish between the two and be marked cancelled after it ran.
  X2 a job cancelled while running and then succeeding is overwritten to done.
  X3 lastRunByTenant is not shared between workers, so fairness is per worker.
  X4 the handler keeps running after a timeout rejection.
"""
+++
Review the `src` directory of this repository for code quality: bugs, AGENTS.md violations, and improvements worth fixing.
