+++
skill = "writing-agent-instructions"
cases_version = 1
kind = "quality"
difficulty = "complex"
fixture = "courier"
rubric = """
result.1  The three headings `test/agents-file.test.js` pins — `## Ground rules`, `## Commands`, `## Done means` — are kept exactly and in order, and `npm test` still passes.
result.2  `AGENTS.md` and `CLAUDE.md` are byte-identical afterwards, and something checks it (a test or check that fails when they differ).
result.3  The rules that lived in only one copy are reconciled, not lost: never run `db:reset` (with its reason, the shared staging database), no real address in a fixture or test, and a fee always travels with its currency all survive.
result.4  The real rules survive in substance: money is an integer minor unit added with `addFees`; never log a request body; migrations are ask-first and a run one is never edited; dependencies are ask-first.
result.5  The Policy rule is gone or rewritten to what the code does (authorisation through `requireRole` in `src/auth/requireRole.js`); no `src/policies/` or Policy class is named as a rule.
result.6  Stale content is fixed: commands are `npm`, not `yarn`; `db:reset` is not offered as a handy command; the missing `docs/setup/legacy-onboarding.md` and the count of 212 tests are gone.
result.7  The code gallery is out of the rules file: moved to a linked file, or removed with that said. The project tour, framework basics, team values and generic lines ("write clean code", "meaningful names") are gone.
result.8  The result is 250 lines or fewer, uses no capitals for emphasis, and bolds labels rather than whole sentences.
result.9  Each remaining never-rule carries its reason, and the definition of done under `## Done means` lists observed evidence (named gates), not feelings.
conduct.1 The reply accounts for the old file: which rules were kept, merged, fixed or dropped, including the drift between the two copies.
conduct.2 The reply names what was not checked and any decision left to the owner (for example the shared headings, or where the gallery went).
"""
+++
Our AGENTS.md has grown out of control and agents ignore half of it. Clean it up.
