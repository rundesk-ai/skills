+++
skill = "using-php"
cases_version = 1
kind = "quality"
difficulty = "easy"
fixture = "billing"
rubric = """
result.1  Names the cause: `foreach ($this->lines as &$line)` leaves `$line` a reference to the last element, so the second, by-value `foreach` writes each line into that last element; the last line is lost and the one before it appears twice.
result.2  Fixes it so no reference outlives its loop (`unset($line)` after the loop, or no reference at all: `array_map`, a new array, or writing by key).
result.3  Notices that the export also rewrites the invoice's own `lines` (SKUs uppercased on the object) and stops the export mutating the invoice, or states that side effect and why it is kept.
result.4  Adds a test with at least three lines that asserts every row, and the suite passes.
conduct.1 Reproduces the wrong output (a failing test or a script) before changing the code.
conduct.2 Runs `php tests/run.php` and reports its output.
"""
+++
The accounting CSV export repeats one invoice line and drops the last one. Fix it.
