# Settings and deployment

## Environment variables

Read every deploy-specific value from the environment, with one helper that decides what "unset"
means. An orchestrator or `.env` file that declares a variable with no value sets it to the empty
string, and `os.environ.get("X", default)`, `environ.Env()("X", default=...)` and `env.path(...)` all
return `""` (or the working directory) rather than the default.

```python
# Bad: MEDIA_ROOT="" gives Path(""), which is the working directory.
MEDIA_ROOT = Path(env("MEDIA_ROOT", default="/srv/media"))

# Good: empty means unset, and a path must be absolute.
def env_path(name: str, default: str) -> Path:
    value = os.environ.get(name, "").strip() or default
    path = Path(value)
    if not path.is_absolute():
        raise ImproperlyConfigured(f"{name} must be an absolute path, got {value!r}")
    return path

MEDIA_ROOT = env_path("MEDIA_ROOT", "/srv/media")
```

The same applies to hosts, origins and URLs: `"".split(",")` is `[""]`, not `[]`. Fail at start-up
on a missing secret (`SECRET_KEY`, database URL) instead of falling back to a development value;
a production process running on a default key or SQLite file looks healthy until data is lost.
Prove it: start the app with the variable empty and with it absent, and assert the resolved value.

Keep one settings module per environment only when they differ in more than values; otherwise one
module that reads the environment, with `DEBUG` defaulting to off.

## Security settings

Run `python manage.py check --deploy` with the production settings module and resolve or justify
every warning. The settings it covers are the floor: `DEBUG = False`, a real `SECRET_KEY`,
`ALLOWED_HOSTS`, `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`,
`SECURE_HSTS_SECONDS` (start small; browsers cache it). `CSRF_TRUSTED_ORIGINS` entries need the
scheme (`https://app.example.com`). Django 6.0 adds a built-in Content Security Policy
(`SECURE_CSP` with `ContentSecurityPolicyMiddleware`); prefer it to a third-party package on 6.0+.

## Behind a reverse proxy

Django sees the proxy, not the browser. Two settings decide what it believes:

- **`SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")`** makes `request.is_secure()`
  trust that header. Set it only when the proxy always sets or strips it, or a client can claim
  HTTPS. With two proxies (a TLS-terminating edge, then nginx in the container), an inner
  `proxy_set_header X-Forwarded-Proto $scheme;` reports `http`, because the inner hop is plain HTTP.
  Django then builds `http://` absolute URLs, and with `SECURE_SSL_REDIRECT` it can redirect in a
  loop. The inner proxy must pass the outer value through:

  ```nginx
  # inner nginx, behind a TLS-terminating proxy
  proxy_set_header X-Forwarded-Proto $http_x_forwarded_proto;
  proxy_set_header Host $host;
  ```

  Prove it: `request.build_absolute_uri()` from a deployed debug endpoint or a DRF hyperlinked
  response shows `https://`.
- **`USE_X_FORWARDED_HOST`** only when the proxy rewrites `Host`; otherwise pass `Host` through
  and list the public names in `ALLOWED_HOSTS`.

## Health checks

With `DEBUG = False`, a request whose `Host` is not in `ALLOWED_HOSTS` gets 400 (`DisallowedHost`),
and with `SECURE_SSL_REDIRECT` a plain-HTTP request gets 301. A container health check that calls
`http://localhost:8000/` therefore fails on a healthy app. Send an allowed `Host` and the forwarded
scheme, and use Python, because slim images ship without curl or wget:

```sh
python -c "import urllib.request as u; u.urlopen(u.Request('http://127.0.0.1:8000/healthz', headers={'Host': 'app.example.com', 'X-Forwarded-Proto': 'https'}), timeout=3)"
```

Keep `/healthz` cheap: it proves the process answers and, if the platform restarts on failure,
should not depend on a database that a restart cannot fix. A separate readiness check may query it.

## gunicorn

- Start with `gunicorn config.wsgi --bind 0.0.0.0:8000 --workers <2 x cores + 1, capped by memory>`
  and an explicit `--timeout`; a request longer than the timeout kills the worker mid-write.
- Log to stdout (`--access-logfile -`), and let the platform collect it.
- Do not run `migrate` or `collectstatic` inside the worker command; do them once per release.

## Static and media files

- `STATIC_ROOT` is where `collectstatic` writes; `STATICFILES_DIRS` are sources. They must differ.
- With `DEBUG = False`, Django serves neither static nor media files. Serve static with the proxy or
  WhiteNoise, and media from the proxy or object storage on a persistent volume, never from the
  container's writable layer, which a redeploy discards.
- Manifest storage (`ManifestStaticFilesStorage`, WhiteNoise's compressed variant) makes
  `collectstatic` fail on a CSS reference to a missing file and makes `{% static %}` raise for a file
  not in the manifest. Run `collectstatic --noinput` in the build and fail the build on error.
- Configure storage through `STORAGES` (Django 4.2+); `DEFAULT_FILE_STORAGE` and
  `STATICFILES_STORAGE` are gone in 5.1.
- Never trust an uploaded file name or content type; validate size and type, and serve user uploads
  from another origin or with `Content-Disposition: attachment` when they may be HTML or SVG.

## Release steps

Run once per release, before new code takes traffic: `migrate --noinput`, then start the new
workers. `collectstatic` belongs in the image build when the output ships in the image. Two code
versions run against one schema during a rolling deploy, so every migration must work with the old
code still running; read the migrations reference for the expand-then-contract order.

## Workers and scheduled tasks

Run Celery workers and one beat from the same image and settings as the web process, restart them on
every deploy, and give the platform a stop timeout longer than the longest task. Read
[tasks and workers](tasks-and-workers.md) for task design, retries, time limits and scheduling.
