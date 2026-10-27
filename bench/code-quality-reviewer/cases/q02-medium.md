+++
subject = "code-quality-reviewer"
kind = "quality"
difficulty = "medium"
fixture = "ledger"
cases_version = 1
key = """
must:
  M1 bug       ledger/invoices.py refund: no upper bound; a refund larger than what was paid makes paid_cents negative and the balance exceed the invoice total (refund 5000 of 1000 paid: balance 14000 on a 10000 invoice).
  M2 rule+bug  ledger/invoices.py void: no _check_can_change; any user can void any invoice. Breaks "Only the owner or an admin may change an invoice".
  M3 bug       ledger/importer.py import_rows: `except Exception: pass` drops bad rows silently and returns (total, total), so the CLI prints "imported 3 of 3 rows" when 2 were lost.
  M4 bug       ledger/store.py save: writes the only data file in place with open("w"); a crash or full disk mid-write truncates every invoice. Fix: write a temp file and os.replace.
  M5 bug+rule  ledger/invoices.py overdue: naive datetime.now() minus the aware created_at raises TypeError whenever an unpaid invoice exists. Also breaks "Time comes from ledger.clock.now()"; one root cause.
  M6 rule      ledger/invoices.py apply_late_fee: computes money with a float (rate_percent / 100), breaking "Money is integer cents"; and it changes an invoice without taking or checking the acting User, breaking the ownership rule. Either half counts as the hit; both halves is full credit.
decoys:
  D1 the two parse_amount functions (importer and cli) look duplicated but docs/decisions.md says they are separate on purpose and why. Proposing to merge them is a false positive.
  D2 create has no ownership check: creating is not changing an existing invoice; the rule does not apply.
  D3 os.chmod(PATH, 0o600): correct permissions for the only data file.
  D4 record_payment rejects payments above the balance: correct.
taste:
  T1 nested ifs in overdue; T2 dict.get accumulation in cli balance instead of defaultdict; T3 variable names i, c, f; T4 PATH read at import time.
extras:
  X1 parse_amount (both) mis-parses negative amounts ("-12.50" gives -1150).
  X2 the CLI acts as an admin user for every command.
  X3 save creates the file before chmod, so it briefly has default permissions.
  X4 find is a linear scan.
"""
+++
Review the `ledger` package in this repository for code quality: bugs, AGENTS.md violations, and improvements worth fixing.
