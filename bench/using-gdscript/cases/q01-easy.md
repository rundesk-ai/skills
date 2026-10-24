+++
skill = "using-gdscript"
cases_version = 1
kind = "quality"
difficulty = "easy"
fixture = "colony"
rubric = """
result.1  Names the cause: `JSON.parse_string` returns every number as a float and every object key as a String, so building ids no longer match (`'5.0'` key errors) and `match` on `1`/`2` never matches a float level.
result.2  Fixes the load so ids, levels, food and building references come back as `int` (explicit `int()` conversion, or a format that keeps types such as `var_to_str`/`str_to_var` or `FileAccess.store_var`), without changing the save's meaning.
result.3  Extends the tests so a loaded world keeps ticking without errors and upgrades buildings, and the run is checked for `SCRIPT ERROR` rather than trusted on exit code.
result.4  Types the code it touches (`int`, `float`, typed parameters and returns) where that would have caught the mix-up.
conduct.1 Runs the project headless and reads the log before and after the fix.
"""
+++
After loading a save nothing grows any more and buildings never upgrade, and the output fills with
errors. Fix loading.
