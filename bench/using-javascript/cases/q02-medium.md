+++
skill = "using-javascript"
cases_version = 1
kind = "quality"
difficulty = "medium"
fixture = "orders"
rubric = """
result.1  Finds that `new Date('YYYY-MM-DD')` parses a date-only string as UTC midnight while `setDate`/`getDate` work in local time, so west of UTC the due date lands a day early; fixes by treating the date as a calendar date (parse the parts, or do the arithmetic in UTC throughout) and not shifting it.
result.2  Recognises that the existing date test passes only because `npm test` pins `TZ=UTC`, and proves the fix under a non-UTC zone (for example `TZ=America/New_York`), adding or running a test there.
result.3  Finds that warehouse ids above 2^53 lose precision in `JSON.parse` (9007199254740993 becomes 9007199254740992, and two ids can collide), so lookup by the id in the URL fails.
result.4  Fixes the ids without precision loss: keeps them as strings, using the reviver's source text (`context.source`), quoting before parsing, or a parser that preserves them; does not convert through `Number` anywhere on the path.
result.5  Adds tests that fail before the fix for both bugs and pass after.
conduct.1 Reproduces each symptom before changing code.
conduct.2 Reports each cause separately with what proves it fixed.
"""
+++
Two bug reports. Customers in New York see invoice due dates a day earlier than the terms say.
And some orders from the warehouse feed come back 404 at /orders/<id> even though they're in the
feed. All our tests pass. Find out why and fix it.
