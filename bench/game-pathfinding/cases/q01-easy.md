+++
skill = "game-pathfinding"
cases_version = 1
kind = "quality"
difficulty = "easy"
fixture = "colony"
rubric = """
result.1  Finds that the heuristic is squared Euclidean distance, which overestimates the step costs, so A* returns non-shortest paths; replaces it with octile distance (or another admissible, consistent heuristic) in the same units as the step costs.
result.2  Finds that a neighbour is only updated when it has no g value yet (`if nxt not in g`), so a cheaper route found later is ignored; changes it to update when the new g is lower.
result.3  Adds a test that compares A* path cost with a plain Dijkstra (or brute-force) oracle on several maps or seeded random pairs, and asserts equality.
result.4  Disallows diagonal moves that cut past a blocked orthogonal neighbour, or explicitly states and justifies keeping corner cutting.
conduct.1 Demonstrates a suboptimal path (a failing oracle test or a printed counter-example) before fixing it.
"""
+++
Colonists keep taking routes that are obviously longer than they need to be, especially around the scattered rocks. Find out why and fix it so their routes are the shortest ones.
