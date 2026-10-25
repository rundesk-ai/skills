+++
skill = "game-agent-behavior"
cases_version = 1
kind = "quality"
difficulty = "medium"
fixture = "settlement"
rubric = """
result.1  Finds that a tree stays `taken` forever when its chopper dies (Settlement.kill) or switches to eating mid-chop, so nobody can work it; releases claims on every exit path, including death, and resets progress correctly.
result.2  Finds that claims are only made on arrival, so workers also converge on one tree; claims at selection.
result.3  Adds an invariant or test that every claimed tree's claimant is alive and currently assigned to it, and a test that kills or interrupts a worker mid-chop and shows the tree gets felled by someone else.
result.4  Reruns tools/bench_tick.py and reports that trees_taken_but_unworked drops to 0 and idle workers fall, with wood produced before and after.
conduct.1 Reproduces the idle-beside-work state before changing code.
"""
+++
In longer games, more and more workers stand around idle even though there are plenty of trees left, and the number of trees chopped per hour drops. tools/bench_tick.py shows it. Find out why and fix it.
