+++
skill = "using-csharp"
cases_version = 1
kind = "quality"
difficulty = "medium"
fixture = "tycoon"
rubric = """
result.1  Finds that the RNG state is not saved: a loaded world restarts `new Random(seed)`, so it draws different numbers than the game that kept running. Saves the generator's state (or replaces it with a generator whose state is plain data) and restores it.
result.2  Finds that the job counter (`_nextJob`) is not saved, so new job ids collide with loaded ones and overwrite them.
result.3  Finds the culture bug: `double.Parse`/interpolation use the current culture, so a save written on an en-US machine reads a 0.1 tax rate as 1 on de-DE. Fixes writing and reading with the invariant culture (or stores the rate as an integer).
result.4  Makes processing order independent of dictionary history: equal-priority jobs are ordered by an explicit tie-break (job id), not by `List.Sort` (unstable) over dictionary enumeration order.
result.5  Adds a test that saves mid-game, loads, keeps stepping both worlds, and compares digests; and a test that loads under `de-DE`. Both fail before the fix and pass after.
conduct.1 Reproduces the divergence with a test before changing code.
conduct.2 Reports each cause separately, with what proves it fixed.
"""
+++
A replay loaded from a save drifts away from the original game after a few ticks, and our tester on a
German laptop says taxes go crazy after loading a save we sent them. The round-trip test passes. Find out
why and fix it.
