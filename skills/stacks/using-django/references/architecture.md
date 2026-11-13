# Architecture and code organization

Follow the structure the project already has. These are the defaults when it has none, and the
reasons to deviate from it when it causes a defect.

## Layout

```text
manage.py
config/                  settings, urls, wsgi/asgi, celery app: the project, not a domain
  settings.py            or settings/ with base.py plus one module per environment
bookings/                one app per part of the domain
  models.py              or models/ split by aggregate, re-exported from models/__init__.py
  querysets.py           custom QuerySets, when models.py grows
  services.py            operations that write, call out or enqueue
  selectors.py           reads shaped for a screen or endpoint, when views grow
  serializers.py  views.py  urls.py  admin.py  tasks.py  apps.py
  management/commands/   one file per command
  migrations/
  tests/                 test_models.py, test_api.py, test_services.py ...
```

Split a module into a package when it passes a few hundred lines or mixes unrelated aggregates,
and re-export from `__init__.py` so imports and migrations do not change. Celery autodiscovers
`tasks.py` in every installed app; a task elsewhere is not registered unless imported.

## Naming

Django derives names from yours: table names, reverse accessors, permissions, default templates,
URL lookups and task names. A name chosen carelessly is copied into the database and into every
caller, and renaming it later costs a migration or breaks queued work.

| Thing | Convention | Example |
|---|---|---|
| App | short, lowercase, plural noun for the domain; no `app` or `django` in it | `bookings`, `billing` |
| Model | singular CapWords noun | `Booking`, `RoomBlock` |
| Field | snake_case; booleans `is_` / `has_`; timestamps `_at`; foreign keys named for the object, not `_id` | `is_active`, `cancelled_at`, `room` |
| `related_name` | plural of the child as the parent sees it; set it on every foreign key to the user model or to another app | `user.bookings`, not `user.booking_set` |
| Choices | `TextChoices` nested in the model, singular | `Booking.Status.CANCELLED` |
| QuerySet method | an adjective or condition, chainable | `.active()`, `.visible_to(user)` |
| Service function | verb and object, keyword-only arguments | `cancel_booking(*, booking_id, actor)` |
| Task | verb and object, ending `_task` only if the project does | `send_refund_email` |
| Serializer / view | `<Model><Purpose>Serializer`; `<Model>ViewSet` or `<Model>ListView` | `BookingCancelSerializer` |
| URL name | namespaced with `app_name`; reverse by name, never hard-code paths | `reverse("bookings:cancel", args=[pk])` |
| Template | `<app>/<model>_<purpose>.html`, the generic views' default | `bookings/booking_detail.html` |
| Migration | `makemigrations --name` saying what changed | `0007_booking_cancelled_at` |
| Management command | verb and object; the file name is the command | `backfill_refunds.py` |
| Setting | upper case, prefixed with the project for its own settings | `BOOKINGS_REFUND_WINDOW_DAYS` |

Renames that reach beyond the code:

- **A model or field** is a migration; check `makemigrations` asks "Did you rename…?" and produces
  `RenameModel` or `RenameField`, not a drop and add that loses the data. Keep the column with
  `db_column` when other systems read the table.
- **An app label** changes every table name, content type and permission; avoid it, or set
  `db_table` and plan the content-type move.
- **A task's module or function** changes its registered name (`bookings.tasks.send_refund_email`).
  Tasks already queued under the old name fail as unregistered; keep the old name with `name=` on
  the decorator, or drain the queue first.
- **A URL name** breaks every `reverse()` and `{% url %}`; search for the string, including
  templates.

## Where code goes

| Code | Home | Why there |
|---|---|---|
| A rule about one row (`is_overdue`, `total_with_tax`) | a model method or property | every caller reads it from the object it describes |
| A reusable filter (`active()`, `visible_to(user)`) | a custom `QuerySet`, exposed with `as_manager()` | chains with other filters and works on related managers |
| An operation that writes several rows, calls out, or enqueues work | a service function in the app (`services.py`) | callable from a view, a task, a command and the admin alike |
| A read shaped for one screen or endpoint, with its joins | a selector function or the view's `get_queryset()` | the query count is fixed in one place |
| Request parsing and response shape | a view and a serializer or form | the HTTP edge only |
| A fixed set of states | `models.TextChoices` / `IntegerChoices` | one list for the database, forms, serializers and code |
| A tunable value | a setting read through `django.conf.settings` | one place to change it per environment |

