# Using PHP validation

The current record for `using-php`; the method is `prompts/benchmark-skill.md`, and the latest result is
in `bench/results/using-php/`.

The `billing` fixture is a small subscription billing service in plain PHP with a dependency-free test
runner (`php tests/run.php`). Its seeded defects were each reproduced before the cases were written: a
`foreach` by reference that duplicates a line in the CSV export; `modify('+1 month')` overflowing 31
January to 3 March, with an existing test that asserts the defect against the rule in `AGENTS.md`;
mutable `DateTime` shared between the issue date and the due date; unsalted `md5` compared with `==`
(a password of `240610708` accepts `QNKCDZO`); `ORDER BY` built from query parameters (a subquery runs);
`unserialize` on a cookie; and `include` built from `$_GET['page']` (a file outside `templates/` runs).

The `shop-laravel` fixture is a minimal Laravel-shaped project for the near-miss routing case, run with
both this skill and the Laravel skill deployed.

2026-10-24, Claude only: routing 3/3, near miss not fired. The skill did not load on the easy case; the
medium case was indistinguishable; on the complex case one skilled run wrote an injection test that
really fails on the vulnerable code. See the result's notes.
