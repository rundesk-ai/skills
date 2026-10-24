+++
skill = "using-godot"
cases_version = 1
kind = "quality"
difficulty = "medium"
fixture = "settlement"
rubric = """
result.1  Measures before changing: frame or process time at 2,000 and 5,000 colonists (Performance monitors, `Time.get_ticks_usec`, or the profiler), and reports the numbers and how they were taken.
result.2  Removes the per-colonist per-frame cost: no `get_node("/root/...")` lookup every frame, and colonist movement driven by one manager on a tick rather than 5,000 `_process` callbacks.
result.3  Draws the colonists in a way that scales (one `MultiMeshInstance2D`, RenderingServer canvas items, or one `_draw` batch) or justifies keeping nodes with measured numbers.
result.4  Keeps what the player sees correct: colonists still move on the same cells, and draw order against houses is considered (y-sorting does not survive a MultiMesh unchanged).
result.5  Reports the after numbers at 5,000 and what was not measured (for example, GPU time in a headless run).
conduct.1 Takes the measurement first and changes the largest measured cost first.
"""
+++
We need 5,000 colonists on the map and it already struggles at 2,000. Make it run well.
