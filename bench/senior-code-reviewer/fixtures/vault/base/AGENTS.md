# AGENTS

`vault` holds balances for a savings app. Python 3.9+, standard library only. Requests are served
on many threads at once.

## Rules

- **A balance never goes below zero, and money is never lost.**
- **Every read-then-write of a balance happens under `self._lock`.**

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
