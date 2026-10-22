+++
skill = "managing-development-work"
cases_version = 2
kind = "quality"
difficulty = "medium"
fixture = "invoicer"
rubric = """
result.1  Delivers one working vertical slice end to end, reachable through the CLI: a recurring schedule can be defined and the invoices that are due get generated on the right dates, with no invoice generated twice for the same period.
result.2  The slice is proved by tests that exercise its behavior (dates, monthly and yearly cadence, no duplicates), and the full suite passes.
result.3  Email reminders are not built and not faked with a stub that pretends to send; pause is built only if it stays small, otherwise deferred.
result.4  The reply lists what is deferred as later slices, each with what would prove it, and names the decisions the owner must make (for example how generation is triggered, or month-end dates).
conduct.1 States the outcome and the proof before writing code.
conduct.2 Breaks the request into slices that each work end to end, rather than layers (model, then store, then CLI) or one change.
conduct.3 Starts with the riskiest core path (generation on the right dates), not with the easiest setup work.
conduct.4 Finishes and proves the first slice before starting any other.
"""
+++
Customers keep asking for recurring invoices: monthly or yearly, generated automatically on the
right date, with a way to pause one, and an email reminder a few days before it's due. Can you get
this going? Ship what you sensibly can today and tell me what's left.
