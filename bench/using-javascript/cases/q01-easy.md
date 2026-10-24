+++
skill = "using-javascript"
cases_version = 1
kind = "quality"
difficulty = "easy"
fixture = "orders"
rubric = """
result.1  Names the cause: binary floating point plus `toFixed`. 13.40 x 0.075 is stored just below 1.005, so `toFixed(2)` gives 1.00, while the total is rounded separately and comes out 14.41, so the lines do not add up.
result.2  Fixes it with integer cents (or another exact representation) and one explicit rounding rule applied once, so subtotal + tax = total on the invoice.
result.3  Adds a test with the reported case and at least one other half-cent case, and the suite passes.
conduct.1 Reproduces the wrong number before changing code.
conduct.2 Runs the tests and reports their output.
"""
+++
A customer's invoice shows a $13.40 subtotal, $1.00 tax at 7.5%, and a $14.41 total. Tax should be
$1.01, and the total doesn't even match the lines. Fix it.
