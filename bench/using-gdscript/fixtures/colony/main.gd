extends Node2D

var world

func _ready():
	world = World.new()
	world.generate(64, 64, 1234)

func _physics_process(_delta):
	world.tick()
