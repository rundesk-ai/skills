# bookings

Room bookings for the shop's guest houses: a Django REST API, a Celery worker for email, and the
Django admin for support staff.

```sh
.venv/bin/python -m pytest -q        # dependencies are already installed in .venv
.venv/bin/python manage.py runserver
```

Production runs the Dockerfile on a container platform whose edge proxy terminates TLS; the web
container runs nginx (deploy/nginx.conf) in front of gunicorn. Settings come from the environment;
see .env.example.
