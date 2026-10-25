+++
skill = "game-agent-behavior"
cases_version = 1
kind = "routing"
fixture = "settlement"
expect = "fire"
rubric = "Loads the skill to replace the worker decision logic with utility scoring."
+++
Replace the if/else in Settlement.think with a utility AI: score eating and chopping for each worker and pick the best.
