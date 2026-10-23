# Recurring invoices

**Status:** active
**Source:** Request: recurring invoices, monthly or yearly, generated on the right date, with pause
and an email reminder a few days before the due date.
**Last checked:** 2026-10-20 17:40

## Done when

- A schedule can be monthly or yearly, and `generate` creates each due invoice on its issue date.
- No period is ever invoiced twice, however often `generate` runs.
- A paused schedule generates nothing until resumed, and skipped periods are not back-filled.
- A reminder is sent a few days before each generated invoice is due.

## Slices

1. [x] Monthly schedules generate on the right dates — rung: 6, reuses `Invoice`, `LineItem`,
   `store` — proof: `tests/test_recurring.py` (dates, month-end clamp, no duplicates), full suite
   passed 2026-10-20.
2. [ ] Yearly schedules — rung: 6 — proof: yearly dates on the anniversary, a 29 February start
   issues on 28 February in other years, no duplicates.
3. [ ] Pause and resume — proof: no invoice while paused; resuming does not back-fill.
~ Email reminder — blocked: no mail service in this project.

## Decisions

- `generate` is a CLI command run by the owner's cron; no daemon or scheduler inside the tool.
- A 29 February yearly start issues on 28 February in non-leap years (owner, 2026-10-20).

## Next action

Add a `cadence` field to `Schedule`, then yearly dates in `issue_dates`.

## Blocked on

- Email reminder: which mail service, and its credentials (owner).