A service function takes typed arguments (`cancel_booking(*, booking_id: int, actor: User) ->
Booking`), not a request or a serializer, owns its `transaction.atomic()`, and raises a domain
exception the view translates. A class is warranted only when it holds configuration or a
dependency worth substituting in tests, such as a payment client.

Do not add a service layer to a project that has none to wrap a one-line `save()`. Extract when an
operation has more than one caller, coordinated writes, side effects, or a test boundary of its own.

## Apps

- One app per part of the domain, named for it (`billing`, `bookings`), not per technical layer
  (`models`, `api`). An app owns its models, migrations, admin, services, tasks and tests.
- Dependencies point one way. When two apps import each other's models, move the shared concept, or
  reference by string (`"billing.Invoice"`) and call through the other app's service functions.
- Put start-up wiring (signal registration, checks) in `AppConfig.ready()`. Never query the
  database there or at import time: Django warns about it, it runs before migrations on a fresh
  database, and it runs in every process, including `migrate` and `collectstatic`.

## Models

- Set a custom user model before the first migration, even if it adds nothing yet.
- Add a database constraint for every invariant that must hold whatever code writes the row:
  `UniqueConstraint` (with `condition=` for "one active per user"), `CheckConstraint`, `null=False`.
  Validation in forms and serializers is for the user's benefit; the constraint is the guarantee.
- Money in `DecimalField` or integer minor units, never `FloatField`.
- `on_delete=PROTECT` for anything financial or audited; `CASCADE` only where the child has no
  meaning without the parent. Django 6.1's `DB_CASCADE` deletes in the database without sending
  `pre_delete` or `post_delete`.
- Override `save()` only for invariants of the row itself, and never to overwrite a field a caller
  may set explicitly (see the derived-field rule in the skill). `save()` does not run for
  `QuerySet.update()`, `bulk_create()` or `bulk_update()`, so it cannot be the only guard.
- Give every model a `__str__`. Set `Meta.ordering` only when every query wants that order: it adds
  a sort to every query that does not override it, and paginate over an explicit, unique `order_by()`.

## Signals

Prefer an explicit call in a service function. A signal hides control flow from the reader, runs
inside the sender's transaction, does not fire for `update()`, `bulk_create()` or queryset
`delete()`, and makes test order matter. Use a signal for decoupling you actually need: reacting to
a third-party app's model, or one app announcing an event others may subscribe to. A receiver that
enqueues work or sends mail does it through `transaction.on_commit`.

## Django-specific Python practice

The language's own guidance owns general Python style; these are the Django-shaped parts.

- Read settings with `from django.conf import settings`, never by importing the settings module:
  the latter bypasses `DJANGO_SETTINGS_MODULE` and test overrides.
- `django.utils.timezone.now()`, never `datetime.now()` or `datetime.utcnow()`. `USE_TZ` is on by
  default since 5.0, and a naive datetime saved with it on raises a `RuntimeWarning` and is read in
  the default time zone. Convert to local time only for display.
- Translate user-visible strings at module level with `gettext_lazy`; plain `gettext` there is
  evaluated once, at import, in whatever language was active.
- Type hints: `django-stubs` and `djangorestframework-stubs` make a type checker understand
  managers, querysets and fields; add them only with the project's type checker, not on their own.
- Run the project's formatter and linter (`ruff` with its `DJ` rules, where configured) before
  finishing; they catch `null=True` on string fields, a model without `__str__`, and `fields = "__all__"`
  on a model form.

## Admin

- The admin is a privileged API: set `list_select_related` and `raw_id_fields` or
  `autocomplete_fields` for foreign keys to big tables, or every change page loads every row.
- Business actions in the admin call the same service functions as the API.
- Permissions come from `has_*_permission` and Django's model permissions; `is_staff` only opens the
  door.
