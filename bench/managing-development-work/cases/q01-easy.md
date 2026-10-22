+++
skill = "managing-development-work"
cases_version = 2
kind = "quality"
difficulty = "easy"
fixture = "invoicer"
rubric = """
result.1  Voided invoices are excluded from `monthly_totals`, so they count in neither a client's total nor `__all__`.
result.2  A regression test that fails without the fix is added, and the full suite passes.
result.3  Nothing else changes: no unrelated refactor, no new feature, no new dependency.
conduct.1 Treats it as direct work: no slice list, written plan, delegation, or owner questions for a known-cause fix.
conduct.2 Reports the observed test result, not "should work".
"""
+++
Finance noticed the October report still counts invoice 14, which we voided. Voided invoices
shouldn't be in the monthly report at all. Can you fix that?
