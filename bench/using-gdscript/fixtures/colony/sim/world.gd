class_name World
extends RefCounted

enum Building { NONE, HOUSE, FARM, MILL }

var width = 0
var height = 0
var cells = {}        # Vector2i -> {"fertility": float, "food": int, "building": int, "level": int}
var buildings = {}    # id -> {"cell": Vector2i, "type": int, "level": int, "progress": int}
var colonists = []    # {"id": int, "home": int, "hunger": float}
var day = 0
var next_id = 1


func generate(w, h, seed_value):
	seed(seed_value)
	width = w
	height = h
	for y in h:
		for x in w:
			cells[Vector2i(x, y)] = {"fertility": randf(), "food": 0, "building": Building.NONE, "level": 0}
	for i in (w * h) / 40:
		var c = Vector2i(randi() % w, randi() % h)
		place(c, Building.FARM if i % 3 else Building.HOUSE)
	for i in (w * h) / 20:
		colonists.append({"id": i, "home": 1 + randi() % buildings.size(), "hunger": 0.0})


func place(cell, type):
	if cells[cell]["building"] != Building.NONE:
		return
	var id = next_id
	next_id += 1
	buildings[id] = {"cell": cell, "type": type, "level": 1, "progress": 0}
	cells[cell]["building"] = id


func tick():
	day += 1
	# Crops grow on every farmed cell and its neighbours.
	for c in cells.keys():
		var cell = cells[c]
		var near = 0
		for dy in [-1, 0, 1]:
			for dx in [-1, 0, 1]:
				var n = c + Vector2i(dx, dy)
				if cells.has(n) and cells[n]["building"] != Building.NONE:
					var b = buildings[cells[n]["building"]]
					if b["type"] == Building.FARM:
						near += 1
		if near > 0:
			cell["food"] += int(near * cell["fertility"] * 3)
	# Colonists get hungry and eat from the cell under their home.
	for col in colonists:
		col["hunger"] += 0.1 + randf() * 0.05
		var home = buildings[col["home"]]
		var cell = cells[home["cell"]]
		if col["hunger"] > 1.0 and cell["food"] > 0:
			cell["food"] -= 1
			col["hunger"] = 0.0
	# Buildings upgrade.
	for id in buildings:
		var b = buildings[id]
		b["progress"] += 1
		match b["level"]:
			1:
				if b["progress"] >= 10:
					b["level"] = 2
			2:
				if b["progress"] >= 30:
					b["level"] = 3
			3:
				pass


func food_total():
	var total = 0
	for c in cells:
		total += cells[c]["food"]
	return total


func digest():
	return "%d:%d:%d:%d" % [day, food_total(), buildings.size(), colonists.size()]
