# AGENTS

`jobs` is the background job queue for a multi-tenant reporting service: tenants enqueue report
builds, and workers run them with retries. Node 20, ES modules, no dependencies. A job that runs
twice sends a customer two copies of a report and bills them twice.

## Rules

- **A job runs at most `maxAttempts` times in total**, counting the first run.
- **One worker owns a running job.** A job moves from `queued` to `running` only through
  `store.transition`, which checks and sets in one step, so two workers never take the same job.
- **State names come from `STATES` in `src/states.js`.** Never write a state as a string literal.
- **Every timer a worker sets is cleared** when the job it guards settles, and every timer is
  cleared when the worker stops, so a stopped worker lets the process exit.

## Build, test & run

```sh
npm test
```
