+++
subject = "code-quality-reviewer"
kind = "quality"
difficulty = "complex"
fixture = "ratelimit"
expect_clean = true
cases_version = 1
key = """
must: none. The expected verdict is no bugs, no rule violations and no improvements: "No changes needed" or its equivalent.
decoys (each is correct; flagging it is a false positive):
  D1 a plain dict used as the LRU: insertion-ordered since Python 3.7, and every use re-inserts the key. Correct and commented.
  D2 REMOTE_ADDR rather than X-Forwarded-For: deliberate and commented; trusting the header would let clients choose their key.
  D3 eviction forgets a key's debt: a documented trade-off for bounded memory.
  D4 max(0.0, now - last): guards a clock going backwards; tested.
  D5 allow and retry_after each take the lock separately in the middleware; tokens can only grow between them, so Retry-After is at worst slightly high, and is rounded up on purpose.
  D6 Retry-After at least 1 and rounded up: deliberate and commented.
  D7 _refilled and _check_cost are shared by allow and retry_after: no duplication to remove.
taste:
  T1 the test reads limiter._buckets; T2 no type hint on _refilled's bucket parameter; T3 the "unknown" literal; T4 a lambda assigned to a name in a test; T5 float tokens.
extras (arguable; neither hit nor false positive if raised as Unverified or Improvement with a stated cost):
  X1 requests without REMOTE_ADDR share one "unknown" bucket (WSGI servers set it in practice).
  X2 float accumulation in tokens could refuse a request a hair early after many tiny refills.
"""
+++
Review the `ratelimit` package in this repository for code quality: bugs, AGENTS.md violations, and improvements worth fixing.
