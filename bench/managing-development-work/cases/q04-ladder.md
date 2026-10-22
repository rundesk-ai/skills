+++
skill = "managing-development-work"
cases_version = 2
kind = "quality"
difficulty = "medium"
fixture = "invoicer"
rubric = """
result.1  Finance can get the monthly report in a form Excel opens (for example `report --month 2026-10 --csv`), built on the standard library's csv module with no new dependency.
result.2  Reuses the existing report computation (monthly_totals, format_cents or equivalent) rather than recomputing totals in new code.
result.3  Builds no unrequested flexibility: no plugin system, exporter registry, configurable delimiter or column set, and no .xlsx writer.
result.4  New logic has a test, and the full suite passes.
conduct.1 Reads the existing report and CLI code before choosing the approach, and says what it reuses.
conduct.2 Ends by naming what was skipped or not checked.
"""
+++
Finance wants to open the monthly report in Excel. Can you add that?
