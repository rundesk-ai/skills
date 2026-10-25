+++
skill = "game-agent-behavior"
cases_version = 1
kind = "quality"
difficulty = "complex"
fixture = "settlement"
rubric = """
result.1  Stops every worker from re-deciding every tick: decisions happen when the task ends, on events, or on a staggered periodic check whose phase is derived from the worker id; the per-tick decision budget is counted in decisions, not milliseconds.
result.2  Protects hunger under that budget: a worker crossing into the dangerous band is decided immediately (bypassing the budget) or is otherwise guaranteed to reach food in time; a soak at scale shows no deaths beside reachable food.
result.3  Replaces whole-list scans for the nearest tree or food with a spatial index or per-region lists, and claims at selection with release on every exit path.
result.4  Adds a bounded per-worker decision trace with stable reason codes (for example no free tree, food out of reach, claimed by another worker), and uses it to answer "why is this worker idle".
result.5  Keeps the simulation deterministic: stable ordering and seeded randomness, and a test that the same seed gives the same results run twice.
result.6  Measures before and after at thousands of workers (time per tick, worst tick, deaths, wood, idle count) and states what remains unproven.
conduct.1 Reads the whole simulation and measures before restructuring.
"""
+++
We want settlements of 5,000 workers. At that size each tick takes far too long, workers starve while standing near food, and players keep asking why a particular worker is idle. Make the worker AI scale, keep them fed, and give us a way to explain any worker's choice. Show the evidence.
