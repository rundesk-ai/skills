---
name: using-godot
description: Use when building, reviewing, debugging, configuring, or running a Godot 4 game in GDScript or C#, including the pinned engine version, nodes and scenes, node lifetime and freeing, signals, exported properties, resources and the import cache, `.uid` files, input handling, autoloads, the C# build and assembly boundary, cameras and instancing, `project.godot` settings, headless and command-line runs, and export presets. It supplies version-gated engine defaults, the traps and how to prove each one. Do not use it for another engine, or for GDScript or C# language questions that touch no engine behaviour.
---

# Use Godot

Treat the pinned engine as the contract, and treat the boundary between the engine and your own code as
the place where most defects live. API names below are the engine's `snake_case`; C# uses the same names
in PascalCase (`queue_free` is `QueueFree`).

## Establish the line before changing code

`$GODOT` below is the engine binary: `command -v godot`, or wherever the project's rules say it lives.

```sh
"$GODOT" --version                                  # the exact build
grep -E "config_version|config/features" project.godot
ls *.csproj 2>/dev/null                             # present: read references/csharp-boundary.md
```

Godot 4 and Godot 3 are different engines with the same name, and within Godot 4 a minor version
changes node APIs, rendering defaults and the C# packages. A claim about 4.2 is not evidence about 4.7:
the answer is the pinned version's documentation (`/en/<version>/`) or a run of the engine.

## Work in this order

1. **Read the repository's rules and the layer boundaries** it declares. A project that keeps an
   engine-free simulation means it: no engine type belongs on that side.
2. **Read the scene and the script that owns it** before changing either. A node's behaviour is split
   between the `.tscn` — exported values, node paths, signal connections — and its script.
3. **Make the change, then run it.** In C#, build first: the engine runs the last built assembly, never
   your source.
4. **Read the whole log, not the last lines.** See the first trap.

## The traps, and how to prove each one

| Trap | What you see | The proof |
|---|---|---|
| An error in `_ready`, `_process` or a signal handler **aborts that callback, is logged, and the game carries on** — GDScript and C# alike | The feature silently does nothing; the process exits 0 | `grep -n -e 'SCRIPT ERROR' -e 'ERROR:' -e 'Exception' run.log`. A headless run that exits 0 is not a run that worked |
| A node used after `queue_free` | Still valid for the rest of the frame, then an error on a freed instance | `is_queued_for_deletion()` the same frame; `is_instance_valid()` for a reference you did not create; null your own field when you free it |
| A freshly instantiated scene configured before `add_child` | "null instance" errors from a setup method; a field the scene shows empty | `get_node` already works on the new instance, but its `@onready` vars stay null until it enters the tree and runs `_ready`. Set plain properties first and apply them in `_ready`, or call setup after `add_child` |
| `add_child` to a parent outside the tree | The child's `_ready` has not run on the next line | `_ready` runs only once the parent is in the tree; check `is_node_ready()` |
| A `Resource` shared between instances | Changing one instance changes every other | `load()` returns one cached instance. `duplicate()` it, or set `resource_local_to_scene` for resources a scene instantiates |
| Tree or physics state changed inside a physics callback or while a parent sets up children | "Can't change this state while flushing queries", or "Parent node is busy setting up children" | `call_deferred` / `set_deferred` for those changes. Adding a child in an ordinary handler is fine |
| A `@tool` (`[Tool]`) script | The editor crashes, or a scene is saved with values the game never produced | Guard editor-time work with `Engine.is_editor_hint()`; everything else in the file runs while the scene is merely open |
| A `.uid` or `.import` file left out of a commit | References break, or assets reimport differently, on the next clone | Commit `*.uid` (4.4+) and `*.import`; ignore only `.godot/` |
| A clean checkout with no import cache | A resource loads as null; a `class_name` is "not declared" | `--headless --import` once before the first run |
| Window size read in a headless run | A placeholder size, not the configured window | Read the design size from `display/window/size/viewport_width`/`_height`; follow the real size through the viewport's `size_changed` |
| An exported member renamed | Scenes silently lose the saved value | Values are stored in the `.tscn` by name; grep the scenes and set them again |
| A one-shot gameplay action read in `_input`, or polled without checking the GUI | Clicks on a menu also fire the weapon | Discrete actions go in `_unhandled_input`, by Input Map action name, so the GUI consumes its events first. Polling `Input.is_action_pressed` for continuous movement is fine |

**Read [Nodes and lifetime](references/nodes-and-lifetime.md)** before writing a node, and
**[The C# boundary](references/csharp-boundary.md)** in any project with a `.csproj`.

## Defaults worth keeping

- **Reach a node by a reference that survives a move.** A path string breaks silently when someone drags
  a node; an exported node reference (`@export var target: Node3D`) or a scene-unique `%Name` does not.
- **Call down, signal up.** A parent calls its children and listens to their signals; a child does not
  reach up the tree, and siblings talk through their parent. A scene that assumes its parent cannot be
  instanced anywhere else.
- **Build the scene in a `.tscn` once its shape is settled, and in code while it is not.** A scene file is
  a second home for every decision and a merge conflict; code is readable in a diff.
- **Autoloads are created in the order listed, before the main scene.** One that reads another in
  `_ready` depends on that order; keep them few and independent.
- **`_physics_process` is a fixed step, `_process` is per frame**, and physics may run zero or several
  times in one frame. A simulation that must replay owns its own accumulator.
- **Many identical meshes are one `MultiMeshInstance3D`** when per-node CPU cost shows in the profiler.
  Forward+ already batches identical mesh-and-material nodes into one draw; Mobile and Compatibility do
  not. See [Rendering and instancing](references/rendering-and-instancing.md).
- **Keep `project.godot` small and hand-read.** The editor adds to it; read what it added, because a
  setting written by accident is a decision nobody made.

## Running it

**Read [Command line and headless](references/command-line-and-headless.md)** for the flags and a smoke
run that fails when the game is broken.

```sh
"$GODOT" --path .                                         # run
"$GODOT" --headless --path . --import                     # import on a clean checkout, then quit
"$GODOT" --headless --path . --fixed-fps 60 --quit-after 300 --log-file "$PWD/run.log" -- --smoke
"$GODOT" --headless --path . --build-solutions --quit     # C#: build without staying in the editor
"$GODOT" --path . --write-movie "$PWD/tmp/shot/f.png" --quit-after 90   # needs a window
```

`--build-solutions` and `--import` both start the editor, and `--write-movie` needs a window; the
reference has why.

## Report what you changed and what proves it

Name the node or scene, the file and method, and the run whose output shows the behaviour. For anything
the owner judges by eye, a capture — never a description.

## References

- [Nodes and lifetime](references/nodes-and-lifetime.md) — the tree, `_ready` order, `queue_free`
  versus `free`, signals, exports, pausing.
- [The C# boundary](references/csharp-boundary.md) — building, swallowed exceptions, the wrapper and the
  native object, assembly reload, marshalling, target framework.
- [Rendering and instancing](references/rendering-and-instancing.md) — automatic instancing, MultiMesh,
  materials, cameras and projection.
- [Command line and headless](references/command-line-and-headless.md) — flags, import, determinism,
  captures, smoke runs with teeth, exporting.
- [Sources](references/sources.md) — the primary documentation behind these claims.
