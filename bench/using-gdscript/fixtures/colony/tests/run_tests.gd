extends SceneTree

var failures = 0

func check(cond, what):
	if not cond:
		failures += 1
		printerr("FAIL ", what)

func _initialize():
	var a = World.new()
	a.generate(16, 16, 5)
	for i in 50:
		a.tick()
	var b = World.new()
	b.generate(16, 16, 5)
	for i in 50:
		b.tick()
	check(a.digest() == b.digest(), "same seed, same world")

	var w = World.new()
	w.generate(16, 16, 5)
	for i in 5:
		w.tick()
	SaveGame.write(w, "user://test_save.json")
	var loaded = SaveGame.read("user://test_save.json")
	check(loaded.day == w.day, "day survives a save")
	check(loaded.buildings.size() == w.buildings.size(), "buildings survive a save")

	print("TESTS OK" if failures == 0 else "TESTS FAILED %d" % failures)
	quit(1 if failures else 0)
