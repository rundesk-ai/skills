extends Sprite2D

var cell := Vector2i.ZERO
var _t := 0.0


func _process(delta: float) -> void:
	_t += delta
	if _t > 0.5:
		_t = 0.0
		cell += Vector2i(randi_range(-1, 1), randi_range(-1, 1))
	var ground = get_node("/root/Main/Ground")
	position = position.lerp(ground.map_to_local(cell), 0.2)
