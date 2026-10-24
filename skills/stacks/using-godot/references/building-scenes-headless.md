# Building scenes and resources without the editor

An agent has no editor window. It creates scenes, TileSets and other resources from a script run on the
command line, or writes the text files directly. Both work; each has traps that report success.

## A script that builds and saves a scene

A command-line script extends `SceneTree` (or `MainLoop`). An `EditorScript` cannot run from the command
line: "can only be instantiated by editor".

```gdscript
extends SceneTree

func _initialize() -> void:
	await process_frame                      # nothing is in the tree yet during _initialize
	var root := Node2D.new()
	root.name = "Map"                        # unnamed nodes save as "" or "@Sprite2D@2"
	var ground := TileMapLayer.new()
	ground.name = "Ground"
	ground.tile_set = load("res://world/terrain.tres")
	root.add_child(ground)
	for y in 64:
		for x in 64:
			ground.set_cell(Vector2i(x, y), 0, Vector2i(0, 0))
	_own_all(root, root)

	var scene := PackedScene.new()
	var err := scene.pack(root)
	if err == OK:
		DirAccess.make_dir_recursive_absolute("res://maps")
		err = ResourceSaver.save(scene, "res://maps/generated.tscn")
	print("SAVE ", error_string(err))
	root.free()
	quit(0 if err == OK else 1)


func _own_all(owner_node: Node, n: Node) -> void:
	for c in n.get_children():
		c.owner = owner_node
		if c.scene_file_path.is_empty():     # an instanced sub-scene: own its root, not its insides
			_own_all(owner_node, c)
```

```sh
"$GODOT" --headless --path . --import                                  # after adding any asset or class_name
"$GODOT" --headless --path . --quit-after 600 --script tools/build_map.gd
```

- **Set `owner` on every node to save, at every depth.** `pack()` saves only owned nodes, and a node
  without an owner is dropped **with its whole subtree**, even an owned grandchild — while `pack` and
  `save` both return `OK`. Prove the result by loading the saved scene in a separate run and asserting
  its node count and contents.
- **An instanced sub-scene is saved as a reference** to its `.tscn`: own its root only.
- **Only `CONNECT_PERSIST` connections to methods are saved**; lambdas never are. Connect in the scene's
  own `_ready` instead, or connect with the flag.
- **Wait a frame before relying on the tree**: during `_initialize` the root is not in the tree, `_ready`
  has not run, `update_internals()` does nothing and scene tiles do not instance. `_initialize` may be a
  coroutine. A `SceneTree._process` override must return a `bool`.
- A texture created at runtime (`ImageTexture.create_from_image`) has no path, so saving a resource that
  uses it embeds the pixels. Load the imported file instead to get a reference.
- **A plain `--script` save writes path references with no UIDs.** Running the same script with
  `--headless --editor --script` writes UIDs the way the editor does, but prints dozens of
  `ERROR: … leaked at exit` lines on quit; a smoke check grepping `ERROR:` must exclude them there.

## Writing `.tscn` and `.tres` by hand

```ini
[gd_scene format=3]

[ext_resource type="Script" path="res://main.gd" id="1"]
[ext_resource type="TileSet" path="res://world/terrain.tres" id="2"]

[node name="Main" type="Node2D"]
script = ExtResource("1")

[node name="Ground" type="TileMapLayer" parent="."]
tile_set = ExtResource("2")
```

- Exactly one root, with no `parent`; every other node's `parent` is a path from the root (`"."`,
  `"Unit"`, `"Unit/Arm"`). A `[sub_resource]` appears before anything that references it.
- `ext_resource` ids are any string. **Leave `uid=` out rather than invent one**: a wrong UID is only a
  warning (`invalid UID … using text path instead`), and a stale one silently points at whatever now has
  that UID. Grep the log for `invalid UID`.
- The editor rewrites the file on its next save: it drops comments, ordering and default values.
- An exported value written in the scene (`speed = 3.5`) is applied before `_ready`.

## A project from nothing

```ini
; project.godot
config_version=5

[application]
config/name="Colony"
run/main_scene="res://main.tscn"
config/features=PackedStringArray("4.7")
```

`config_version=5` and a name are enough to run `--script`, `--import` and `--editor`; `--import` does
not add anything to the file. Write every setting the project depends on explicitly — the physics engine
above all — rather than relying on what the editor's project manager would have written.

## Seeing what was built

A headless viewport has no pixels: `get_texture().get_image()` returns null. In a short windowed run,
wait for a drawn frame:

```gdscript
await RenderingServer.frame_post_draw
get_viewport().get_texture().get_image().save_png("user://shot.png")
```

Reading `get_pixel` from that image is a cheap automated check of draw order — whether a unit is in front
of or behind a wall. A release export does not run `--script`.

## Save games

- **Loading a `.tres` or `.res` that a player can replace runs code**: a save holding an embedded script
  executed it on `load()`. `str_to_var` and `ConfigFile` also build live objects from text, and
  `FileAccess.get_var(true)` deserializes objects with their code. Saves, mods and downloaded content are
  plain data — JSON, or `store_var` / `get_var` with objects off.
- JSON returns every number as a float and every key as a string; `JSON.from_native` / `to_native`
  (4.4+) or `store_var` keep ints and vectors exact.
- A process stopped from the editor never closes its files: `flush()` after each save, and write to a
  temporary file renamed over the old one.
