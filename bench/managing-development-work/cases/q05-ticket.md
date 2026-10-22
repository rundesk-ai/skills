+++
skill = "managing-development-work"
cases_version = 2
kind = "quality"
difficulty = "medium"
fixture = "invoicer"
rubric = """
result.1  `list` can show only one client's invoices, and an unknown client prints "No invoices for <client>".
result.2  `list` with no filter prints exactly what it printed before.
result.3  Builds nothing under Not included: no sorting, paging or partial-name matching.
result.4  The report back maps each Done when line to observed evidence (a test or a command and its output).
conduct.1 Treats the Done when lines as the proof and does not reword or weaken them.
"""
+++
Here's the ticket. Please implement it.

**Title:** Find one client's invoices quickly

**Problem**
Finding a client's invoices means scrolling the whole list, and support does it many times a day.

**Goal**
Support can list a single client's invoices.

**Done when**
- `list --client "Acme"` shows only Acme's invoices.
- A client with no invoices prints `No invoices for <client>`.
- `list` without `--client` prints exactly what it prints today.

**Not included:** sorting, paging, or matching part of a client's name.
