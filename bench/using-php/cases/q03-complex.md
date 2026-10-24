+++
skill = "using-php"
cases_version = 1
kind = "quality"
difficulty = "complex"
fixture = "billing"
rubric = """
result.1  Login: finds unsalted `md5` compared with loose `==`, and that a stored hash of the form `0e` followed by digits equals any other such hash (a password of `240610708` is accepted for `QNKCDZO`); replaces it with `password_hash` and `password_verify`.
result.2  Migrates the existing md5 hashes without locking users out: a legacy hash is checked once with `hash_equals` (or strict comparison) and replaced by a `password_hash` on successful login, or wrapped; no forced reset.
result.3  Report: the `sort` and `dir` query parameters are interpolated into `ORDER BY`, which runs attacker SQL (a subquery executes); fixes with an allow-list of columns and directions, since identifiers cannot be bound parameters.
result.4  Finds `unserialize` on the `prefs` cookie (object injection: any class can be instantiated) and replaces it with `json_decode` with error handling, or `allowed_classes => false` at the least.
result.5  Finds `include` built from `$_GET['page']` (local file inclusion through `../`) and replaces it with an allow-list of pages.
result.6  Adds a test per fix that fails on the original code (an exploit as a test), and the suite passes.
result.7  States what was not settled or not reviewed: for example CSRF on the login form, session fixation (`session_regenerate_id` on login), cookie flags, rate limiting, and that the review covered only these files.
conduct.1 Reports each finding with its location, the evidence or exploit, and the proof of the fix.
"""
+++
We have a penetration test next week. Review the login and the admin invoice report for security
problems and fix what you find. Existing users must still be able to sign in after your change.
