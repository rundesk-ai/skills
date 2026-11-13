# Django REST Framework

## Views

- Prefer generic views or viewsets that already match the endpoint; override `get_queryset()`,
  `get_serializer_class()` and `perform_create()` rather than rewriting `get()` and `post()`.
- `get_queryset()` is the authorization boundary for lists and the place query counts are fixed:
  filter it to the requesting user's rows and add `select_related` / `prefetch_related` there.
  The class-level `queryset` cannot see the request, so per-user filtering never belongs there.
- Keep `perform_create()` and `perform_update()` to one call into a domain function, passing
  `serializer.validated_data` and `request.user`. Business rules in a serializer's `create()` are
  unreachable from a management command, a task or the admin.
- After a merge or refactor, `python manage.py check` imports every view; a missing `APIView`
  import otherwise surfaces as 500 on every URL.

## Serializers

- List fields explicitly. `fields = "__all__"` publishes and accepts every column added later.
- Mark server-owned fields `read_only_fields` (owner, status, totals, timestamps); otherwise a client
  can set them. Set ownership in `perform_create(serializer.save(owner=self.request.user))`.
- Field-level rules in `validate_<field>()`, cross-field rules in `validate()`, raising
  `serializers.ValidationError`. Uniqueness that matters is also a database constraint;
  serializer validators race.
- `serializer.data` before `is_valid()` or after a failed one is not validated input. Read
  `validated_data`.
- Use separate serializers for input and output when they differ, rather than one with many
  conditional fields.
- `SerializerMethodField` and nested serializers run per row; check they read prefetched data.
- Writable nested serializers need an explicit `create()` / `update()`; DRF does not save nested
  data by default and raises to say so.

## Permissions

- Set `DEFAULT_PERMISSION_CLASSES` (and `DEFAULT_AUTHENTICATION_CLASSES`) in `REST_FRAMEWORK`. The
  default is `AllowAny`, so any view that forgets `permission_classes` is public.
- `has_permission()` runs on every request; `has_object_permission()` runs only when the view calls
  `get_object()` (or `check_object_permissions()` yourself in an override). Generic list views never
  call it, so an object permission alone on a list returns every row. Filter the queryset.
- Compose with `&`, `|` and `~` instead of writing a combined class.
- Return 404 rather than 403 for another user's object when its existence is itself private;
  filtering `get_queryset()` does that for free.
- Test each permission from the outside: an anonymous request, another user's object, and a list
  that must not contain other users' rows.

## Authentication

- Session authentication enforces CSRF for unsafe methods; token and JWT authentication do not.
  A browser client on session auth needs the CSRF token, and `CSRF_TRUSTED_ORIGINS` when it calls
  from another origin.
- DRF's `TokenAuthentication` stores one non-expiring token per user in plain text; prefer a
  maintained package with expiry and hashing, or sessions for a first-party browser client.
- `WWW-Authenticate` decides whether an unauthenticated request gets 401 or 403: the first
  authentication class sets it. Session auth alone yields 403.

## Throttling and pagination

- Set `DEFAULT_PAGINATION_CLASS` and `PAGE_SIZE`; an unpaginated list grows with the table.
- Throttles use the cache; with the default local-memory cache each gunicorn worker counts
  separately. Use a shared cache in production, and remember throttling is not a security control
  against a determined client.
- `ScopedRateThrottle` per sensitive endpoint (login, password reset) rather than one global rate.
