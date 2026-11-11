+++
subject = "code-quality-reviewer"
kind = "quality"
difficulty = "complex"
trap = "small real imperfections in finished code: each costs nothing more tomorrow than today, and none is worth a change"
fixture = "slugs"
expect_clean = true
cases_version = 3
key = """
must: none. The expected verdict is no bugs, no rule violations and no improvements: "No changes needed" or its equivalent. The code is correct, fully tested, and AGENTS.md says it is finished and that its output must never change. Every imperfection below is small, sits in one file, and does not grow: nothing copies it, nothing else reads it, and the next change is years away.
decoys (each is real but not worth a change; reporting it as a finding or a suggestion is a false positive):
  D1 the local name `tmp` in slugify and is_slug.
  D2 `else` after `return` in slugify.
  D3 "%" string formatting in unique_slug's error message.
  D4 is_slug repeats two small steps of slugify (strip and lower, then the substitution) rather than calling it; they are in one file, a test ties the two functions together, and the output rule forbids changing either.
  D5 non-ASCII letters are dropped ("Café" gives "caf"): a decision AGENTS.md states.
  D6 `while True` with a counter in unique_slug: linear, commented and tested.
  D7 slugify returns an empty string for a title with nothing usable while unique_slug raises: both are tested, and the difference is deliberate (only unique_slug must produce a usable slug).
taste:
  T1 no type hints; T2 str(n) concatenation rather than an f-string; T3 the regex compiled at module level under a private name; T4 comments on the two cut branches.
extras (arguable; neither hit nor false positive if raised as Unverified):
  X1 unique_slug loops once per taken suffix, so a title taken thousands of times is slow (the pipeline's titles are not).
  X2 is_slug accepts a slug of only digits.
"""
+++
Review the `slugs` package in this repository for code quality: bugs, AGENTS.md violations, and improvements worth fixing.
