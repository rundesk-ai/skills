+++
skill = "using-csharp"
cases_version = 1
kind = "quality"
difficulty = "easy"
fixture = "tycoon"
rubric = """
result.1  Names the cause: `Math.Round` rounds a midpoint to even by default, so 2.5 becomes 2.
result.2  Fixes it with an explicit rounding rule (`MidpointRounding.AwayFromZero`, or integer arithmetic on the rate such as basis points) and does not leave `Math.Round` with the default anywhere tax is computed.
result.3  Adds a test with midpoint cases (25 at 10% is 3; one more midpoint), and the existing tests still pass.
result.4  Says that a `double` rate can land just off a midpoint (0.1 is not exact), and either removes the floating-point step or states the remaining risk.
conduct.1 Runs `dotnet test` and reports its output, rather than claiming the fix works.
"""
+++
Accounting says tax on a $25 sale at 10% should be $3, but the game charges $2. Fix it.
