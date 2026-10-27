# AGENTS

`accounts` holds user accounts and plans for a SaaS product: an HTTP API for the web app, and a
nightly job that syncs plans from the billing provider. Python 3.12, standard library only.

## Rules

- **A plan is one of `PLANS`**, whoever sets it: the API or the nightly billing sync.
- **Calls to the billing provider are retried**, because its API drops about one request in a
  thousand.

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
