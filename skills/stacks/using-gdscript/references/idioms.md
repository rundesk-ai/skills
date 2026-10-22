# GDScript idioms

Read the section the change reaches. Each pair shows the shape to write and the one it replaces.

## A script, in order

```gdscript
class_name Turret
extends Node2D
## Fires at the nearest enemy in range.

signal fired(target: Enemy)

enum State { IDLE, AIMING, COOLDOWN }

const BULLET: PackedScene = preload("res://combat/bullet.tscn")

@export var range_px: float = 320.0
@export_range(0.1, 5.0, 0.1) var cooldown_s: float = 0.8

var state: State = State.IDLE
var _target: Enemy

@onready var _muzzle: Marker2D = $Muzzle


func _physics_process(delta: float) -> void:
	...


func fire() -> void:
	...


func _pick_target() -> Enemy:
	...
```

`preload` into a `const` when the path is fixed: it loads at parse time and fails at parse time.
`load()` is for paths decided at runtime.

## Initialization

The order is: defaults and initializers top to bottom, `_init`, exported values from the scene,
`@onready`, `_ready`. Children are ready before their parent.

```gdscript
# Bad: exported values are not applied yet in _init
func _init() -> void:
	_scale_to(range_px)

# Good
func _ready() -> void:
	_scale_to(range_px)
```

`@onready` and `@export` on one variable is an error by default (`ONREADY_WITH_EXPORT`): the scene's value
would be overwritten at ready. A `_ready` runs once per node; `request_ready()` runs it again on re-entry.

## Signals

Name a signal for what happened, in the past tense, with typed arguments. A parent calls methods on its
children and listens to their signals; a child does not reach up the tree. Siblings talk through their
parent.

```gdscript
# Bad: string names, unchecked
connect("died", self, "_on_died")
emit_signal("died")

# Good: the parser checks both ends
enemy.died.connect(_on_enemy_died)
died.emit()
```

- Extra context goes through `bind`, which appends after the signal's own arguments:
  `button.pressed.connect(_on_slot_pressed.bind(index))`.
- Connecting the same callable twice is an error unless it was connected with `CONNECT_REFERENCE_COUNTED`;
  check `is_connected` when a connect may run more than once.
- `CONNECT_ONE_SHOT` disconnects after the first emission.
- Connections made in the editor live in the `.tscn`; grep the scene before deciding a handler is unused.

## Lambdas and callables

```gdscript
var hits := 0
var count := func() -> void: hits += 1     # Bad: changes a copy; hits stays 0
var tally := {"hits": 0}
var count2 := func() -> void: tally.hits += 1   # Good: mutates shared state
```

A lambda captures locals **by value, once, at creation**; Arrays, Dictionaries and objects are shared
because the copied value is a reference. A lambda needs an explicit `return`. A lambda capturing a node
keeps a connection to it alive for as long as the emitter lives; connect a method where the lifetime
matters. There are no list comprehensions; use `filter`, `map`, `reduce`, `any`, `all` or a loop.

## Coroutines

```gdscript
func open() -> void:
	_door.play("open")
	await _door.animation_finished
	opened.emit()

# Bad: does not wait; opened fires later, at an unknown time
func enter() -> void:
	open()
	_walk_in()

# Good
func enter() -> void:
	await open()
	_walk_in()
```

`await get_tree().create_timer(0.5).timeout` waits on time. A coroutine waiting on a signal that never
fires — its emitter freed, its tween killed — is never resumed and is never reported. Guard on
`is_instance_valid(self)` after an `await` in a node that may have been freed meanwhile.

## Properties

```gdscript
@export var max_hp: int = 10

var hp: int = 10:
	set(value):
		hp = clampi(value, 0, max_hp)
		health_changed.emit(hp)
```

Inside its own accessor the name reaches the backing field. The initializer does not run the setter. A
setter that touches child nodes runs when the scene sets an exported value — before `_ready` — so guard
it with `if is_node_ready():`.

## Exports

Export what a designer tunes; a value the code owns is a `const`. Use the specific annotation
(`@export_range`, `@export_enum`, `@export_file("*.json")`, `@export_group`) so the inspector cannot
accept a value the code rejects. `@export var target: Node2D` exports a node reference directly.
`@export_tool_button` (4.4+) needs `@tool`.

## Resources, RefCounted and nodes

- **`Resource`** for data a designer edits or that is saved: a `class_name` extending `Resource` with
  exported fields appears in the inspector and saves to `.tres`. Give `_init` parameters defaults, or the
  inspector and `duplicate()` cannot construct it.
- **`RefCounted`** for runtime data and logic objects; freed when the last reference goes.
- **`Node`** only for something that lives in the tree. Every node costs processing propagation.
- **`Object`** needs a manual `free()`; prefer `RefCounted`.

A resource loaded from disk is one shared instance:

```gdscript
# Bad: every goblin loses health together
stats.hp -= damage

# Good: each instance owns a copy
func _ready() -> void:
	stats = stats.duplicate()
```

## Errors

Engine calls return `Error` codes; check the ones whose failure matters.

```gdscript
var file := FileAccess.open(path, FileAccess.READ)
if file == null:
	push_error("cannot open %s: %s" % [path, error_string(FileAccess.get_open_error())])
	return {}
```

`get_node_or_null` where absence is normal; `get_node` where absence is a bug, so the error names it.
`push_error` and `push_warning` log with a stack trace and continue; there is nothing to catch.

## Autoloads

An autoload is for a system that owns its own state across scenes — a save manager, an audio bus. It is
not a namespace: stateless helpers are `static func` on a `class_name`, and since 4.1 a `static var` holds
shared data without a node. Every autoload is a global dependency the next scene inherits.

## Performance

Profile first; the debugger's profiler and monitors show which function costs. Then, in hot code:

- Type it. Typed GDScript uses specialised instructions; the engine's benchmark measured 25–50% on
  operators and built-in calls and more on native method calls.
- Cache node references in `@onready` vars; do not call `get_node` or `$` per frame.
- Use `PackedFloat32Array`, `PackedVector2Array` and friends for bulk numbers; they iterate faster than
  `Array[T]`, which beats an untyped `Array`.
- Use `&"name"` StringName literals for names compared often (input actions, animation names); creating
  a StringName from a String each call is the slow part.
- Turn off what does not need to run: `set_process(false)`, a `Timer` for checks that do not need every
  frame, removing a node from the tree rather than hiding it.
- Move work the engine already does in C++ to the engine call (`Array.sort_custom`, physics queries,
  `Geometry2D`); a loop rewritten in GDScript is slower than the built-in.
