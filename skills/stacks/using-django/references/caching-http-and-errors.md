# Caching, outbound HTTP, errors, logging and mail

## Caching

- Configure a shared cache (`django.core.cache.backends.redis.RedisCache`, Memcached) in production.
  The default local-memory cache is per process: each gunicorn worker has its own copy, so
  invalidation, locks (`cache.add`), throttles and rate limits silently apply per worker.
- Cache a computed value under a key that names its inputs and a version
  (`f"room:{room_id}:availability:v2"`), with an explicit timeout. Bumping the version is the
  cheapest invalidation after a format change.
- Invalidate after the write commits: `transaction.on_commit(lambda: cache.delete(key))`. Deleting
  inside the transaction lets a concurrent read repopulate the cache from the old row.
- `cache.get_or_set(key, compute, timeout)` lets several processes compute at once on a miss; for an
  expensive value, guard the computation with `cache.add` as a lock.
- Per-view caching (`cache_page`) and template fragment caching vary by URL, not by user, unless told
  otherwise (`vary_on_cookie`, a user id in the key); a cached authenticated page served to the next
  user is a data leak.
- Never cache a queryset object; cache the list of values or ids it produced.
- Tests: use `locmem` or dummy cache in test settings and clear it between tests that rely on it.

## Outbound HTTP

- Give every call an explicit timeout. `requests` has none by default and waits forever; `httpx`
  defaults to five seconds. A stuck call holds a gunicorn worker until gunicorn kills it.
- Never call out inside `transaction.atomic()`: the call cannot roll back and it holds row locks
  while it waits. Call before, or from a task enqueued with `on_commit`.
- Retry only idempotent requests, or send the provider's idempotency key, with backoff; prefer
  retrying in a task over sleeping in a request.
- Wrap each provider in a small client module that the rest of the code calls, so timeouts,
  authentication, error mapping and test doubles live in one place. Do not let a provider's
  exception types leak into views.
- Validate webhooks: verify the signature on the raw body before parsing, make the handler
  idempotent on the event id, and return 2xx quickly, doing the work in a task.

## Errors

- Raise domain exceptions from services (`BookingAlreadyCancelled`) and translate them at the edge:
  in DRF a `ValidationError`, `PermissionDenied`, `NotFound` or a custom `APIException` subclass with
  its `status_code`; in plain views `Http404` or `PermissionDenied`. Map them once, in a custom DRF
  `EXCEPTION_HANDLER` when many views share them, not in a `try` in every view.
- `get_object_or_404` for lookups by URL; a bare `.get()` turns a bad id into a 500.
- Do not catch `Exception` in a view to return a friendly 400: it hides defects and turns a 500
  that alerts someone into a 400 that nobody sees.
- `DEBUG = False` in production shows the `500.html` template; give it one that does not need a
  database or context processors, because it renders when those may be the thing that failed.

## Logging

- Configure `LOGGING` to write to stdout in containers, at `INFO` for the project's loggers and
  `WARNING` for noisy libraries; keep `django.request` errors and `django.security` warnings
  (`DisallowedHost`, suspicious operations) visible.
- `logger = logging.getLogger(__name__)` per module; `logger.exception(...)` inside `except` to keep
  the traceback; structured context (`extra={"booking_id": ...}`) instead of formatted strings.
- Never log passwords, tokens, full card or identity numbers, or whole request bodies.
- Send unhandled exceptions to an error tracker when the project has one; `ADMINS` email is a last
  resort that floods in an incident.

## Mail

- Send mail from a task or `on_commit`, never inside a transaction or a slow request.
- Templates for subject and body, rendered with the recipient's language active
  (`translation.override`).
- Tests: Django's test setup swaps in the local-memory backend; assert on `mail.outbox`.
- From 6.1, `MAILERS` configures named mail backends and the `EMAIL_*` settings are deprecated;
  follow what the installed version and the project use.
