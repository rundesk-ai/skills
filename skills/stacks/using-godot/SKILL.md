---
name: using-godot
description: Use when building, reviewing, debugging, configuring, or running a Godot 4 game in GDScript or C#, including the pinned engine version, nodes and scenes, node lifetime and freeing, signals, exported properties, resources and the import cache, `.uid` files, input handling, autoloads, the C# build and assembly boundary, cameras and instancing, tile maps and isometric or hex grids, 2D and 3D at simulation scale, large or streamed chunked worlds, memory and leaks, threads, graphics settings, `project.godot` settings, project layout and naming, building scenes from the command line, headless runs, and export presets. It supplies version-gated engine defaults, the traps and how to prove each one. Do not use it for another engine, or for GDScript or C# language questions that touch no engine behaviour.
---

# Use Godot

Most Godot defects report success: a callback that errors is logged and skipped, a scene saved without
its nodes returns `OK`, a path that will not exist in the export loads fine in the editor. Prove every
change by a run whose output you read. API names below are `snake_case`; C# uses PascalCase
(`queue_free` is `QueueFree`).

## Establish the version before changing code

`$GODOT` below is the engine binary: `command -v godot`, or wherever the project's rules say it lives.

```sh
"$GODOT" --version                                  # the exact build
grep -E "config_version|config/features|physics_engine|rendering_method" project.godot
ls *.csproj 2>/dev/null                             # present: read references/csharp-boundary.md
```

A minor version changes node APIs, rendering defaults and the C# packages: a claim about another 4.x is
not evidence. Read the pinned version's documentation (`/en/<version>/`) or run the engine. A node's
behaviour is split between its script and the `.tscn` that holds its exported values, node paths and
signal connections; read both before changing either.

## The traps, and how to prove each one

| Trap | What you see | The proof |
|---|---|---|
| An error in `_ready`, `_process` or a signal handler **aborts that callback, is logged, and the game carries on** — GDScript and C# alike | The feature silently does nothing; the process exits 0 | `grep -n -e 'SCRIPT ERROR' -e 'ERROR:' -e 'Exception' run.log`. A headless run that exits 0 is not a run that worked |
| C# code changed but not built | Yesterday's behaviour | The engine runs the last built assembly. `dotnet build` first, and read its errors — see [The C# boundary](references/csharp-boundary.md) |
| A node used after `queue_free` | Still valid for the rest of the frame, then an error on a freed instance | `is_queued_for_deletion()` the same frame; `is_instance_valid()` for a reference you did not create; null your own field when you free it |
| A node configured before it is in the tree | "null instance" errors from a setup method; `_ready` has not run on the next line | `@onready` vars stay null and `_ready` waits until the node — and its parent — are in the tree. Set plain properties first and apply them in `_ready`, or call setup after `add_child` |
| A `Resource` shared between instances | Changing one instance changes every other | `load()` returns one cached instance. `duplicate()` it (shallow; `duplicate_deep()` from 4.5), or set `resource_local_to_scene` |
| Tree or physics state changed inside a physics callback | "Can't change this state while flushing queries" | `call_deferred` / `set_deferred` for those changes. Adding a child in an ordinary handler is fine |
| A `@tool` (`[Tool]`) script | The editor crashes, or a scene is saved with values the game never produced | Guard editor-time work with `Engine.is_editor_hint()`; everything else runs while the scene is merely open |
| A file moved or renamed outside the editor, or a `.uid` left out of a commit | The scene loads and the node silently has **no script** | Move the `.uid` with its file, commit `*.uid` and `*.import`, run `--import`, grep the old path — see [Organization and naming](references/organization-and-naming.md) |
| No import cache: a clean checkout, or an asset or `class_name` added mid-task | A resource loads as null; "No loader found"; a class "not declared" | `"$GODOT" --headless --path . --import`, again after adding files |
| A path whose case differs from the file | Loads in the editor; `null` or a parse error in the export | Grep a run log for `Case mismatch` (4.4+) and run an exported pack — see [Organization and naming](references/organization-and-naming.md) |
| An exported member renamed | Scenes silently lose the saved value | Values are stored in the `.tscn` by name, and override the code default; grep the scenes and set them again |
| A one-shot action read in `_input`, or polled without checking the GUI | Clicking a menu button also places a building | Discrete actions go in `_unhandled_input`, by Input Map action name, so the GUI consumes its events first |
| A scene built and saved from a script | `pack` and `save` return `OK`, and nodes are missing from the file | A node without `owner` is dropped with its whole subtree; load the saved file and count — see [Building scenes headless](references/building-scenes-headless.md) |
| `Engine.time_scale` used for 2×/4× speed | The simulation behaves differently at each speed | It stretches each tick instead of adding ticks; drive the simulation from your own accumulator |
| Anything rendering measured headless | 0 draw calls, 0 video memory, zeros read back from a MultiMesh | Headless renders nothing; measure in a short windowed run, and profile an export rather than the editor binary |
| A node removed with `remove_child`, a `RefCounted` cycle, a server RID | Memory and object counts climb over a session | None of them is freed for you; watch `OBJECT_ORPHAN_NODE_COUNT` and the exit's `leaked` lines — see [Performance and memory](references/performance-and-memory.md) |
| A `.tres` or `.res` save loaded from `user://` | A shared or downloaded save runs code | Resource files can embed scripts; save plain data |
| Physics engine unset in a hand-written or upgraded `project.godot` | Physics differs from a new project; Jolt settings do nothing | `"DEFAULT"` is GodotPhysics3D; only the 4.6+ project manager writes `"Jolt Physics"`. Set `physics/3d/physics_engine` explicitly |

