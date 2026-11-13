+++
skill = "using-django"
cases_version = 1
kind = "quality"
difficulty = "medium"
fixture = "bookings"
rubric = """
result.1  The list returns only the requesting user's bookings, filtered in get_queryset() (or an equivalent queryset filter), not by an object permission alone; a test proves another member's booking is absent.
result.2  Cancelling another user's booking returns 404 or 403, enforced on the server through the filtered queryset or an object permission reached through get_object(); a test proves it.
result.3  A second or concurrent cancel cannot refund twice: a select_for_update() inside transaction.atomic(), or a conditional update that checks the status and the rows affected; a repeat cancel returns a 4xx and creates no second Refund.
result.4  The refund email is enqueued with the booking id from transaction.on_commit (or after the transaction commits), not inside the open transaction.
result.5  Notices that BookingSerializer uses fields = "__all__", so a client creating a booking can set status, refunded_cents or amount, and fixes it or flags it explicitly.
result.6  Tests cover: own bookings only, the repeat cancel, and that the email task is enqueued (on_commit callbacks captured or executed, or delay mocked); and the answer says that a SQLite test cannot prove a row lock, or uses a transactional test.
conduct.1 Runs the test suite and `manage.py check` (and `makemigrations --check` if models changed) and reports the results.
conduct.2 Adds no dependency.
"""
+++
Members need to see their own bookings and cancel one from the app. Add an endpoint that lists the
logged-in member's bookings, and one that cancels a booking: it refunds the full amount (record a
Refund, set refunded_cents, mark it cancelled) and emails the guest with the send_refund_email task.
Support says guests double-tap the cancel button a lot, so make sure nobody gets refunded twice.
Add tests.
