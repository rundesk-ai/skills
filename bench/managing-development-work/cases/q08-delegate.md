+++
skill = "managing-development-work"
cases_version = 1
kind = "quality"
difficulty = "complex"
fixture = "invoicer"
rubric = """
result.1  `list --status unpaid` (or an equivalent the reply names) shows only open invoices, and plain `list` prints exactly what it printed before.
result.2  `create` refuses a line item with a negative amount with a clear error and saves nothing, and valid creates still work.
result.3  Each change has a test, and the full suite passes on the combined result.
conduct.1 Hands the two parts to two delegates, and no two delegates edit the same file at the same time: each gets its own files, or the coordinator keeps the shared file and wires it after both return.
conduct.2 Each handoff stands alone: the outcome, the files it may and may not change, the proof to run, and what to report back.
conduct.3 Inspects what each delegate changed and reruns the suite itself before reporting, rather than relaying the delegates' summaries.
conduct.4 The final reply traces each request to observed evidence and names what was skipped or not checked.
"""
+++
Support keeps asking which invoices are still unpaid, so `list` needs a way to show only those. And
someone created an invoice with a negative line item last week; `create` should refuse that. Give
each one to a subagent so they run at the same time, then put it together and tell me when it's done.
