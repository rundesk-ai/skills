extends Node2D

const COLONIST = preload("res://colonist/colonist.tscn")
const HOUSE = preload("res://art/house.png")

@export var map_size := Vector2i(128, 128)
@export var colonist_count := 2000

@onready var ground: TileMapLayer = $Ground
@onready var camera: Camera2D = $Camera2D

var selected := Vector2i(-1, -1)


func _ready() -> void:
	var rng := RandomNumberGenerator.new()
	rng.seed = 42
	for y in map_size.y:
		for x in map_size.x:
			var t := 0 if rng.randf() > 0.1 else 1
			ground.set_cell(Vector2i(x, y), 0, Vector2i(t, 0))
	for i in 200:
		var house := Sprite2D.new()
		house.texture = HOUSE
		house.offset = Vector2(0, -16)
		house.position = ground.map_to_local(_random_cell(rng))
		$Buildings.add_child(house)
	for i in colonist_count:
		var c := COLONIST.instantiate()
		c.cell = _random_cell(rng)
		$Colonists.add_child(c)
	camera.position = ground.map_to_local(map_size / 2)


func _random_cell(rng: RandomNumberGenerator) -> Vector2i:
	return Vector2i(rng.randi_range(0, map_size.x - 1), rng.randi_range(0, map_size.y - 1))


func _input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed:
		match event.button_index:
			MOUSE_BUTTON_LEFT:
				selected = ground.local_to_map(event.position)
				print("selected ", selected)
			MOUSE_BUTTON_WHEEL_UP:
				camera.zoom *= 1.1
			MOUSE_BUTTON_WHEEL_DOWN:
				camera.zoom /= 1.1
	elif event is InputEventMouseMotion and event.button_mask & MOUSE_BUTTON_MASK_RIGHT:
		camera.position -= event.relative / camera.zoom
