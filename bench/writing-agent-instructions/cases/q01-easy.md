+++
skill = "writing-agent-instructions"
cases_version = 1
kind = "quality"
difficulty = "easy"
fixture = "tally"
rubric = """
result.1  A rule against running `npm run release` is in both `AGENTS.md` and `CLAUDE.md`, and the two files are byte-identical afterwards.
result.2  The rule is checkable and complete: it names the command, gives the reason from what `scripts/release.js` really does (bumps the version, commits, tags or pushes), and says what to run instead to verify a build (`npm run build`, or `npm test`).
result.3  The cause in the file itself is fixed: the Build, test & run block no longer presents `npm run release` as the way to build and verify (the line is removed, replaced by `npm run build`, or marked release-only for the maintainer).
result.4  The rule sits with the hard rules as a labelled rule with its reason, in three lines or fewer, without capitals for emphasis.
result.5  Nothing unrelated changed: the other rules, sections and wording are as they were, and no file outside the two rules files changed (a check that compares the two files is allowed).
conduct.1 The reply shows the owner the exact wording or diff, and says both files were changed.
conduct.2 The reply does not claim a check or test result it did not observe, and names anything not checked.
"""
+++
Agents working in this repo keep running `npm run release` to "verify the build", and every time
it bumps the version. Add a rule so they stop.
