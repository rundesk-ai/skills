# The ORM

## Query counts

An N+1 is invisible in review and in a small test database. Fix it at the queryset, and pin it with
a test that fails when it comes back.

- `select_related("customer")` joins a forward foreign key or one-to-one into the same query.
- `prefetch_related("lines")` runs one more query for a reverse foreign key or many-to-many. Filter
  or order the prefetched rows with `Prefetch("lines", queryset=Line.objects.filter(...))`; calling
  `.filter()` on `obj.lines` afterwards ignores the cache and queries again per row.
- Build the queryset where the response is shaped: in a DRF view's `get_queryset()`, matched to the
  fields the serializer reads, including nested serializers and `SerializerMethodField`s.
- Prove it with a query-count assertion over a list of several rows (pytest-django's
  `django_assert_num_queries`, or `assertNumQueries`); one row cannot show an N+1.
- Django 6.1 adds fetch modes: `QuerySet.fetch_mode(models.FETCH_PEERS)` loads a deferred or
  related field for every instance from the queryset at once, and `FETCH_RAISE` raises
  `FieldFetchBlocked` on a lazy load, which turns a hidden N+1 into a test failure. Check the
  installed version before using them.

Other common query-count multipliers: `len(qs)` or `if qs:` where `exists()` or `count()` is meant,
`obj.related.count()` inside a loop (annotate with `Count` instead), and `save()` in a loop where
`bulk_create` / `bulk_update` or `QuerySet.update()` would do. `bulk_create`, `update()` and
`delete()` on a queryset skip `save()`, model signals and per-row validation; check nothing depends
on them first.

## Correctness traps

- `F("stock") - 1` in `update()` avoids a read-modify-write race; `obj.stock -= 1; obj.save()` loses
  concurrent updates. After `obj.save()` with an `F()` expression, refresh before reading the field
  (6.0 does it for you on backends with `RETURNING`).
- `get_or_create` and `update_or_create` race without a unique constraint on the lookup fields; add
  the constraint, and the ORM retries the read after the `IntegrityError`.
- `save(update_fields=[...])` writes only those columns, so a field set by `save()` logic or
  `auto_now` is skipped unless listed.
- Validation on the model (`full_clean()`) does not run on `save()`; forms and DRF serializers call
  their own validation. Enforce invariants that must hold everywhere with database constraints
  (`UniqueConstraint`, `CheckConstraint`).

## Transactions

- Wrap a multi-step write in `transaction.atomic()` at the service function that owns the unit of
  work, not around a whole view by habit. `ATOMIC_REQUESTS = True` holds a transaction open for the
  whole request, including slow template rendering or outbound calls.
- Never make an outbound call (payment API, email, HTTP) inside `atomic()`: it cannot roll back, and
  it holds locks while it waits. Do it before, or after via `transaction.on_commit`.
- `transaction.on_commit(fn)` runs `fn` only if and after the outermost transaction commits, and
  immediately when there is none. Enqueue tasks, send mail and publish events from it. Bind loop
  variables (`lambda pk=obj.pk: ...`), and pass `robust=True` when one callback failing must not stop
  the rest.
- Catching `IntegrityError` inside `atomic()` without a nested `atomic()` around the failing
  statement leaves the outer transaction broken (`TransactionManagementError` on the next query).

## Locking

```python
with transaction.atomic():
    account = Account.objects.select_for_update().get(pk=account_id)
    account.balance -= amount
    account.save(update_fields=["balance"])
```

- `select_for_update()` must be evaluated inside `atomic()`. On PostgreSQL, MySQL and Oracle it
  raises `TransactionManagementError` in autocommit. Two things hide that in tests: SQLite ignores
  `select_for_update()` entirely, and an ordinary database test already runs inside a transaction.
  Prove locking code with a transactional test (`django_db(transaction=True)`) on the production
  engine.
- Lock in a consistent order (by primary key) when locking several rows, or two requests deadlock.
- `select_for_update(of=("self",))` limits the lock to the main table when the query joins others;
  `nowait=True` or `skip_locked=True` for queues and contended rows.
- A lock lasts until the transaction ends, so keep the locked section short and free of I/O.
- For conflicts that are rare, a version column checked in `filter(pk=..., version=v).update(...)`
  (zero rows updated means someone else won) avoids holding locks at all.
