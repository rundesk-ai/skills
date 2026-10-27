+++
subject = "code-quality-reviewer"
kind = "quality"
difficulty = "complex"
trap = "a green suite whose tests assert the wrong answers"
fixture = "proration"
cases_version = 2
key = """
The suite passes. The traps are tests that pin wrong behaviour; a reviewer that treats green as correct misses all three.
must:
  M1 bug+rule  proration.period_days returns (end - start).days, excluding the last day, against "A billing period includes both its first and last day": March 1-31 bills 30 days and a full month of 3100 bills 3000. test_full_month, test_half_month and test_leap_february all pin the wrong values. Credit needs the code defect and that the tests are wrong too (naming at least one of them).
  M2 bug+rule  prorate uses round(), which rounds half to even, against "rounded half up": 2.5 cents bills 2. test_half_cent pins 2. Fix: integer arithmetic or Decimal with ROUND_HALF_UP.
  M3 bug+rule  apply_discounts takes the fixed amount before the percentage, against "percentage first, then the fixed amount": 10% and $5 off $100 gives 8550, not 8500. test_discounts only asserts the result is truthy, so it proves nothing. Credit needs the order defect; full credit also names the empty assertion.
decoys:
  D1 test_discount_never_negative is correct under either order (300 with $5 off clamps to 0).
  D2 test_period_cannot_end_before_start and the ValueError guard are correct.
  D3 percent validation 0..100 is correct.
taste:
  T1 docstrings could state units; T2 days_in_month passed in rather than computed; T3 test names.
extras:
  X1 days_in_month is supplied by the caller, so a wrong value from a caller misprices; calendar.monthrange would remove the parameter.
  X2 a period spanning two months is priced against one month's length.
"""
+++
Review the `billing` package in this repository for code quality: bugs, AGENTS.md violations, and improvements worth fixing.
