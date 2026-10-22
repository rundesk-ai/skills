# Syntax from elsewhere

Most generated GDScript errors are code from Godot 3 or from Python. Godot 3 code often parses under a
different meaning or fails with an error far from the cause; Python code mostly fails to parse.

## Godot 3 → Godot 4

| Godot 3 | Godot 4 |
|---|---|
| `tool`, `export var`, `onready var` | `@tool`, `@export var`, `@onready var` |
| `export(int, 0, 10) var x` | `@export_range(0, 10) var x: int` |
| `var x setget set_x, get_x` | `var x: int:` with `set(value):` and `get:` blocks |
| `yield(obj, "signal")` | `await obj.signal` |
| `connect("sig", self, "_m", [arg])` | `sig.connect(_m.bind(arg))` |
| `emit_signal("sig", v)` | `sig.emit(v)` |
| `funcref(obj, "m")` | `obj.m` or `Callable(obj, "m")` |
| `scene.instance()` | `scene.instantiate()` |
| `get_tree().change_scene("res://x.tscn")` | `get_tree().change_scene_to_file("res://x.tscn")` |
| `KinematicBody2D`, `Spatial`, `translation` | `CharacterBody2D`, `Node3D`, `position` |
| `velocity = move_and_slide(velocity, Vector2.UP)` | set `velocity` and `up_direction`, then `move_and_slide()` (returns bool) |
| `rand_range`, `deg2rad`, `stepify`, `range_lerp` | `randf_range`, `deg_to_rad`, `snapped`, `remap` |
| `str2var`, `var2str`, `.empty()`, `.invert()` | `str_to_var`, `var_to_str`, `.is_empty()`, `.reverse()` |
| `PoolStringArray`, `PoolVector2Array` | `PackedStringArray`, `PackedVector2Array` |
| `File`, `Directory` | `FileAccess.open(...)`, `DirAccess.open(...)` — a different API, not a rename |
| `OS.get_ticks_msec()`, `OS.get_unix_time()` | `Time.get_ticks_msec()`, `Time.get_unix_time_from_system()` |
| `BUTTON_LEFT`, `KEY_ESCAPE` as globals | `MOUSE_BUTTON_LEFT`, `KEY_ESCAPE` (enums `MouseButton`, `Key`) |
| `.is_a_parent_of(n)` | `.is_ancestor_of(n)` |
| Overridden `_ready` calls the parent's | Call `super()` yourself; Godot 4 does not |
| `randomize()` at start | Not needed; seeding is automatic |

When converting a whole project, the editor's converter does most of the renames but leaves `tool`,
string `connect` calls and some `setget` for you. Read the official upgrade guide for the version pair.

## Python → GDScript

| Python | GDScript |
|---|---|
| `None`, `True`, `len(x)` | `null`, `true`, `x.size()` (a global `len()` exists, but the method is idiomatic) |
| `[f(x) for x in xs if p(x)]` | `xs.filter(p).map(f)` with lambdas, or a loop |
| `a, b = pair` | No unpacking or tuples; index an Array, or return a small `RefCounted` or Dictionary |
| `try:` / `except` | No exceptions; check the returned `Error` or `null` |
| `with open(p) as f:` | `var f := FileAccess.open(p, FileAccess.READ)`; it closes when freed |
| `f(x, flag=True)`, `**kwargs` | Positional only; pass a Dictionary or a settings `Resource` |
| `def f(*args)` | `func f(...args: Array)` from 4.5 |
| `def f(xs=[])` shared between calls | Defaults are evaluated on every call; not shared |
| `7 // 2`, `7 / 2 == 3.5` | `7 / 2 == 3` for ints; `7 / 2.0 == 3.5` |
| `-7 % 3 == 2` | `-7 % 3 == -1`; `posmod(-7, 3) == 2` |
| `f"{a} {b}"` | `"%s %s" % [a, b]` or `"{0} {1}".format([a, b])` |
| `for i in range(0, 1, 0.1)` | `range` is ints only; loop an int and scale |
| `for k, v in d.items()` | `for k in d:` then `d[k]` |
| `class A(B):` | `class A extends B:`, or one class per file with `extends` |
| `@staticmethod` | `static func` |
| `__init__(self, ...)` | `func _init(...) -> void:`; `self` is implicit |
| `raise NotImplementedError` | `@abstract func f() -> void` (4.5+) |
