# AGENTS

`payments` records card captures and refunds for an online shop. Python 3.9+, standard library
only. Money moves for real when these functions run.

## Rules

- **Money is integer cents.**
- **A refund never exceeds what was captured, less earlier refunds.**

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
