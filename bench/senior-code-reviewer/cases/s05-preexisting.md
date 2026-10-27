+++
subject = "senior-code-reviewer"
kind = "quality"
difficulty = "medium"
fixture = "shipping"
expect_clean = true
cases_version = 1
key = """
clean_verdict is true when the review's final verdict lets this change land: Ready, Approved, or Approved with conditions that do not require fixing the pre-existing bug in this change. Here the right verdict is Ready, with the pre-existing bug reported separately.
The change (express delivery) is correct. The file already had a bug the change does not touch.
must: none for the change.
pre-existing (report separately; it must not block this change):
  P1 rates.standard uses `order_cents > FREE_FROM_CENTS`, so an order of exactly $50.00 pays 495 against "Orders of $50.00 or more ship free" (reproduced). Reporting it under Pre-existing, or as not introduced, is correct and counts as an extra. Making it Blocking or Important for this change, or withholding Ready for it, is the failure this case measures.
decoys:
  D1 express is flat and never free: the requirement says so.
  D2 express validating a negative order like standard does: consistent.
taste:
  T1 module-level constants; T2 options returning a plain dict.
extras:
  X1 P1 itself, reported as pre-existing.
  X2 no test at the 5000-cent boundary (which would have caught P1).
"""
+++
Review my uncommitted changes before I open a pull request. The requirement: offer next-day express delivery at a flat $12.95, never free, alongside standard delivery.
