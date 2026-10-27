+++
subject = "dry-simplicity-reviewer"
kind = "quality"
difficulty = "complex"
fixture = "code-quality-reviewer/ratelimit"
expect_clean = true
cases_version = 1
key = """
Well-factored code. The expected verdict is "Nothing worth consolidating" or its equivalent.
must: none.
decoys (flagging any as something to consolidate or simplify is a false positive):
  D1 _refilled and _check_cost are already shared by allow and retry_after.
  D2 allow and retry_after each take the lock and read the clock; they do different things with the result.
  D3 the dict-as-LRU with pop and re-insert is the simplest bounded structure here; OrderedDict would add nothing.
  D4 client_ip is a one-line function, but it is the documented default for key_func and the place its security comment lives.
  D5 the middleware's two limiter calls (allow, then retry_after) are not redundant: the second runs only on refusal.
taste:
  T1 the test reaches into _buckets; T2 the "unknown" literal; T3 a lambda assigned to a name in a test; T4 repeated setup lines across tests, each test reading alone.
extras:
  X1 a combined acquire() returning the decision and the wait under one lock would remove the second lock acquisition; arguable, cosmetic.
"""
+++
Look for duplication, redundancy and needless complexity in the `ratelimit` package, and tell me what is worth consolidating or simplifying.
