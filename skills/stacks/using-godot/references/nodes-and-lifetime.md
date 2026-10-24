# Nodes, signals and exports: what the lifecycle docs leave out

Examples are GDScript; C# uses the same engine names in PascalCase.

## Freed is not null

A queued node is still valid until the frame ends, and a reference to a freed node is not `null`:

```gdscript
# Bad: assumes the panel is gone, or that the reference became null
_panel.queue_free()
if _panel:
	_panel.show()                       # still runs this frame; errors next frame

# Good
_panel.queue_free()
_panel = null                           # you own it: drop the reference

# For a reference you did not create and cannot vouch for
if is_instance_valid(target) and not target.is_queued_for_deletion():
	target.hit()
```

Set a node's properties before `add_child` where you can: once it is in the tree, each setter may do work
the engine would otherwise do once.

## Signals

- A connection to a node's **method** is removed when that node is freed — except a custom C# `[Signal]`
  subscribed with `+=` (see [The C# boundary](csharp-boundary.md)).
- **A lambda is not tied to a receiver**: it keeps firing after the node that connected it and the nodes
  it captured are freed, and logs `Lambda capture at index 0 was freed`. Connect a method, or disconnect
  the lambda yourself.
- Connections made in the editor live in the `.tscn` as `[connection]` lines. Grep the scene before
  deciding a handler is unused.

## Exported values

The value the inspector shows is stored **in the `.tscn`**, and overrides the default in code: changing the
default changes nothing for a scene that already saved a value. Exported values are applied after
`_init`, before `_ready`. Export a node reference directly (`@export var target: Node3D`) instead of a
`NodePath` you resolve yourself.

## Pausing

A simulation that must stop when the game pauses stops because its own driver stops calling it, not
because each node's `process_mode` happens to be right. Nodes that must run while paused — a menu, a
debug overlay — set `process_mode = PROCESS_MODE_ALWAYS`.
