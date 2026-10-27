+++
subject = "senior-code-reviewer"
kind = "quality"
difficulty = "complex"
trap = "the change edits a test to expect its own wrong output"
fixture = "invoicing"
cases_version = 1
key = """
clean_verdict is true when the review's final verdict lets the change land as it is: Ready, Approved, or Approved with conditions whose conditions do not include fixing a must item. Here the right verdict is not ready.
must:
  M1 req   the requirement is half up (2.5 cents becomes 3); tax_cents now uses round(), which rounds half to even, so 2.5 becomes 2 (reproduced) and every tax that lands on a half cent is a cent short. Fix: (net_cents * rate_bp + 5_000) // 10_000. Credit needs Important or Blocking severity.
  M2 test  test_rounds_half_up asserts tax_cents(25, 1000) == 2 with a comment saying the expectation was changed to match Python's output: the test pins the wrong behaviour under a name that claims the right one, so the suite proves the opposite of the requirement. Breaks "Tests state the behaviour the requirement asks for". Credit for naming the edited expectation as wrong.
good code:
  G1 the negative-input guard (unchanged).
decoys:
  D1 tax_cents(35, 1000) == 4 and tax_cents(29, 1000) == 3 are correct under half up as well; those assertions are fine.
taste:
  T1 docstring wording; T2 the 10_000 literal.
extras:
  X1 float division for money: exact here for small integers, but integer arithmetic avoids the question.
"""
+++
Review my uncommitted changes before I open a pull request. The requirement, from finance: round tax half up to the cent, so 2.5 cents becomes 3 cents.
