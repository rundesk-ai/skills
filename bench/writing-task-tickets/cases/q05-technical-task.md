+++
skill = "writing-task-tickets"
cases_version = 3
kind = "quality"
difficulty = "medium"
rubric = """
result.1  Uses a one-sentence Goal, not a User story: nobody's experience changes when the upgrade goes right, and no "As a developer" story appears.
result.2  Title and Problem speak for who is hurt if it is not done (customers' payment data, checkout failing), and Problem states that cost in at most two sentences.
result.3  Done when holds only new work; the already-upgraded staging environment is not a requirement but appears as a technical note.
result.4  Library names, version numbers and the config flag appear, if at all, only in Technical notes with a reason.
result.5  The date the old library loses support is written as a date or a delay a reader can check, not as a release or a pipeline event.
conduct.1 Notes after the ticket are four or fewer one-sentence bullets, with nothing after them.
"""
+++
Write a Linear ticket: we need to upgrade payments-client from v3 to v5 in the checkout service before v3 loses vendor support on 31 March, after which security patches stop. Staging already runs v5. v5 drops the legacy_tokens flag, so we need to move the saved-card flow off it, and checkout must keep working for customers with saved cards. Run the full regression suite and roll out behind a feature flag.
