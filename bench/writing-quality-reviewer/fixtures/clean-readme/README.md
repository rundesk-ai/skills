# stamp

stamp records when a Markdown page was last reviewed. It writes `last_reviewed: YYYY-MM-DD` into the page's front matter, adding the line if it is missing and replacing it if it is there.

```sh
python3 stamp.py docs/billing.md docs/refunds.md
```

Each file it changes is printed, one per line. A file with no front matter is skipped with a message on stderr, and stamp never adds front matter to a page that has none.

## Options

- `--date YYYY-MM-DD` writes that date instead of today's. Use it when you reviewed the page on another day.
- `--check` writes nothing. It prints the files that would change and exits with status 1 if there are any, so a CI job can fail when a page's date is out of step.

## In CI

To fail a build when any page carries a date other than the one you expect, run the check with that date:

```sh
python3 stamp.py --check --date 2026-11-01 docs/*.md
```

stamp compares only the `last_reviewed` line. It does not read the rest of the page, so it cannot tell whether anyone actually reviewed it; it records that someone said they did.