## Simulation scale: the world is data, nodes are its view

A city builder, a colony or agent simulation, a 4X map or a factory game outgrows one node per thing long
before it outgrows the CPU. Keep the simulation in packed arrays or plain objects outside the tree, step
it on a fixed tick, and give nodes only to what the player can see.

| Things | Representation |
|---|---|
| up to a few thousand, each with behaviour | a node each, instanced from its scene |
| tens of thousands of one look | a MultiMesh per chunk, RenderingServer instances, or one `_draw` per chunk |
| proximity between thousands of agents | your own grid or spatial hash — not an `Area2D`/`Area3D` each |
| paths for many units to one place | one distance field shared by all, not a path query each |
| a map larger than memory or the screen | chunks of compact data, with views built only near the camera |

A `MeshInstance3D` costs about 4.5 KB and a `TileMapLayer` cell about 360 bytes; the same cell in your own
array is 1–4 bytes. Forward+ batches identical mesh-and-material nodes into one draw; Mobile and
Compatibility do not.

- [Performance and memory](references/performance-and-memory.md) — before choosing a representation, using
  servers, threads, physics at scale, speed controls, or chasing a leak.
- [Large worlds](references/large-worlds.md) — before streaming chunks or going far from the origin.
- [Tiles and 2D](references/tiles-and-2d.md) — before a tile, isometric or hex map, picking cells,
  y-sorting, grid pathfinding or many sprites.
- [Rendering and instancing](references/rendering-and-instancing.md) — before a MultiMesh or an
  orthographic camera.
- [Graphics quality](references/graphics-quality.md) — before changing renderer, lighting, shadows or GI.
- [Organization and naming](references/organization-and-naming.md) — before laying out folders, naming
  classes, autoloads, groups or actions, or moving files.

## Defaults worth keeping

- **Reach a node by an exported reference or a `%Unique` name**, never a `$A/B/C` path that breaks when
  someone drags a node; `%Unique` finds only nodes the same scene owns.
- **Autoloads are created in the order listed, before the main scene.** One that reads another in
  `_ready` depends on that order; keep them few and independent.
- **After any editor or `--import` run, diff `project.godot`** and revert settings nobody chose.

Read [Nodes and lifetime](references/nodes-and-lifetime.md) before writing signal or export code.

## Running it

**Read [Command line and headless](references/command-line-and-headless.md)** for the flags and a smoke
run that fails when the game is broken, and
[Building scenes headless](references/building-scenes-headless.md) to create scenes, resources or a
project from the command line.

```sh
"$GODOT" --path .                                         # run
"$GODOT" --headless --path . --import                     # import, then quit
"$GODOT" --headless --path . --fixed-fps 60 --quit-after 300 --log-file "$PWD/run.log" -- --smoke
dotnet build                                              # C#: the build, with its compiler errors
"$GODOT" --path . --write-movie "$PWD/tmp/shot/f.png" --quit-after 90   # needs a window
```

Pass `--quit-after` to every `--script` run: an error before `quit()` leaves it running forever.

For anything the owner judges by eye, report a capture, never a description.
[Sources](references/sources.md) holds the evidence behind each rule.
