# Godot source basis

Audited 2026-10-09 against the Godot 4.7 documentation and the engine source at `4.7-stable`. Claims
marked *observed* were reproduced on Godot 4.7.2 (mono), headless unless noted. **Read the version this
project pins**, not `stable`, when a claim must be exact: `/en/4.7/` for 4.7.

| Guidance | Primary source |
|---|---|
| Node lifetime, `_ready` order, the scene tree, `request_ready` | [Nodes and scenes](https://docs.godotengine.org/en/stable/getting_started/step_by_step/nodes_and_scenes.html), [Node](https://docs.godotengine.org/en/stable/classes/class_node.html) |
| `queue_free` versus `free`; a queued node valid until the frame ends (*observed*) | [Node.queue_free](https://docs.godotengine.org/en/stable/classes/class_node.html#class-node-method-queue-free), [Object.free](https://docs.godotengine.org/en/stable/classes/class_object.html#class-object-method-free) |
| Freed objects and `is_instance_valid` | [@GlobalScope.is_instance_valid](https://docs.godotengine.org/en/stable/classes/class_%40globalscope.html) |
| `add_child` to a parent outside the tree does not run `_ready` (*observed*) | [Node.add_child](https://docs.godotengine.org/en/stable/classes/class_node.html#class-node-method-add-child) |
| Signals; method connections removed with the receiver, lambda connections kept (*observed*, both languages) | [Using signals](https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html), [C# signals](https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_signals.html) |
| Scene organization, loose coupling, dependency injection | [Scene organization](https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html) |
| Autoload order | [Singletons (Autoload)](https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.html) |
| Gameplay input in `_unhandled_input` | [Using InputEvent](https://docs.godotengine.org/en/stable/tutorials/inputs/inputevent.html) |
| Exported properties | [GDScript exports](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_exports.html), [C# exports](https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_exports.html) |
| Pausing and `process_mode` | [Pausing games](https://docs.godotengine.org/en/stable/tutorials/scripting/pausing_games.html) |
| Resources, sharing, `resource_local_to_scene`, `duplicate_deep` | [Resources](https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html), [Resource](https://docs.godotengine.org/en/stable/classes/class_resource.html) |
| The import system; commit `.import` files | [Import process](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html), [Version control systems](https://docs.godotengine.org/en/stable/tutorials/best_practices/version_control_systems.html) |
| `.uid` files (4.4+) must be committed | [UID changes coming to Godot 4.4](https://godotengine.org/article/uid-changes-coming-to-godot-4-4/) |
| C# setup, target framework, platform limits, snake_case names in string APIs | [C# basics](https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_basics.html), [C# API differences](https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_differences.html), [Godot.NET.Sdk](https://www.nuget.org/packages/Godot.NET.Sdk) |
| Variant and what crosses the boundary | [Variant](https://docs.godotengine.org/en/stable/classes/class_variant.html), [C# Variant](https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_variant.html) |
| Assembly reload only in the editor; delegate serialization | engine source `modules/mono/csharp_script.cpp` (`reload_assemblies`) |
| StringName | [StringName](https://docs.godotengine.org/en/stable/classes/class_stringname.html) |
| Automatic instancing on Forward+ only, opaque or alpha-tested | [Optimizing 3D performance](https://docs.godotengine.org/en/stable/tutorials/performance/optimizing_3d_performance.html) |
| MultiMesh | [MultiMesh](https://docs.godotengine.org/en/stable/classes/class_multimesh.html), [Using MultiMeshInstance3D](https://docs.godotengine.org/en/stable/tutorials/3d/using_multi_mesh_instance.html) |
| Camera projection and orthographic size | [Camera3D](https://docs.godotengine.org/en/stable/classes/class_camera3d.html) |
| Environment and lighting | [Environment and post-processing](https://docs.godotengine.org/en/stable/tutorials/3d/environment_and_post_processing.html) |
| Renderer selection | [Renderers](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html) |
| Command-line flags; `--import` and `--build-solutions` imply the editor; `--write-movie` forces `--fixed-fps` | [Command line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html), and `godot --help` |
| Movie Maker | [Creating movies](https://docs.godotengine.org/en/stable/tutorials/animation/creating_movies.html) |
| Project settings | [ProjectSettings](https://docs.godotengine.org/en/stable/classes/class_projectsettings.html) |
| Exporting, presets and templates | [Exporting projects](https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html) |

Observed on 4.7.2, beyond the documentation:

- A runtime error in a GDScript callback, and an exception in a C# one, aborts the callback, logs it, and
  the process exits 0; `_process` keeps running.
- `--headless --build-solutions` without `--quit` never exits; with it, exit 0 on success and 1 on a
  compile error.
- `--write-movie` under `--headless` crashes; windowed, a `.png` path gives a numbered sequence.
- A headless viewport reports a placeholder size for the whole run.
- `--quit-after n` runs exactly n `_process` calls; physics steps per frame vary without `--fixed-fps`.
- A smoke scene that calls `get_tree().quit(1)` on a failed assertion makes the run exit 1.
- In `--script` mode, autoloads exist from `_initialize`, not in `_init`.
- On a freshly instantiated scene, `get_node` finds children before `add_child`, while `@onready` vars are
  still null.
