+++
skill = "using-gdscript"
cases_version = 1
kind = "quality"
difficulty = "medium"
fixture = "colony"
rubric = """
result.1  Runs `tools/bench_tick.gd` before changing anything and reports the baseline time and digest.
result.2  Replaces the per-cell Dictionaries keyed by `Vector2i` with flat typed storage (`PackedInt32Array`/`PackedFloat32Array` or typed arrays indexed by `y * width + x`), and removes per-iteration allocation such as the `[-1, 0, 1]` literals and `cells.keys()`.
result.3  Types the hot code (typed locals, parameters, returns, typed loop variables) and avoids repeated dictionary lookups in the inner loop; may precompute which cells are next to farms instead of recomputing every tick.
result.4  Proves results are unchanged: the digest (or a stronger comparison) matches the baseline for the same seed, or the agent explains exactly why it differs. Reports the new time and the speed-up.
result.5  Keeps saving and the tests working (`tests/run_tests.gd` prints `TESTS OK`).
conduct.1 Measures first, changes second, measures again.
"""
+++
On a 256x256 map one simulation tick takes far too long. Make it at least three times faster without
changing what the simulation produces.
