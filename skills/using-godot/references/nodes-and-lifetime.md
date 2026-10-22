# Nodes, scenes and lifetime

Examples are GDScript; C# uses the same engine names in PascalCase.

## The tree

A Godot game is a tree of nodes. A node is in the tree or it is not, and almost everything — `_ready`,
`_process`, signals, `get_node` — depends on which.

```
_enter_tree()         the node is now in the tree; its children are NOT ready yet
_ready()              this node and all its children are ready. Runs once
_process(delta)       every frame, while in the tree and not paused
_physics_process(d)   every physics step, at a fixed rate; zero or several per frame
_exit_tree()          leaving the tree; may be followed by free, or by re-entry
```

**`_ready` runs children first, then the parent.** A parent's `_ready` can rely on its children; a
child's cannot rely on its parent. Adding a child to a node **that is already in the tree** runs the
child's `_ready` before `add_child` returns, so it is usable on the next line:

```gdscript
func _ready() -> void:
	_view = HealthBar.new()
	add_child(_view)           # _view._ready() has run: this node is in the tree
	_view.build(_data)
```

Added to a parent that is not in the tree yet, the child waits until that parent enters it. A `_ready`
runs once; `request_ready()` makes it run again on the next entry.

Set a node's properties before `add_child` where you can: once it is in the tree, each setter may do
work the engine would otherwise do once.

## Freeing

**`queue_free()` marks a node to be freed at the end of the frame; `free()` destroys it now.** During a
signal, a physics step or an iteration over children, "now" means destroying an object the engine is
still walking — so `queue_free` is the default and `free` needs a reason. Freeing a node frees its
children.

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

`Node` and `Object` are not reference-counted: nothing frees a node you removed from the tree with
`remove_child` and forgot. `RefCounted` and `Resource` free themselves.

## Signals

A signal is the engine's event. Connect to a method where you can, and disconnect where you connected
when the emitter outlives the receiver:

```gdscript
button.pressed.connect(_on_pressed)
button.pressed.disconnect(_on_pressed)
```

- A connection to a node's **method** is removed when that node is freed. A **lambda** is not tied to a
  receiver: it keeps firing after the node that connected it and the nodes it captured are freed, and
  logs `Lambda capture at index 0 was freed`. Connect a method, or disconnect the lambda yourself.
- Connecting the same callable twice is an error; `is_connected` checks first. `CONNECT_ONE_SHOT`
  disconnects after one emission.
- Connections made in the editor live in the `.tscn`. Grep the scene before deciding a handler is unused.

## Exported properties

`@export` (`[Export]` in C#) publishes a property to the inspector and the scene file.

- The value the inspector shows is stored **in the `.tscn`**. The default in code applies only where the
  scene does not override it, and exported values are applied after `_init`, before `_ready`.
- Export a node reference directly (`@export var target: Node3D`) instead of a `NodePath` you resolve.

Export what a designer tunes. A constant the code owns is a constant, where no scene can change it.

## Scenes versus code

A `.tscn` is a saved tree; instancing one is how a game reuses a thing. While the shape of a view changes
daily, a scene file duplicates every decision and conflicts on every merge; once the shape settles, a
scene is readable in the editor and editable without a code change. Moving from code to scene is an
ordinary step.

A scene should run with no assumption about its parent. Give it what it needs through exported
properties or a setup method its parent calls, and let it report upward with signals.

## Groups and autoloads

`add_to_group(&"enemies")` and `get_tree().get_nodes_in_group(&"enemies")` find nodes without paths.
An autoload is for a system that owns state across scenes,
not a namespace for helpers.

## Pausing and processing

`get_tree().paused = true` stops nodes whose `process_mode` inherits or is `PROCESS_MODE_PAUSABLE`, and
stops physics. A node that must run while paused — a menu, a debug overlay — sets
`process_mode = PROCESS_MODE_ALWAYS`. A simulation that must stop when paused should stop because its
own driver stopped calling it, not because a node's process mode happened to be right.
