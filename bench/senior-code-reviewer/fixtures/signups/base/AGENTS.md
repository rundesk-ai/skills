# AGENTS

`signups` handles registration for a newsletter platform with about 2 million subscribers. Python
3.9+, standard library and SQLite. Until now emails were stored exactly as typed.

`migrations/` holds numbered SQL files applied in order at deploy; a failed migration stops the
deploy. `data/production_sample.sql` is an anonymised sample of the production `users` table.

## Rules

- **Every migration must apply to the production data as it is.**
- **Every query takes parameters.**

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
