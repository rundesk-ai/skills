+++
skill = "using-django"
cases_version = 1
kind = "quality"
difficulty = "easy"
fixture = "bookings"
rubric = """
result.1  Names the cause: User.save() sets is_staff from role on every save, so an is_staff=True set in the admin (or anywhere) on a member is overwritten.
result.2  The fix keeps an explicitly granted is_staff=True on a member after save and reload, while support and manager roles still get staff access; it does not answer "change their role instead" alone.
result.3  States what happens when a support or manager user is moved back to member (staff kept or revoked) and makes that a deliberate, tested choice.
result.4  Adds a test that sets is_staff=True on a member, saves, reloads and asserts it stuck, and keeps the role path tested; the existing tests still pass.
conduct.1 Reproduces the overwrite (a failing test or a shell check) before changing the model.
conduct.2 Runs the test suite and `manage.py check`, plus `makemigrations --check` if a field or model changed, and reports the results.
"""
+++
Support keeps complaining about the admin. When they open a user in the Django admin and tick
"Staff status" so a contractor can get in, it saves without an error, but when they reload the user
the box is unticked again and the contractor still can't log in to the admin. Fix it.
