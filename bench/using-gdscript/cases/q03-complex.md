+++
skill = "using-gdscript"
cases_version = 1
kind = "quality"
difficulty = "complex"
fixture = "colony"
rubric = """
result.1  Finds that the simulation draws from the global RNG (`seed`, `randf`, `randi`), so anything else that draws from it, including a second world, changes this one; moves it to a `RandomNumberGenerator` owned by the world.
result.2  Saves and restores the generator's `seed` and `state`, so a loaded game continues on the same numbers.
result.3  Makes saved state round-trip exactly: integer fields come back as `int`, and floats survive (JSON.stringify drops precision unless `full_precision` is passed, or a binary or `var_to_str` format is used); the agent verifies this rather than assuming.
result.4  Adds tests that (a) two interleaved worlds with the same seed stay identical, and (b) saving at tick N, loading and running to tick M matches an uninterrupted run to M, compared by a digest that covers per-cell state, not just totals.
result.5  Shows at least one of those tests failing before the fix, or breaks the code on purpose and shows it fail.
result.6  States what remains unproven, such as whether float results match across platforms or engine versions.
conduct.1 Reads the whole simulation and save code before changing it, and runs the tests headless with the log checked for script errors.
"""
+++
We want replays: record a seed, and replay the game exactly, including after saving and loading in the
middle of a game. Make the simulation support that and prove it.
