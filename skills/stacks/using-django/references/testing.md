# Testing with pytest-django

This page covers how Django and pytest-django behave under test; which behaviour deserves a test is
a separate, framework-neutral decision.

## Setup

```ini
# pytest.ini, or [tool.pytest.ini_options] in pyproject.toml
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.test
addopts = --reuse-db
```

- Point tests at the production database engine when behaviour depends on it: locking, JSON
  queries, constraints, case sensitivity, transactions. SQLite passes code that fails on PostgreSQL.
- `--reuse-db` keeps the test database between runs; pass `--create-db` after a migration change.
  `--nomigrations` is faster but skips the migrations themselves, so CI should run at least once
  with them.
- A fast password hasher (`MD5PasswordHasher`) in test settings cuts user-creation time sharply.

## Database access

- A test touches the database only with `@pytest.mark.django_db` (or a fixture that requests `db`).
  The default wraps each test in a transaction that rolls back: fast, but `on_commit` callbacks never
  run and `select_for_update()` outside `atomic()` does not raise.
- `@pytest.mark.django_db(transaction=True)` truncates instead and commits for real. Use it for
  locking, `on_commit` ordering and code that opens its own connections; it is much slower.
- Capture `on_commit` callbacks in a normal test with the `django_capture_on_commit_callbacks`
  fixture (`execute=True` runs them), or `TestCase.captureOnCommitCallbacks`.

## Fixtures and factories

- Build data with factories or small fixture functions, not shared JSON fixtures that every test
  silently depends on.
- **A helper that creates a user should produce the same user the real code path does.** When
  `save()` derives fields (a role setting `is_staff`, a status setting a timestamp), a helper that
  sets the derived field directly is either overwritten, giving 403s that look like permission bugs,
  or tests a state production never reaches. Set the source field, then assert the derived one.
- `client` / `rf` / `admin_client` and DRF's `APIClient` with `force_authenticate()` cover most
  request tests. Send an allowed `Host` when a test overrides `ALLOWED_HOSTS`.

## Assertions that catch Django regressions

```python
def test_order_list_query_count(api_client, django_assert_num_queries, make_orders):
    make_orders(count=5, lines_each=3)
    with django_assert_num_queries(3):          # auth + orders + prefetched lines
        response = api_client.get("/api/orders/")
    assert response.status_code == 200
    assert len(response.json()["results"]) == 5
```

- Query counts with several rows, so an N+1 changes the number.
- Permissions from outside: anonymous, another user's object (404 or 403), and a list that excludes
  other users' rows.
- Migrations: `makemigrations --check` in CI; a data migration tested by migrating to the state before
  it, creating rows with `apps.get_model`, then migrating forward and back.
- `settings` fixture for per-test overrides; it reverts after the test.

## The gate

```sh
python manage.py check
python manage.py makemigrations --check
python -m pytest -q
```

Run the narrowest test first (`pytest path/to/test_file.py::test_name`), then the full gate.
