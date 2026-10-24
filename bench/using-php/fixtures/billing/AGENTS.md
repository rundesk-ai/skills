# Billing

A small subscription billing service in plain PHP, no framework. `public/index.php` is the front
controller; `src/` holds the code under the `App\` namespace.

- Test: `php tests/run.php`.
- Money is held in integer cents.
- A subscription renews on the same day of the next month, or on the last day of that month when the
  day does not exist there; it keeps the day it started on (a subscription started on the 31st renews
  on the 31st whenever the month has one).
