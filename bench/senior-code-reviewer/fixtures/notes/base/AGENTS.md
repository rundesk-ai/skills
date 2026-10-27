# AGENTS

`notes` stores private notes for each user of a journaling app. Python 3.9+, standard library and
SQLite. A user must never read or change another user's notes.

## Rules

- **Every query takes parameters**; values are never formatted into SQL.
- **Every function that reads or changes a note checks it belongs to the acting user.**

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
