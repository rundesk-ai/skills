# AGENTS

`sessions` keeps sign-in sessions and a small response cache for an online banking portal.
Python 3.9+, standard library only.

## Rules

- **A session expires 5 minutes after sign-in.** The regulator requires it.
- **Times are Unix seconds from `time.time()`** unless a name says otherwise.

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
