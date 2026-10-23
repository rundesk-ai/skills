+++
skill = "managing-development-work"
cases_version = 3
kind = "quality"
difficulty = "medium"
fixture = "invoicer-resume"
rubric = """
result.1  Yearly schedules work: one invoice per year on the anniversary, a 29 February start issues on 28 February in other years, no period invoiced twice; tests cover these and the full suite passes.
result.2  Recorded decisions are kept, not reopened: generation stays the `generate` CLI command, with no daemon or scheduler added.
result.3  Pause and the email reminder are not built in this slice; they stay open slices.
result.4  The existing brief is updated in place: slice 2 marked done with its observed proof, Next action pointing at the next open slice, no second brief created.
conduct.1 Reads the brief before deciding what to do, and resumes from its first unproven slice instead of re-scoping the whole request.
conduct.2 Checks the brief's next action against the code: notices `cadence` already exists on `Schedule` rather than adding it again.
"""
+++
Carry on with the recurring invoices.
