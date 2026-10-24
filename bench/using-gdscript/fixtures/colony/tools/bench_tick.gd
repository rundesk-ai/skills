extends SceneTree

func _initialize():
	var world = World.new()
	world.generate(256, 256, 99)
	var start = Time.get_ticks_usec()
	for i in 20:
		world.tick()
	var ms = (Time.get_ticks_usec() - start) / 1000.0 / 20.0
	print("TICK %.2f ms  digest %s" % [ms, world.digest()])
	quit()
