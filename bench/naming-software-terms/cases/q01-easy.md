+++
skill = "naming-software-terms"
cases_version = 1
kind = "quality"
difficulty = "easy"
fixture = "helpdesk"
rubric = """
result.1  The new column and model field name the value as a noun phrase that sits with the existing `closed_at` (for example `close_reason`), not a question, mechanism, type suffix or numbered flag (`why_closed`, `reason_text`, `flg_3`).
result.2  The allowed reasons, if any are defined, are named as states (for example `resolved`, `duplicate`, `no_response`), not sentences or numbers.
result.3  No existing name is renamed, and the published API is not changed unless the request's scope is stated to include it.
conduct.1 Reads the existing schema and model names before choosing the new one.
conduct.2 Reports the chosen name and its reason in a few lines, without a glossary, layer table or summary nobody asked for.
"""
+++
We need to store why a ticket was closed. Add it to the database and the model.
