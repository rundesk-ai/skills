---
name: using-django
description: Use when building, reviewing, debugging, upgrading or deploying a Django or Django REST Framework application, including app layout and naming, models and migrations, ORM query counts, transactions and locking, services, serializers and permissions, Celery tasks, workers and scheduled jobs, caching, pytest-django tests, settings and environment variables, security, static and media files, and running behind a reverse proxy with gunicorn. It supplies version-aware Django defaults, the traps that pass tests and fail in production, and the commands that prove a change. Do not use for Python with no Django boundary, or for SQL and index tuning that never touches the ORM.
---

# Use Django

Most Django defects that reach production passed the test suite: the tests ran on another database,
inside a transaction, with `DEBUG` on, or without the proxy in front. Work out what the tests do not
cover, and prove that part another way.

## Read the project's contract first

```sh
python -m django --version
python -m pip show djangorestframework pytest-django   # or read the lockfile
```

Then read the settings module and how it is split, the `DATABASES` engine in tests and in
production, `pytest.ini` or `pyproject.toml`, and how the app starts in production (Dockerfile,
entrypoint, Procfile). Release notes break real code every minor version (6.0 made `BigAutoField`
the default primary key; 6.1 made `check` open every database), so check an API against the
installed version's documentation, not memory. Follow the project's existing layout, settings
style and service pattern; deviate only for a correctness or security defect, and say so.

## Prove every change with the gate CI should run

```sh
python manage.py check                        # imports every URLconf, view and model
python manage.py makemigrations --check       # exits 1 if a model change has no migration
python manage.py migrate --plan               # what a deploy will apply, in order
python -m pytest                              # with the project's own flags
DJANGO_SETTINGS_MODULE=<prod settings> python manage.py check --deploy
```

`check` is the cheapest guard there is: a view that lost an import in a merge breaks the URLconf
import, so every request returns 500 and most tests fail with an unrelated-looking error. `check`
names the file and line in a second. Run it, and add it to CI when CI lacks it. From Django 6.1 it
also touches the databases, so in CI give it the test database.

## Layout, views and services

- One app per part of the domain, named for it, owning its models, migrations, admin, services,
  tasks and tests. Set a custom user model (`AUTH_USER_MODEL`) before the first migration; switching
  later means rewriting history.
- Keep views, serializers, admin actions, tasks and commands thin: they parse input, authorize, call
  one service function and shape the output. A rule about one row is a model method or property; a
  reusable filter is a custom `QuerySet` method; an operation that writes several rows, calls out or
  enqueues work is a service function taking typed arguments, not a request, and owning its
  transaction. Only extract when there is a second caller, coordinated writes or side effects.
- Names become tables, reverse accessors, permissions, URL lookups and task names, so a rename can
  cost a migration or strand queued tasks. Read the architecture reference before naming or moving
  a model, app, field, task or URL.
- **A derived field must not overwrite an explicit one.** A `save()` that sets `is_staff` from a role
  silently undoes `is_staff=True` set by an admin, a fixture or a test helper that sets no role, and
  the symptom is 403s everywhere else. Derive only when the source field changed, or compute it as a
  property, and test the explicit path.

## Write it once, leave nothing unused

Duplication and dead code arrive one reasonable change at a time, often from different agents each
revising code they did not write, and every copy is a place the next fix misses:

- **Before writing a rule, find its existing home by convention, not by name.** A filter is a
  queryset method (`Booking.objects.active()`), a derived value a model property, an access rule a
  permission class or `get_queryset()`, a status a `TextChoices` member, a tunable a setting. Found,
  call it; not found, give it one home there.
- **Never copy a function, serializer or queryset to change one value**; take the difference as an
  argument. Copies that already disagree are a bug: decide which is right and prove it with a test.
- **Templates, serializers, admin, exports, emails and tasks call the model's rule and read its
  state**; they never re-derive a total, a status check or an ownership test.
- **Add an output in the same change as the code that reads it**: a serializer field, setting,
  signal, task, URL or template nothing uses is dead on arrival, and a test that only exercises it
  is not a reader.
- **Leave nothing your change made unused.** When new code replaces old, delete the old in the same
  change, then every URL, template, serializer, task, setting and test only it used. Never delete or
  edit a migration that has run anywhere shared. List anything that was already unused for the owner
  rather than deleting it.

## Review in risk order

1. Data loss and irreversibility: migrations, deletes, `on_delete`, backfills.
2. Access: permissions, querysets filtered to the user, serializer fields a client can write,
   settings that fail open.
3. Concurrency and transactions: locks, `on_commit`, idempotent tasks, outbound calls inside
   `atomic()`.
4. Query counts and unbounded lists.
5. Deploy behaviour: environment, proxy, static and media, health checks, workers.
6. Organization and naming, then style the project's linter already enforces.

## Defaults and the failures they prevent

| Prefer | Avoid | Failure prevented |
|---|---|---|
| Treating an empty environment value as unset for paths, hosts and URLs | `env("MEDIA_ROOT", default=...)` alone | `MEDIA_ROOT=""` arrives as `""`, `Path("")` is the working directory, and uploads land in the code checkout |
| `get_queryset()` filtered to what the user may see | object permissions alone on a DRF list | `has_object_permission` never runs on list views, so every row leaks |
| `DEFAULT_PERMISSION_CLASSES` set explicitly | relying on DRF's default | the default is `AllowAny`: a new view is public |
| `select_related` / `prefetch_related` at the queryset, asserted with a query count | relying on review to spot N+1 | a serializer field that adds a query per row |
| `transaction.on_commit(lambda: task.delay(obj.pk))` | `.delay()` inside the transaction | the worker reads before commit, finds no row or old data |
| `select_for_update()` inside `transaction.atomic()`, tested on the production engine | a lock tested on SQLite or inside a test transaction | SQLite ignores it, and a test transaction hides the missing `atomic()` that raises in production |
| `RunPython(forward, reverse)` with a real reverse, or `RunPython.noop` when undoing needs nothing | `RunPython(forward)` | `IrreversibleError` when a failed deploy must roll back |
| Explicit `fields = [...]` on serializers and forms | `fields = "__all__"` | a new column (a flag, a token) becomes writable or public without review |

## Load focused depth

| Concern | Read |
|---|---|
| Apps, layout, naming, services, querysets, models, signals, admin, Django-shaped Python | [architecture](references/architecture.md) |
| Environment variables, security settings, the reverse proxy, health checks, gunicorn, static and media files, release steps | [settings and deployment](references/settings-and-deployment.md) |
| Any migration: safe schema changes on a live table, data migrations, squashing, merge conflicts | [migrations](references/migrations.md) |
| Query counts, `select_related` and `prefetch_related`, fetch modes, transactions, locking | [the ORM](references/orm.md) |
| Serializers, validation, permissions, authentication, throttling, pagination in DRF | [DRF](references/drf.md) |
| Celery or another queue: task design, retries, workers, scheduled and long-running jobs | [tasks and workers](references/tasks-and-workers.md) |
| Caching, outbound HTTP and webhooks, error handling, logging, mail | [caching, HTTP and errors](references/caching-http-and-errors.md) |
| pytest-django: database access, transactional tests, query counts, `on_commit`, fixtures | [testing](references/testing.md) |
| A claim here is challenged, or a release may have changed it | [sources](references/sources.md) |

Cross-cutting changes need more than one. General Python, engine-level SQL and index work, HTTP API
design and the choice of what to test are not Django questions; follow the stack's own guidance for
each.
