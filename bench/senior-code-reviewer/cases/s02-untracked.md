+++
subject = "senior-code-reviewer"
kind = "quality"
difficulty = "complex"
trap = "the defect lives in a new untracked file that git diff does not show"
fixture = "payments"
cases_version = 1
key = """
clean_verdict is true when the review's final verdict lets the change land as it is: Ready, Approved, or Approved with conditions whose conditions do not include fixing a must item. Here the right verdict is not ready.
`git diff` shows only charges.py gaining an import and a three-line wrapper. payments/refunds.py and tests/test_refunds.py are untracked; a review that reads only the diff never sees the refund logic.
must:
  M1 bug+rule  payments/refunds.py refund never checks the amount against what was captured less earlier refunds: a 9000-cent refund on a 4500-cent capture goes through (reproduced), sending real money that was never taken, and repeated refunds are unbounded. Breaks "A refund never exceeds what was captured, less earlier refunds". Fix: refuse when cents > captured_cents - refunded_cents(order). Credit needs Blocking or Important severity and the location in refunds.py.
good code:
  G1 the checks refund does have (positive amount, order captured) are correct.
decoys:
  D1 charges.handle_refund_request is a thin wrapper; the defect is not in it.
taste:
  T1 the re-export import style; T2 dict orders rather than a class.
extras:
  X1 the new tests cover only a partial refund and an uncaptured order, never an over-refund.
  X2 refunds are not idempotent: a retried request refunds twice.
"""
+++
Review my uncommitted changes before I open a pull request. The requirement: let the support team refund part or all of a captured order.
