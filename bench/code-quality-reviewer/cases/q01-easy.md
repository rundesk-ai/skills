+++
subject = "code-quality-reviewer"
kind = "quality"
difficulty = "easy"
fixture = "signup"
cases_version = 1
key = """
must:
  M1 bug       signup/accounts.py login: email formatted into the SQL string; `x' OR '1'='1` logs in as the first user with that user's password (SQL injection). Also breaks the "SQL takes parameters" rule; one root cause.
  M2 rule      signup/accounts.py set_temporary_password: the temporary password is stored in plain text in reset_password, breaking "Passwords are stored only as scrypt hashes". A leaked database reveals working credentials.
  M3 bug       signup/accounts.py average_email_length: ZeroDivisionError when there are no users.
decoys (correct; flagging is a false positive):
  D1 check_password uses hmac.compare_digest: constant-time, correct.
  D2 register lower-cases and strips the email, and login does the same: consistent.
  D3 scrypt n=2**14, r=8, p=1: the standard interactive parameters.
taste (not a finding at any severity):
  T1 no type hint on the cursor; T2 SCHEMA as a module string; T3 f-strings elsewhere; T4 no docstrings.
extras (real but unplanted; neither hit nor false positive):
  X1 register does not validate the email format.
  X2 duplicate email raises sqlite3.IntegrityError rather than a domain error.
"""
+++
Review the `signup` package in this repository for code quality: bugs, AGENTS.md violations, and improvements worth fixing.
