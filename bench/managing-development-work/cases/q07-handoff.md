+++
skill = "managing-development-work"
cases_version = 3
kind = "quality"
difficulty = "complex"
fixture = "invoicer-resume"
rubric = """
result.1  One thin slice of multi-currency works end to end through the CLI (for example an invoice created in one currency other than USD shows and lists in it), with tests, and the full suite passes.
result.2  Reports and totals never add amounts in different currencies together: either the slice keeps them apart, or it leaves totals unchanged and names mixed-currency reporting as an open slice.
result.3  A new brief for multi-currency exists in `.work/briefs/`, separate from the recurring-invoices brief, which is left unchanged; it holds Done when, the slices with state and proof, and an executable Next action.
result.4  Later slices (for example reports by currency, exchange rates, recurring invoices in a currency) are named with what would prove each, and owner decisions are listed rather than guessed.
conduct.1 States the outcome and proof and writes the slice list before writing code.
conduct.2 Finishes and proves the first slice before starting another.
"""
+++
We need invoices in other currencies, not just USD. Get the first part working today; I'll pick the
rest up tomorrow in a new session, so leave it so I can.
