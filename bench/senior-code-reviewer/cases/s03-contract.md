+++
subject = "senior-code-reviewer"
kind = "quality"
difficulty = "complex"
trap = "the change is consistent within itself and breaks an unchanged caller"
fixture = "sessions"
cases_version = 1
key = """
clean_verdict is true when the review's final verdict lets the change land as it is: Ready, Approved, or Approved with conditions whose conditions do not include fixing a must item. Here the right verdict is not ready.
must:
  M1 bug+rule  the change makes cache.ttl() return milliseconds (config.TTL = 300_000) and updates the cache's own use (ttl() / 1000), but session.new_session, which the diff does not touch, still adds cache.ttl() to a time in seconds: a session now lasts 300,000 seconds, about 3.5 days, instead of 5 minutes (reproduced). Breaks "A session expires 5 minutes after sign-in", a regulatory requirement on a banking portal. test_new_session_is_valid only checks a session is valid one second later, so the suite stays green. Fix: convert in session.py too, or give sessions their own setting in seconds. Credit needs session.py named and Blocking or Important severity.
good code:
  G1 Cache.put dividing by 1000 and the sub-second cache test are correct for the cache itself.
decoys:
  D1 secrets.token_urlsafe(32) for the session token: correct.
taste:
  T1 the config comment; T2 the test's manual save and restore of config.TTL.
extras:
  X1 one setting drives both the cache and sessions, so a cache tuning change moves session lifetime; separate settings would prevent the next M1.
  X2 no test pins the session lifetime.
"""
+++
Review my uncommitted changes before I open a pull request. The requirement: switch the cache TTL setting to milliseconds so we can set sub-second cache lifetimes.
