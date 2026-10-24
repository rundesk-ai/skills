+++
skill = "using-php"
cases_version = 1
kind = "quality"
difficulty = "medium"
fixture = "billing"
rubric = """
result.1  Finds that `modify('+1 month')` overflows a missing day (31 January + 1 month is 3 March) and implements the rule in AGENTS.md: the last day of the month when the day does not exist.
result.2  Keeps the anchor day: after 28 February the next renewal is 31 March, not 28 March, because the rule keys on the day the subscription started; tests cover 31 Jan -> 28 Feb -> 31 Mar -> 30 Apr and a leap year (29 February 2028).
result.3  Finds that `DateTime` is mutable: `dueDate()` moves the caller's issue date, and `renew()` changes an object that may be shared (with `startedAt`, or the caller's). Fixes with `DateTimeImmutable` (or clones) and adds a test that the issue date is unchanged after computing the due date.
result.4  Recognises that the existing `test_renewal_from_month_end` asserts the defect (2026-03-03) against the documented rule, changes it, and says so rather than keeping the old expectation green.
conduct.1 Reproduces both symptoms before changing code.
conduct.2 Runs `php tests/run.php` and reports its output.
"""
+++
Two complaints from support. A customer who subscribed on January 31 was charged again on March 3.
And on several invoices the issue date printed is two weeks later than the day we actually sent them.
Fix both.
