+++
skill = "using-django"
cases_version = 1
kind = "routing"
fixture = "invoices"
expect = "no-fire"
rubric = "Writes the Alembic migration and model change without loading the Django skill."
+++
Add a nullable paid_at column to invoices with a migration, and backfill it from the latest payment
for each fully paid invoice. Keep the downgrade working.
