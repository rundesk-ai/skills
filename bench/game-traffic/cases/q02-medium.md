+++
skill = "game-traffic"
cases_version = 1
kind = "quality"
difficulty = "medium"
fixture = "town"
rubric = """
result.1  Finds that cars are removed silently after STUCK_TICKS (`_remove`), so spawned != arrived + active; counts every removal by reason, settles the trip, and adds an invariant or test that spawned == arrived + active + removed.
result.2  Finds that cars enter a junction without checking that the exit lane has room, then wait inside it while holding the junction (`inside` blocks every other car); reserves exit-lane space before a car may enter (block-the-box).
result.3  Restricts the stuck timer to cars that are at the head of their lane and cannot enter the next step, instead of any stopped car in a queue, and/or adds a deadlock (cycle) breaker so that removal is a last resort.
result.4  Reruns tools/bench_tick.py and reports arrived, unaccounted (now 0) and cars stuck in junctions before and after.
conduct.1 Reproduces the lock-up and the missing cars before changing code.
"""
+++
At rush hour (tools/bench_tick.py 3 1) the middle of town locks up, cars sit in intersections, and the trip statistics are wrong: hundreds of cars leave and never arrive, yet the streets are not full. Find out what is going on and fix it.
