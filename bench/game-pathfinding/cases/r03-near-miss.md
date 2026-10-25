+++
skill = "game-pathfinding"
cases_version = 1
kind = "routing"
fixture = "colony"
expect = "no-fire"
rubric = "Adds a hunger need and eating decision without loading the pathfinding skill; the work is deciding what a colonist wants, not how it gets there."
+++
Give colonists a hunger value that rises every tick, and when it passes a threshold they should stop what they are doing and go eat at the nearest food tile instead. Add food tiles to the world.
