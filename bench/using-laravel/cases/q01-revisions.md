+++
skill = "using-laravel"
cases_version = 1
kind = "quality"
difficulty = "complex"
fixture = "shop"
steps = 3
setup = "composer install --no-interaction --prefer-dist -q && cp .env.example .env && php artisan key:generate -q"
arms = "bench/using-laravel/arms/q01-revisions"
rubric = """
Graded once, on the tree after all three steps, against the base. Each step was a fresh agent with no memory of the others. Every rule the steps need already has one home in the base, found by Laravel convention rather than by name.
R1  Step 1 lists orders with the existing Order::overdue() scope, not a restated status and due_at where clause.
R2  Step 1 shows each total through the total_with_vat_cents accessor; no VAT arithmetic or vat_bp read appears in a controller, view or new class.
R3  Step 1 decides the Cancel button with @can('cancel', ...) or the policy; the pending-and-owner-or-admin rule is not re-derived.
R4  Step 1 protects the page with the existing admin gate (can:admin, @can('admin') or Gate::authorize('admin')), not an inline is_admin check.
R5  Step 2 builds its CSV totals from total_with_vat_cents, not a new VAT calculation.
R6  Step 2 removes the old export and everything only it used: OrdersExportController (or its csv method), the orders.export route, the export-button partial or its old link, the export_wait (and replaced export_csv) translation keys, and the old export test, with nothing they alone used left behind.
R7  Step 3 shows the email total through total_with_vat_cents, not new VAT arithmetic in the mailable or its view.
R8  Across the steps, nothing was added that nothing reads: no unused view variable, appended accessor, event without a listener, config key, translation key, route or method.
R9  No migration was deleted or edited, and no status appears as a bare string where OrderStatus exists.
R10 `php artisan test` passes on the final tree.
"""
+++
## Step 1

Admins need a page listing every overdue order, with each order's total including VAT and a Cancel
button on the orders they're allowed to cancel. Put it under the admin area and add a test.

## Step 2

The CSV export times out for big customers. Replace it with a queued job that emails the customer the
CSV when it's ready; the button on the orders page should start the job and say the email is on its
way. Remove the old export.

## Step 3

Customers say the order confirmation email shows the wrong total. It should show the total including
VAT, the same as the order page.
