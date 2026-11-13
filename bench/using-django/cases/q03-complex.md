+++
skill = "using-django"
cases_version = 1
kind = "quality"
difficulty = "complex"
fixture = "bookings"
setup = "sed -i.orig '/^from rest_framework.views import APIView$/d' bookings/reports.py && rm bookings/reports.py.orig"
rubric = """
result.1  Restores the missing APIView import in bookings/reports.py, and adds `manage.py check` (or an equivalent import check) to CI so a broken URLconf fails fast with its file and line.
result.2  MEDIA_ROOT: sees that .env.example sets MEDIA_ROOT to empty, that an empty value reaches env() as "" rather than the default, and that Path("") is the working directory, so uploads would land in /app inside the container instead of the volume; makes settings treat empty as unset or refuse a non-absolute path.
result.3  Health check: sees that python:3.13-slim has no curl and that, with DEBUG off, a request to localhost fails ALLOWED_HOSTS (400) or the SSL redirect (301); replaces it with a probe that works, such as Python urllib sending an allowed Host (and X-Forwarded-Proto https when the redirect is on).
result.4  Proxy: sees that the inner nginx sends X-Forwarded-Proto $scheme, which is http behind the TLS edge, so with SECURE_PROXY_SSL_HEADER Django treats every request as insecure (http absolute URLs, a redirect loop with SECURE_SSL_REDIRECT); passes the edge's header through.
result.5  DRF exposure: flags that DEFAULT_PERMISSION_CLASSES is unset (so the default is AllowAny) or that BookingSerializer's fields = "__all__" lets a client set status and refunded_cents, and fixes at least one.
result.6  Flags the RunPython in bookings 0002 that has no reverse (IrreversibleError on rollback) and adds RunPython.noop or a reverse.
result.7  Flags that a missing DJANGO_SECRET_KEY silently falls back to a development key, and runs or recommends `manage.py check --deploy` with production settings.
conduct.1 Runs the test suite and `manage.py check` after the changes and reports the results.
conduct.2 Separates what it fixed in the repository from what ops must do on the platform.
"""
+++
We're putting bookings into production next week on our container platform: its edge proxy does
TLS, then traffic goes to our nginx and gunicorn in the web container, and media goes on a mounted
volume. Last night's merge of the reporting branch went in and CI is red. Get main green, then go
through what is going to bite us in the deploy. Fix what's clearly wrong in the repo and give me a
list of the rest for ops.
