# Syntax from elsewhere

Most generated GDScript errors are code from Godot 3 or from Python. Most of it fails to parse, which the
checker catches; the rows below are the ones agents still get wrong, or where the replacement is a
different design rather than a rename.

## Godot 3 → Godot 4

| Godot 3 | Godot 4 |
|---|---|
| `var x setget set_x, get_x` | `var x: int:` with `set(value):` and `get:` blocks |
| `yield(obj, "signal")` | `await obj.signal` |
| `connect("sig", self, "_m", [arg])` | `sig.connect(_m.bind(arg))` |
| `emit_signal("sig", v)` | `sig.emit(v)` |
| `velocity = move_and_slide(velocity, Vector2.UP)` | set `velocity` and `up_direction`, then `move_and_slide()` (returns bool) |
| `rand_range`, `deg2rad`, `stepify`, `range_lerp` | `randf_range`, `deg_to_rad`, `snapped`, `remap` |
| `File`, `Directory` | `FileAccess.open(...)`, `DirAccess.open(...)` — a different API, not a rename |
| `OS.get_ticks_msec()`, `OS.get_unix_time()` | `Time.get_ticks_msec()`, `Time.get_unix_time_from_system()` |
| Overridden `_ready` or `_init` calls the parent's | Call `super()` yourself; Godot 4 does not |
| `randomize()` at start | Not needed; seeding is automatic |

The editor's project converter does most renames but leaves `tool`, string `connect` calls and some
`setget` for you.

## Python → GDScript

| Python | GDScript |
|---|---|
| `a, b = pair` | No unpacking or tuples; index an Array, or return a small `RefCounted` or Dictionary |
| `with open(p) as f:` | `var f := FileAccess.open(p, FileAccess.READ)`; it closes when the last reference goes |
| `f(x, flag=True)`, `**kwargs` | Positional only; pass a Dictionary or a settings `Resource` |
| `def f(*args)` | `func f(...args: Array)` from 4.5; no spread — pass an array to `callv` |
| `f"{a} {b}"` | `"%s %s" % [a, b]` or `"{0} {1}".format([a, b])` |
| `for i in range(0, 1, 0.1)` | `range` takes ints only; loop an int and scale |
| `for k, v in d.items()` | `for k in d:` then `d[k]`, or `for v in d.values()` |
| `raise NotImplementedError` | `@abstract func f() -> void` (4.5+) |
