# AGENTS

`wallet` holds customer balances for a prepaid card service. Python 3.9+, standard library only.
Requests are served on many threads at once.

## Rules

- **A balance never goes below zero.**
- **Money is integer cents.**

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
