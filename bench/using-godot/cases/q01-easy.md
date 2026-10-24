+++
skill = "using-godot"
cases_version = 1
kind = "quality"
difficulty = "easy"
fixture = "settlement"
rubric = """
result.1  Names the cause: `event.position` is in viewport (screen) coordinates, and `local_to_map` expects the TileMapLayer's local coordinates, so any camera pan or zoom picks the wrong cell.
result.2  Converts through the canvas transform: `ground.local_to_map(ground.get_local_mouse_position())`, or `ground.to_local(get_global_mouse_position())`, or the event made canvas-relative with `make_input_local`.
result.3  Moves the click from `_input` to `_unhandled_input` (or otherwise lets GUI consume clicks first), or says why it does not.
result.4  Proves it without a person clicking: a headless check that moves the camera, converts a known screen point and asserts the cell; or a precise manual check for the owner.
conduct.1 Runs the project headless after the change and checks the log for errors, not only the exit code.
"""
+++
Clicking a tile selects the wrong one as soon as I pan or zoom the camera. Fix selection.
