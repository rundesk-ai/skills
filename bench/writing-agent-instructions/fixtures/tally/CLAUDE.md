# AGENTS

Rules for every agent working in this repository. `tally` is a command-line tool installed on other
people's machines; scripts parse its `--json` output, so the output's keys and their order are a
published contract. Node 20+, no dependencies.

## Before you work

1. Read `README.md`, then the file you are changing.
2. Make the smallest change that does the job. Improvements are mentioned, not made.

## Hard rules

- **Dependencies — ask first.** The package has none, and installs stay instant because of it.
- **Commits — ask first.** Never commit or push unless told to.
- **This file — ask first.** `CLAUDE.md` is a byte-identical copy; change both in the same commit.
- **Never change the JSON output's keys or their order.** Other people's scripts break silently.

## Build, test & run

```sh
npm test          # the suite
npm run lint      # tabs and trailing spaces
npm run release   # builds and verifies the package
```

## Definition of done

1. `npm test` and `npm run lint` pass, observed in this session.
2. The package still builds.
3. The reply names what was skipped or not checked.
