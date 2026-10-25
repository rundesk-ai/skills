+++
skill = "game-traffic"
cases_version = 1
kind = "quality"
difficulty = "complex"
fixture = "town"
rubric = """
result.1  Replaces distance-only routing fixed at spawn with a time-based cost that includes congestion (from measured speed or volume against capacity), plus a seeded per-car perturbation so equal routes share load, and uses the avenue's higher speed.
result.2  Adds rerouting that is damped: staggered by car id or blocked-route triggers, with a margin before switching, so traffic does not slosh between routes.
result.3  Fixes last-moment lane changes: the lane for the next turn is chosen when the car enters the road (looking ahead along its route), not in the last 10 m, and a car does not stop dead in its lane waiting to change.
result.4  Keeps cars from blocking junctions (exit-space reservation) and accounts for every car removed.
result.5  Scales: removes the per-step linear scans (`car in lane.cars`, `lane.cars.index`, `list.remove`) from the hot loop, keeps a fixed simulation step, and measures time per tick at much higher car counts before and after.
result.6  Keeps the run deterministic (seeded perturbation, stable order) with a test, and states what remains unproven.
conduct.1 Measures the current behaviour (route split, lane-change stops, tick time) before redesigning.
"""
+++
Players complain that everyone drives down the same streets while the fast two-lane avenue sits half empty, that cars stop dead in the avenue to change lanes right before turning, and the city will need ten times as many cars. Rework the traffic so routes spread sensibly, lane changes happen early, and it scales. Show the evidence.
