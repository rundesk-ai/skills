+++
skill = "writing-prose"
kind = "quality"
difficulty = "easy"
rubric = """
result.1  Each line is one change, with the user (or "you") as the actor and what they can now do or no longer suffer, not "X functionality has been enhanced".
result.2  No vague catch-all line ("various improvements", "bug fixes and performance improvements") is left standing; it is named from the commits or cut.
result.3  Uses the one real figure in the input (p95 from 4.2 s to 0.9 s) and invents no other number, date or version.
result.4  The internal-only commits (CI cache, dependency bump, test refactor) are left out or kept apart, not presented as user-facing changes.
conduct.1 Contains none of the stock glue the guidance lists ("not just X, but Y", "ultimately", "here's the thing", "we're excited to").
"""
+++
Write the release notes for customers for this week's release. Commits since last tag:

- feat(invoices): add CSV export button to invoice list
- fix(auth): settings save no longer logs user out on safari (session cookie samesite)
- perf(search): add trigram index on contacts.name, p95 search latency 4.2s -> 0.9s on big accounts
- chore(ci): cache node_modules
- chore(deps): bump axios 1.7.2 -> 1.7.4
- refactor(tests): split invoice tests into files
- fix: misc
