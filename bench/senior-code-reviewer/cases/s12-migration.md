+++
subject = "senior-code-reviewer"
kind = "quality"
difficulty = "complex"
heldout = true
fixture = "signups"
cases_version = 1
key = """
clean_verdict is true when the review's final verdict lets the change land as it is: Ready, Approved, or Approved with conditions whose conditions do not include fixing a must item. Here the right verdict is not ready.
Held out: written after the first run, before the agent change it measures was run on it.
must:
  M1 bug+rule  migrations/002_unique_email.sql (untracked) creates a unique index on lower(email), but production has stored emails as typed for years and the sample already holds case duplicates (ada@ / Ada@, bob@ / BOB@); the migration fails with "UNIQUE constraint failed" on that data (reproduced), which stops the deploy. Tests build an empty database, so they pass. Breaks "Every migration must apply to the production data as it is". Fix: a migration that first finds and resolves existing duplicates (merge or rename), then adds the index. Credit needs the existing data named and Blocking or Important severity.
good code:
  G1 register catching IntegrityError and raising AlreadyRegistered: correct, and parameterized.
decoys:
  D1 an expression index on lower(email) is valid SQLite and the right shape for case-insensitive uniqueness.
taste:
  T1 the exception name; T2 strip() without lower() on insert (the index handles case).
extras:
  X1 the stored emails stay in mixed case, so lookups elsewhere must also use lower().
  X2 no test runs the migration against data like the production sample.
"""
+++
Review my uncommitted changes before I open a pull request. The requirement: stop people registering the same email twice in different letter case.
