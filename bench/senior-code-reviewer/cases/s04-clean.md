+++
subject = "senior-code-reviewer"
kind = "quality"
difficulty = "medium"
fixture = "products"
expect_clean = true
cases_version = 1
key = """
clean_verdict is true when the review's final verdict lets the change land as it is: Ready, Approved, or Approved with conditions that are optional. Here the right verdict is Ready.
A sound change: pagination with validated input, a stable order, parameters, tests for the default, last, empty and invalid pages, and the one existing caller updated.
must: none.
decoys (each is correct; reporting it as a defect is a false positive):
  D1 LIMIT ? OFFSET ? with ORDER BY id: parameterized and stable. OFFSET pagination at 40,000 rows is fine (the deepest page is 2,000 rows in at per_page 20).
  D2 ValueError from int() and from list_products are both mapped to 400: intended, and the error message covers both.
  D3 a page past the end returns an empty list with 200: a normal pagination contract.
  D4 the response echoes page and per_page: harmless and useful.
taste:
  T1 typing imports; T2 the error message wording; T3 no total count in the response (not in the requirement).
extras (arguable; neither hit nor false positive if raised as Optional or Unverified):
  X1 int() accepts " 2 " and "+2".
  X2 no total count for the client to show the number of pages.
(Corrected again 2026-10-26 after the second run: the fixture's AGENTS.md said input "is validated in products/api.py", which the change's range check in store.py literally broke; reviewers that quoted it were right. The rule now says what was meant: invalid input is answered with 400 by api.py, wherever the checks live.)
(Corrected 2026-10-26 after the first run: the change had no upper bound on page, so a huge page raised OverflowError from SQLite and answered 500, not 400. Every arm in every run found it and blocked, rightly. The fixture now bounds page at 1,000,000 and tests it, so the case is clean as intended; that run's s04 verdicts do not count as wrongly blocked.)
"""
+++
Review my uncommitted changes before I open a pull request. The requirement: paginate the product list, 20 per page by default and at most 100, with invalid input answered by 400.
