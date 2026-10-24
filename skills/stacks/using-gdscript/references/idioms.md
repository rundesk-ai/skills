# GDScript idioms that fail quietly

Each of these parses, runs, and does the wrong thing without an error. The traps in `SKILL.md` are not
repeated here.

## Initialization

- **Exported values are not applied in `_init`.** The order is: member initializers, `_init`, the
  scene's exported values, `@onready`, `_ready`. Read an exported value in `_ready`.
- `preload` into a `const` when the path is fixed: it loads, and fails, at parse time. `load()` is for
  paths decided at runtime — and for anything you mean to unload, since a `preload` pins the resource for
  as long as the script is loaded.
- **A node removed and added again does not run `_ready` again.** A pooled node that sets itself up in
  `_ready` comes back stale; call `request_ready()` before re-adding it, or set it up in a method you
  call.

## Signals

- `bind` appends after the signal's own arguments: `button.pressed.connect(_on_slot_pressed.bind(index))`
  calls `_on_slot_pressed(index)`, but a signal with arguments puts them first.
- Connecting the same callable twice is an error unless connected with `CONNECT_REFERENCE_COUNTED`; check
  `is_connected` where a connect can run more than once (a `_ready` re-run, a re-entered tree).
- Connections made in the editor live in the `.tscn`, as `[connection]` lines. Grep the scene before
  deleting a handler that looks unused.

## Coroutines

A node can be freed while a coroutine in it is suspended. After an `await` in a node that may be freed
meanwhile, check `is_instance_valid(self)` before touching its members.

## Properties

```gdscript
var hp: int = 10:
	set(value):
		hp = clampi(value, 0, max_hp)
		if is_node_ready():
			_bar.value = hp
```

- **The initializer does not run the setter**, so a clamp or a signal in it does not apply to the default.
- **A setter runs when the scene applies an exported value — before `_ready`**, when `@onready` members
  are still null; guard child-node work with `is_node_ready()`.
- Inside its own setter, the name writes the backing field. A helper method the setter calls that assigns
  the property runs the setter again, and an unconditional one recurses until the stack overflows.

## Resources and objects

- **A custom `Resource`'s `_init` parameters need defaults**, or the inspector and `duplicate()` cannot
  construct it.
- A resource's script cannot be an inner class: its properties are not saved.
- `free()` on a `RefCounted` is an error that aborts the function; drop the references instead.

## Turning work off

Hiding a node does not stop its `_process`. `set_process(false)`, a `Timer` for checks that need not run
every frame, or removing the node from the tree. A loop rewritten in GDScript to replace an engine routine
— `sort`, a physics query, `Geometry2D` — is slower than the routine.
