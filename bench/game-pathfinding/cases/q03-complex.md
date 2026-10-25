+++
skill = "game-pathfinding"
cases_version = 1
kind = "quality"
difficulty = "complex"
fixture = "colony"
rubric = """
result.1  Routes path requests through a central queue spending a fixed per-tick budget counted in iterations or nodes, not milliseconds, and explains why a time budget breaks lockstep.
result.2  Makes the search deterministic and allocation-light: integer costs, a fixed neighbour order (not a set), a total-order tie-break ending in a stable cell index, and no per-search allocation of whole-map structures (generation stamps or preallocated arrays).
result.3  Rejects unreachable requests with reachability labels and repairs them locally on edits, and repaths only affected colonists, spread over ticks.
result.4  Proves determinism with a test: the same seed and commands run twice (and with requests issued in a different order, or with a worker count changed if threads are used) produce identical per-tick digests, using a stable digest rather than Python's salted hash() of strings.
result.5  Measures at scale (thousands of colonists) before and after, with counters such as searches per tick, nodes expanded and worst-tick time, and reports them.
result.6  Chooses speedups by fit and says why: does not cache whole start-to-goal paths, and uses flow fields or hierarchy only where the workload justifies them (shared goals, large static maps); names what remains unproven.
conduct.1 Reads the whole simulation before redesigning, and measures before choosing optimisations.
"""
+++
We want 5,000 colonists on a 512x512 map, and the game will run in lockstep multiplayer, so every machine must compute identical results. Right now pathfinding is the bottleneck by far. Rework pathfinding so it scales to that and stays deterministic, and show us the evidence.
