+++
subject = "senior-code-reviewer"
kind = "quality"
difficulty = "complex"
heldout = true
fixture = "vault"
expect_clean = true
cases_version = 1
key = """
clean_verdict is true when the review's final verdict lets the change land as it is: Ready, Approved, or Approved with conditions that are optional. Here the right verdict is Ready.
Held out: written after the first run, before the agent change it measures was run on it. A correct change in concurrent code: the trap is inventing a race.
must: none.
decoys (each is correct; reporting it as a defect is a false positive):
  D1 close checks existence and zero balance and deletes under one `with self._lock`: atomic; no race with withdraw, which takes the same lock (a 200-iteration concurrent test covers it and passed in five repeated runs).
  D2 closing refuses any non-zero balance, so money is never lost by closing.
  D3 a closed account raising UnknownAccount afterwards is the intended behaviour.
taste:
  T1 three exception classes; T2 the list-comprehension thread start in the test.
extras (arguable; neither hit nor false positive if raised as Optional or Unverified):
  X1 there is no deposit method in this module, so "deposit to a closed account" is not reachable here.
"""
+++
Review my uncommitted changes before I open a pull request. The requirement: let customers close an account once its balance is zero.
