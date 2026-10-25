+++
skill = "game-traffic"
cases_version = 1
kind = "quality"
difficulty = "easy"
fixture = "town"
rubric = """
result.1  Finds that the time step is scaled by game speed (dt = BASE_DT * game_speed), so at 4x a car moves past its leader in one step; keeps a fixed dt and runs more steps per tick (with a cap) at higher game speeds.
result.2  Makes the follower's movement respect the gap: it never advances past the leader minus the car length (for example by clamping, or by computing all moves from the state before any car moves).
result.3  Adds a test that at 1x and 4x (and higher) the minimum gap never goes below zero, and that the same scenario gives the same trajectories at each speed within tolerance.
conduct.1 Reproduces the overlap (for example min_gap_m below zero from tools/bench_tick.py 3 4) before fixing it.
"""
+++
When the player runs the game at 4x speed, cars drive through each other. At normal speed it looks fine. Fix it.
