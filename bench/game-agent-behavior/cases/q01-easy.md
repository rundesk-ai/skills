+++
skill = "game-agent-behavior"
cases_version = 1
kind = "quality"
difficulty = "easy"
fixture = "settlement"
rubric = """
result.1  Finds that a tree is only marked taken when a worker arrives, so several workers choose the same nearest tree; claims the tree when the worker chooses it, before walking, with the claimant's id.
result.2  Releases the claim when the tree is felled and on every other exit from the task (re-selection, eating, death), not only on success.
result.3  Adds a test: several workers and fewer trees in one tick give at most one claimant per tree, and no worker turns back.
conduct.1 Reproduces the convergence in a test or a printed trace before fixing it.
"""
+++
At the start of a game, several workers walk to the same tree and all but one turn back when they get there. Fix it so each tree gets one worker.
