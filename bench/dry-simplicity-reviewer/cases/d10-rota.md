+++
subject = "dry-simplicity-reviewer"
kind = "quality"
difficulty = "medium"
fixture = "rota"
expect_clean = false
cases_version = 1
key = """
Held out for the change to the reviewer's bar: whole methods copied with one thing changed, and one literal repeated for one meaning, which the two-or-three-lines exemption had been swallowing; and decoys that a looser bar would flag.
must:
  M1 Week.move_earlier and move_later (rota/shifts.py) are the same swap mirrored: bounds check, swap with the neighbour, log line. One _swap(index, other) behind both.
  M2 exports.export_staff_csv and export_absences_csv are the same CSV writer, quoting rule included, differing only in the column list. One writer taking the columns.
  M3 The gateway timeout 30 is a bare literal in send_week, send_change and send_reminder (rota/notify.py); one named constant or a default on _post.
  M4 Week.split_shift has no caller anywhere.
decoys (proposing to change any of these is a false positive):
  D1 The two-line `if not person: raise ValueError(...)` guard repeated in hours and the senders.
  D2 PAGE_SIZE = 30 is a page of the staff list, not the gateway timeout; folding the two 30s together is wrong.
  D3 overtime_pay_uk and overtime_pay_de: same shape, but AGENTS.md says they follow different statutes and change on different dates.
  D4 The setup repeated across tests.
taste:
  T1 dataclass choices; T2 urllib versus a client library; T3 naming.
extras (real but not core; neither hit nor false positive):
  X1 send_week, send_change and send_reminder differ only in their kind; one sender taking the kind.
  X2 payroll.run notifies inside the loop before the export succeeds.
  X3 the hand-rolled CSV quoting where the csv module would do.
"""
+++
Look for duplication, redundancy and dead code in the `rota` package, and tell me what is worth consolidating or removing.
