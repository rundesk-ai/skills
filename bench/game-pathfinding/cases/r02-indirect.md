+++
skill = "game-pathfinding"
cases_version = 1
kind = "routing"
fixture = "colony"
expect = "fire"
rubric = "Loads the skill though the request never says pathfinding: colonists ordered somewhere they cannot reach make every tick slow."
+++
When I order a colonist to a spot on the far side of the river the whole colony crawls, and it never recovers until I cancel the order. Make that stop.
