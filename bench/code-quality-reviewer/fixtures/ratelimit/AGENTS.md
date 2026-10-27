# AGENTS

`ratelimit` limits how often each client may call a public API: per-key token buckets and a WSGI
middleware that answers 429 when a client is over its limit. Python 3.9+, standard library only. It
sits in front of every request, so it must be thread-safe, keep memory bounded under a flood of
distinct clients, and never let a client choose its own key.

## Rules

- **Time comes from the injected `clock`**, never from `time` directly in logic, so tests control it.
- **Memory stays bounded.** The limiter never holds more than `max_keys` buckets.
- **Every public function and method has a test** in `tests/`.

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
