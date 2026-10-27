+++
subject = "senior-code-reviewer"
kind = "quality"
difficulty = "complex"
trap = "a check and an act split across two lock acquisitions, beside a method that does it right"
fixture = "wallet"
cases_version = 1
key = """
clean_verdict is true when the review's final verdict lets the change land as it is: Ready, Approved, or Approved with conditions whose conditions do not include fixing a must item. Here the right verdict is not ready.
must:
  M1 bug+rule  Accounts.transfer checks self.balance(source) (one lock acquisition) and debits in a second; two concurrent transfers of 100 from a balance of 100 both pass and leave -100 (reproduced). Breaks "A balance never goes below zero" on a service that runs many threads. withdraw, beside it, does the check and the debit under one lock. Fix: check and move inside one `with self._lock`. Credit needs Blocking or Important severity.
  M2 bug       transfer debits source before touching target; an unknown target raises KeyError after the debit, so the money disappears (reproduced: 60 gone). Fix: check both accounts exist before changing either, inside the lock.
good code:
  G1 withdraw and deposit (unchanged): correct.
decoys:
  D1 the same-account check: correct.
taste:
  T1 Dict typing; T2 Insufficient carrying only the account name.
extras:
  X1 the new tests are single-threaded, so nothing covers M1.
"""
+++
Review my uncommitted changes before I open a pull request. The requirement: let customers move money between their own prepaid accounts.
