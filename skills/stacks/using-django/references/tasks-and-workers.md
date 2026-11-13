# Background tasks, workers and long-running jobs

Celery is the usual queue for Django and the examples use it; the rules hold for any broker-backed
worker (RQ, Dramatiq, a `django.tasks` backend). Django 6.0's `django.tasks` defines and enqueues
tasks but ships no production worker, so it needs a third-party backend before it replaces one.

## What goes on a queue

Anything slow, retried or external that the user need not wait for: email, webhooks, exports,
image processing, calls to third-party APIs. Keep inside the request what the response depends on
and what must fail the request when it fails.

## Write a task

```python
@shared_task(
    bind=True,
    autoretry_for=(PaymentGatewayTimeout,),
    retry_backoff=True,          # 1 s, 2 s, 4 s ... capped by retry_backoff_max (600 s)
    max_retries=5,
    acks_late=True,
)
def refund_booking(self, booking_id: int) -> None:
    booking = Booking.objects.get(pk=booking_id)
    if booking.refund_reference:            # already done by an earlier attempt
        return
    reference = gateway.refund(booking.amount_cents, idempotency_key=f"booking:{booking_id}:refund")
    Booking.objects.filter(pk=booking_id, refund_reference="").update(refund_reference=reference)
```

- **Pass ids, not model instances.** Arguments are serialized when enqueued; an instance is stale
  by the time the worker runs, and the JSON serializer rejects it.
- **Enqueue after commit**: `transaction.on_commit(lambda: refund_booking.delay(booking.pk))`. Inside
  the transaction, a fast worker reads before the row exists, or reads the old state.
- **Make every task idempotent.** A task can run more than once: a retry after a partial success,
  `acks_late` redelivery after a worker dies, a broker redelivering a task that ran past its
  visibility timeout. Check state before acting, use the external service's idempotency key, and
  write the result with a conditional update.
- **Retry only what a retry can fix** (timeouts, 5xx, connection errors) with backoff and jitter
  (`retry_jitter` is on by default), and a ceiling. Retrying a validation error or a 4xx wastes the
  queue and repeats side effects.
- **Record terminal failure** where someone will see it: a status on the row the user can see, and
  an error report. Celery's default is a log line.
- Keep the task a thin wrapper over a service function, so the same work runs from a test, a
  command or the shell without a broker.

## Run workers

- `acks_late=True` with `task_reject_on_worker_lost=True` for work that must not be lost when a
  worker is killed, and only for idempotent tasks. With the default early ack, a task is gone the
  moment a worker takes it.
- `worker_prefetch_multiplier = 1` for long tasks; the default 4 lets one busy worker hoard tasks
  that idle workers could run.
- Set `task_time_limit` and `task_soft_time_limit` (`CELERY_TASK_TIME_LIMIT` under the usual
  `CELERY_` namespace). A soft limit raises `SoftTimeLimitExceeded` inside the task so it can clean
  up; the hard limit kills the process. Set outbound HTTP timeouts too: a time limit may not
  interrupt a blocked socket on every pool.
- With Redis or SQS as broker, a task not acknowledged within the visibility timeout (Redis: one
  hour by default) is delivered again to another worker. Keep `acks_late` tasks, and ETA or
  countdown tasks, shorter than it, or raise it.
- `worker_max_tasks_per_child` (or `--max-memory-per-child`) recycles a process that leaks memory.
- Route slow and fast work to separate queues (`task_routes`) and run workers per queue, so a
  backlog of exports cannot delay password-reset email.
- Restart workers on every deploy: they run the code they started with. Drain with a warm shutdown
  (`SIGTERM`) so running tasks finish; size the platform's stop timeout to the longest task.
- Run workers from the same image and settings as the web process, as separate processes.
- Celery closes Django's database connections before and after each task. A custom long-running
  loop (a consumer, a `while True` management command) must call
  `django.db.close_old_connections()` per iteration, or it dies on the first dropped connection.

## Scheduled work

- Run exactly one beat (or scheduler) process. Two beats enqueue every periodic task twice.
- Guard a periodic task that can overrun its interval with a lock, so the next run skips rather
  than overlaps:

  ```python
  if not cache.add(f"lock:{name}", "1", timeout=lock_seconds):   # atomic on Redis and Memcached
      return
  try:
      run()
  finally:
      cache.delete(f"lock:{name}")
  ```

  `cache.add` is only a lock on a shared cache; the local-memory cache is per process.
- Store the schedule in code (`beat_schedule`) unless operators need to change it at run time
  (`django-celery-beat`), and make each run safe to repeat or skip.
- Times in `crontab()` are in the Celery `timezone` setting; set it, and expect daylight-saving
  hours to be skipped or run twice.

## Long-running jobs

Imports, backfills and exports over many rows:

- Process in batches by primary-key range or `iterator(chunk_size=...)`, each batch in its own short
  transaction, so locks are brief and progress survives a crash.
- Make the job resumable: record the last processed id, or select only rows not yet done.
- Fan a large job out into one task per batch rather than one task that runs for an hour past every
  time limit and visibility timeout. Celery's `group` and `chord` coordinate the fan-out; a chord
  needs a result backend.
- A one-off data fix that is not part of the schema history is a management command, not a
  migration: give it `--dry-run`, a batch size, and output that says what it changed. A fix every
  environment needs to reach a consistent schema state belongs in a data migration.
- Report progress to the user through a status row they can poll, not through a task result.

## Testing tasks

- Call the service function directly for the logic; test the task wrapper with the broker out of
  the picture.
- `CELERY_TASK_ALWAYS_EAGER` runs tasks inline, inside the caller's transaction and without
  serialization, so it hides the before-commit and non-serializable-argument bugs above. Prefer
  asserting the enqueue (mock `.delay`, or capture `on_commit` callbacks) and running the task
  function separately.
