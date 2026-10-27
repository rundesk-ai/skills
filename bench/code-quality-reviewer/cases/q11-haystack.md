+++
subject = "code-quality-reviewer"
kind = "quality"
difficulty = "complex"
trap = "two real bugs buried deep in a 35-file tree of clean code"
fixture = "clinic"
cases_version = 2
key = """
A review that samples files, or reads the top level and stops, misses both. A review that claims to have read everything but misses both has a coverage claim it did not earn.
must:
  M1 bug+rule  clinic/core/util/dates.py add_months adds 30 days per month: January 31 plus a month is March 2, and March 15 plus twelve months is March 10 of the next year (reproduced). Breaks "renews on the same day of the month, or the month's last day". The only test (test_renewal_mid_month) uses April 1 to May 1, which 30 days happens to get right. Fix: compute year and month, clamp the day with calendar.monthrange.
  M2 bug+rule  clinic/core/auth/roles.py can_cancel_others tests `role in "admin,owner"`, a substring test on one string: "", "own", "min" and "admin,owner" all pass (reproduced), so a user with an empty or truncated role cancels other people's appointments. Breaks "Only admins and owners may cancel". Fix: role in ("admin", "owner").
good code (no finding expected): the twelve clinic/codes modules, people/, booking/slots.py, booking/overlap.py, booking/appointments.py, booking/cancel.py, core/util/money.py.
decoys:
  D1 overlaps uses half-open intervals so back-to-back appointments do not clash: correct and documented.
  D2 the twelve codes modules repeat the same describe() shape: each is a small lookup table; merging them into one generic helper is taste, not a cost.
  D3 email.looks_valid is deliberately cheap and says so.
taste:
  T1 the codes modules could be one JSON file; T2 typing List imports; T3 the 45-minute default slot length as a literal.
extras:
  X1 cancel raises StopIteration for an unknown appointment id, which surfaces as a confusing error (or RuntimeError inside a generator).
  X2 next_renewal loops month by month; fine for real dates, slow only for absurd inputs.
  X3 ROLES is defined but never used to validate a role.
"""
+++
Review this repository for code quality: bugs, AGENTS.md violations, and improvements worth fixing.
