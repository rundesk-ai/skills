+++
skill = "game-pathfinding"
cases_version = 1
kind = "quality"
difficulty = "medium"
fixture = "colony"
rubric = """
result.1  Finds that an unreachable goal (across the river) makes A* flood the whole reachable area, and that the colonist retries it every tick; adds a reachability check (connected-component labels or region labels) that rejects the request before searching, with the labels updated when the map is edited.
result.2  Bounds every search (a node or iteration budget) and reports the failure to the caller instead of silently retrying every tick (a failure status, a retry delay, or cancelling the order).
result.3  Finds that any edit sends every colonist to search again in the same tick; repaths only colonists whose remaining path is affected, and/or spreads repaths over ticks through a queue or per-tick budget.
result.4  Measures with tools/bench_tick.py before and after and reports the change in total and worst-tick time.
result.5  Adds tests: an unreachable goal returns quickly without exploring the map, and placing a wall leaves unaffected colonists' paths alone.
conduct.1 Reproduces the hitch with the bench tool before changing code.
"""
+++
The game hitches badly: when colonists are sent somewhere across the river, and every time the player builds a wall, ticks take hundreds of milliseconds. tools/bench_tick.py shows it. Fix the hitching without breaking normal movement.
