class_name SaveGame
extends RefCounted


static func write(world, path):
	var data = {
		"width": world.width,
		"height": world.height,
		"day": world.day,
		"next_id": world.next_id,
		"cells": [],
		"buildings": {},
		"colonists": world.colonists,
	}
	for c in world.cells:
		var cell = world.cells[c]
		data["cells"].append([c.x, c.y, cell["fertility"], cell["food"], cell["building"], cell["level"]])
	for id in world.buildings:
		var b = world.buildings[id]
		data["buildings"][id] = {"x": b["cell"].x, "y": b["cell"].y, "type": b["type"], "level": b["level"], "progress": b["progress"]}
	var f = FileAccess.open(path, FileAccess.WRITE)
	f.store_string(JSON.stringify(data))


static func read(path):
	var f = FileAccess.open(path, FileAccess.READ)
	var data = JSON.parse_string(f.get_as_text())
	var world = World.new()
	world.width = data["width"]
	world.height = data["height"]
	world.day = data["day"]
	world.next_id = data["next_id"]
	for row in data["cells"]:
		world.cells[Vector2i(row[0], row[1])] = {"fertility": row[2], "food": row[3], "building": row[4], "level": row[5]}
	for id in data["buildings"]:
		var b = data["buildings"][id]
		world.buildings[id] = {"cell": Vector2i(b["x"], b["y"]), "type": b["type"], "level": b["level"], "progress": b["progress"]}
	world.colonists = data["colonists"]
	return world
