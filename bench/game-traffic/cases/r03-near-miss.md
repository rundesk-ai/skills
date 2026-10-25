+++
skill = "game-traffic"
cases_version = 1
kind = "routing"
fixture = "town"
expect = "no-fire"
rubric = "Writes a generic grid A* utility without loading the traffic skill: it is grid pathfinding for pedestrians, not road traffic."
+++
Add a module sim/walk.py with an A* search on a walkability grid so pedestrians can cut across the park. It does not touch roads or cars.
