+++
subject = "dry-simplicity-reviewer"
kind = "quality"
difficulty = "medium"
fixture = "code-quality-reviewer/ledger"
expect_clean = true
cases_version = 1
key = """
The trap is two functions that look duplicated and are kept apart by a documented decision. The expected verdict is "Nothing worth consolidating" or its equivalent.
must: none.
decoys (flagging any as duplication to merge is a false positive):
  D1 importer.parse_amount and cli.parse_amount look alike; docs/decisions.md says they are separate on purpose (the export always uses a dot, people type German formats) and that merging them once broke imports. Proposing to merge them is the failure this case measures.
  D2 record_payment and refund share three lines (find, check, validate positive); extracting them saves nothing and hides each function's own rule.
  D3 store._encode and store._decode mirror each other by necessity.
  D4 cli.format_cents and the cents arithmetic in parse_amount are inverse operations, not copies.
taste:
  T1 nested ifs in overdue; T2 dict.get accumulation in balance; T3 variable names.
extras (real but not this reviewer's core; neither hit nor false positive):
  X1 void and apply_late_fee skip the ownership check the other changing functions share (_check_can_change); naming that inconsistency is a fair catch.
  X2 overdue calls datetime.now() where every other function uses clock.now().
  X3 importer swallows every exception and reports all rows imported.
"""
+++
Look for duplication, redundancy and needless complexity in the `ledger` package, and tell me what is worth consolidating or simplifying.
