# Django source basis

Checked against Django 6.1.3, Django REST Framework 3.18.3, pytest-django 4.14.0 and
django-environ 0.14.0 on Python 3.13, in November 2026. Behaviour marked *observed* was reproduced
in a scratch project on those versions, on SQLite and on PostgreSQL 17. Read this when a claim in
the skill is challenged or a new release may have changed it.

## Django

- [Django 6.0 release notes](https://docs.djangoproject.com/en/6.1/releases/6.0/): `BigAutoField`
  default for `DEFAULT_AUTO_FIELD`; built-in CSP (`SECURE_CSP`, `ContentSecurityPolicyMiddleware`);
  `django.tasks` with no production worker; squashed migrations can be squashed; `F()` fields
  refreshed after `save()` on `RETURNING` backends; Python 3.12 minimum.
- [Django 6.1 release notes](https://docs.djangoproject.com/en/6.1/releases/6.1/): fetch modes
  (`FETCH_ONE`, `FETCH_PEERS`, `FETCH_RAISE`, `FieldFetchBlocked`); "the `check` command now supplies
  all databases when none are specified, so callers should expect database access"; PostgreSQL 15
  minimum.
- [Deployment checklist](https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/):
  `check --deploy`, `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS`, HTTPS cookie settings, HSTS.
- [Settings reference](https://docs.djangoproject.com/en/6.1/ref/settings/):
  `SECURE_PROXY_SSL_HEADER` (trust it only when the proxy sets or strips the header),
  `USE_X_FORWARDED_HOST`, `CSRF_TRUSTED_ORIGINS` (scheme required since 4.0), `ATOMIC_REQUESTS`,
  `STORAGES` (4.2; `DEFAULT_FILE_STORAGE` and `STATICFILES_STORAGE` removed in 5.1),
  `AUTH_USER_MODEL`.
- [System check framework](https://docs.djangoproject.com/en/6.1/ref/checks/) and
  [django-admin](https://docs.djangoproject.com/en/6.1/ref/django-admin/): `check` runs the URL
  checks, which import the root URLconf; `makemigrations --check` exits non-zero without writing
  (4.2+); `migrate --plan`; `sqlmigrate`; `squashmigrations`; `makemigrations --merge`.
- [Migrations topic](https://docs.djangoproject.com/en/6.1/topics/migrations/) and
  [writing migrations](https://docs.djangoproject.com/en/6.1/howto/writing-migrations/): historical
  models via `apps.get_model` without custom methods; `RunPython` reverse and `RunPython.noop`;
  `elidable`; non-atomic migrations; avoiding schema and `RunPython` operations in one PostgreSQL
  migration ("pending trigger events"); squashing and transitioning off `replaces`; conflict
  detection and `--merge`.
- [Migration operations](https://docs.djangoproject.com/en/6.1/ref/migration-operations/):
  `SeparateDatabaseAndState`; [PostgreSQL operations](https://docs.djangoproject.com/en/6.1/ref/contrib/postgres/operations/):
  `AddIndexConcurrently` requires `atomic = False`.
- [Database access optimization](https://docs.djangoproject.com/en/6.1/topics/db/optimization/) and
  [QuerySet API](https://docs.djangoproject.com/en/6.1/ref/models/querysets/): `select_related`,
  `prefetch_related`, `Prefetch`, filtering a prefetched relation re-queries, `exists()` and
  `count()`, `bulk_create` and `update()` skip `save()` and signals, `get_or_create` and unique
  constraints, `select_for_update` (`of`, `nowait`, `skip_locked`; `TransactionManagementError` in
  autocommit on backends that support it; no effect on SQLite).
- [Transactions](https://docs.djangoproject.com/en/6.1/topics/db/transactions/): `atomic`,
  "avoid catching exceptions inside atomic", `on_commit` (runs immediately with no transaction,
  `robust`), `on_commit` callbacks never run under `TestCase`, `captureOnCommitCallbacks`.
- [Static files deployment](https://docs.djangoproject.com/en/6.1/howto/static-files/deployment/)
  and [`ManifestStaticFilesStorage`](https://docs.djangoproject.com/en/6.1/ref/contrib/staticfiles/):
  `STATIC_ROOT`, `collectstatic`, `manifest_strict`; Django serves static and media only with
  `DEBUG` on.
- [Customizing authentication](https://docs.djangoproject.com/en/6.1/topics/auth/customizing/):
  set a custom user model before the first migration.
- [Testing tools](https://docs.djangoproject.com/en/6.1/topics/testing/overview/): `MD5PasswordHasher`
  to speed up tests.

## Django REST Framework

- [Permissions](https://www.django-rest-framework.org/api-guide/permissions/): default `AllowAny`;
  object permissions run from `get_object()` and are not applied to list views "for performance
  reasons"; overriding `get_object()` requires `check_object_permissions()`; `&`, `|`, `~`.
- [Authentication](https://www.django-rest-framework.org/api-guide/authentication/): CSRF enforced
  by `SessionAuthentication` only; the first authentication class decides 401 versus 403;
  `TokenAuthentication`'s single stored token.
- [Generic views](https://www.django-rest-framework.org/api-guide/generic-views/): `get_queryset()`,
  `perform_create()`.
- [Serializers](https://www.django-rest-framework.org/api-guide/serializers/): `validate_<field>`,
  `validate`, `read_only_fields`, `fields = "__all__"`, writable nested serializers need explicit
  `create()` / `update()`.
- [Throttling](https://www.django-rest-framework.org/api-guide/throttling/): throttles use the cache
  and are not a security control; `ScopedRateThrottle`.

## Tools

- [pytest-django helpers](https://pytest-django.readthedocs.io/en/latest/helpers.html):
  `django_db(transaction=...)`, `django_assert_num_queries`, `django_capture_on_commit_callbacks`
  (`execute`), the `settings` fixture reverting changes; [database](https://pytest-django.readthedocs.io/en/latest/database.html):
  `--reuse-db`, `--create-db`, `--nomigrations`.
- [django-environ](https://django-environ.readthedocs.io/): `Env()` and `env.path()`.
- [gunicorn settings](https://gunicorn.org/reference/settings/): workers, `timeout`,
  `accesslog`; [design](https://gunicorn.org/design/): `(2 x cores) + 1` workers as a starting point.
- [Celery with Django](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html):
  `CELERY_` namespace, `autodiscover_tasks()` finds `tasks.py`, `transaction.on_commit` for enqueuing.
- [nginx `proxy_set_header`](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_set_header)
  and [`$http_` variables](https://nginx.org/en/docs/http/ngx_http_core_module.html#var_http_).

## Architecture, tasks, caching and errors

- [Applications](https://docs.djangoproject.com/en/6.1/ref/applications/): `AppConfig.ready()`, and
  the warning on database access during app initialization (added in 5.0; observed in
  `django/db/backends/utils.py` on 6.1.3).
- [Signals](https://docs.djangoproject.com/en/6.1/topics/signals/): signals make code harder to
  follow and debug; [QuerySet `update()`](https://docs.djangoproject.com/en/6.1/ref/models/querysets/#update)
  and `bulk_create()` send no `pre_save` / `post_save`.
- [Time zones](https://docs.djangoproject.com/en/6.1/topics/i18n/timezones/): `timezone.now()`,
  naive datetime `RuntimeWarning`; `USE_TZ` default `True` since 5.0 (observed in
  `global_settings.py`).
- [Translation](https://docs.djangoproject.com/en/6.1/topics/i18n/translation/#lazy-translation):
  `gettext_lazy` at module level.
- [Models](https://docs.djangoproject.com/en/6.1/ref/models/fields/#django.db.models.ForeignKey.related_name):
  `related_name`, default `<model>_set`; [`Meta.ordering`](https://docs.djangoproject.com/en/6.1/ref/models/options/#ordering)
  cost; [constraints](https://docs.djangoproject.com/en/6.1/ref/models/constraints/);
  [generic display views](https://docs.djangoproject.com/en/6.1/ref/class-based-views/generic-display/)
  for the `<app>/<model>_detail.html` template name; [URL namespaces](https://docs.djangoproject.com/en/6.1/topics/http/urls/#url-namespaces).
- [Cache framework](https://docs.djangoproject.com/en/6.1/topics/cache/): local-memory cache is
  per process; `add()`, `get_or_set()`; `cache_page` and `vary_on_cookie`; Redis backend.
- [Email testing](https://docs.djangoproject.com/en/6.1/topics/testing/tools/#email-services):
  the test runner uses the local-memory backend and `mail.outbox`.
- [Error views](https://docs.djangoproject.com/en/6.1/ref/views/#the-500-server-error-view):
  `500.html` rendered with an empty context; [logging](https://docs.djangoproject.com/en/6.1/topics/logging/):
  `django.request`, `django.security`.
- DRF [exceptions](https://www.django-rest-framework.org/api-guide/exceptions/): `APIException`,
  custom `EXCEPTION_HANDLER`.
- [Ruff `flake8-django` rules](https://docs.astral.sh/ruff/rules/#flake8-django-dj): DJ001 nullable
  string field, DJ007 `__all__` on a model form, DJ008 model without `__str__`.
- [Requests timeouts](https://requests.readthedocs.io/en/latest/user/advanced/#timeouts): no timeout
  by default; [HTTPX timeouts](https://www.python-httpx.org/advanced/timeouts/): five seconds by default.
- Celery [tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html): `bind`, `autoretry_for`,
  `retry_backoff` (cap `retry_backoff_max` 600, `retry_jitter` on; observed in
  `celery/app/autoretry.py` 5.7.0), `acks_late`, `reject_on_worker_lost`, idempotence, passing ids
  rather than objects, task names derived from the module; [workers](https://docs.celeryq.dev/en/stable/userguide/workers.html):
  time limits, `--max-tasks-per-child`, `--max-memory-per-child`, warm shutdown;
  [optimizing](https://docs.celeryq.dev/en/stable/userguide/optimizing.html): prefetch multiplier 1
  for long tasks; [routing](https://docs.celeryq.dev/en/stable/userguide/routing.html);
  [canvas](https://docs.celeryq.dev/en/stable/userguide/canvas.html): chords need a result backend;
  [Redis broker](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html):
  visibility timeout, one hour by default (observed in `kombu/transport/redis.py`);
  [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html): one beat,
  `timezone`.
- Celery's Django fixup (`celery/fixups/django.py`, 5.7.0) closes database connections before and
  after each non-eager task (observed in source); [`close_old_connections`](https://docs.djangoproject.com/en/6.1/ref/databases/#persistent-connections)
  for other long-running loops.
- [Django 6.1 `MAILERS`](https://docs.djangoproject.com/en/6.1/releases/6.1/) and `DB_CASCADE` without
  delete signals.

## Observed

- An environment variable set to the empty string: `os.environ.get`, `Env()("X", default=...)` both
  return `""`, `env.path("X", default=...)` returns the working directory, and `Path("")` resolves to
  the working directory.
- A view module with `class V(APIView)` and no import: `manage.py check` exits 1 with the
  `NameError` and its file and line; so do `migrate` and `makemigrations`.
- With `DEBUG = False` and `ALLOWED_HOSTS = ["app.example.com"]`, `Host: localhost` returns 400;
  with `SECURE_SSL_REDIRECT`, a plain request returns 301 to `https://`.
- With `SECURE_PROXY_SSL_HEADER` set, `X-Forwarded-Proto: http` (an inner proxy's `$scheme`) gives
  `is_secure()` false and `http://` from `build_absolute_uri()`; `https` gives `https://`.
- A DRF `ListAPIView` with only an owner object permission returned another user's row (200); the
  matching `RetrieveAPIView` returned 403. A view with no `permission_classes` answered anonymous
  requests (200).
- `select_for_update()` outside `atomic()`: no error on SQLite; no error on PostgreSQL inside a
  `django_db` test; `TransactionManagementError` on PostgreSQL under `django_db(transaction=True)`.
- `RunPython(forward)` with no reverse: `migrate <app> <previous>` raised `IrreversibleError`.
- `makemigrations --check` with a pending model change exited 1 and wrote no file.
- Under `django_db`, an `on_commit` callback did not run; with
  `django_capture_on_commit_callbacks(execute=True)` it did.

The empty-variable, missing-import, derived `is_staff`, health-check `Host` and inner-proxy
`X-Forwarded-Proto` traps were reported from a production Django deployment and reproduced above,
except the derived `is_staff` one, which is application code and is taught as a pattern.

Last checked: 2026-11-13, against the versions above.
