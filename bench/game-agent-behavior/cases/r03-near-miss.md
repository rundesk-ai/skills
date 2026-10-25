+++
skill = "game-agent-behavior"
cases_version = 1
kind = "routing"
fixture = "settlement"
expect = "no-fire"
rubric = "Changes only how workers move between tiles, without loading the agent-behaviour skill: route search around obstacles is movement, not decisions."
+++
Add rocks to the map that workers cannot walk through, and make step_toward route around them with A* instead of walking straight.
