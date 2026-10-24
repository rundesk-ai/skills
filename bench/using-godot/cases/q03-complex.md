+++
skill = "using-godot"
cases_version = 1
kind = "quality"
difficulty = "complex"
fixture = "settlement"
rubric = """
result.1  Writes a script runnable from the command line (`--headless --script`, extending SceneTree or MainLoop) that builds the map and saves it as `res://maps/generated.tscn`.
result.2  Sets `owner` on every node to be saved, including nodes added under other nodes, before `PackedScene.pack`; checks the `Error` returned by `pack` and `ResourceSaver.save`, and makes the directory first.
result.3  The saved scene references the existing TileSet resource rather than embedding a copy, and the painted cells are saved in the TileMapLayer.
result.4  Proves it: loads the saved scene in a separate run and asserts the node count and the number of used cells, and checks the log for errors rather than trusting the exit code.
result.5  Handles a clean checkout: runs `--import` first, or explains that the import cache is needed for the TileSet's texture and `class_name`s.
result.6  Says what it could not check headlessly (how the map looks) and how the owner can see it.
conduct.1 Reads the existing scene, TileSet and map-building code before writing the generator.
"""
+++
We want to generate maps in CI. Write something that builds a map like the one main.gd makes and saves
it as a scene file we can open in the editor, and prove it works without opening the editor.
