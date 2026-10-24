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

## Scale, tiles, large worlds, graphics and headless authoring

| Guidance | Primary source |
|---|---|
| TileMapLayer replaces TileMap; quadrants, y-sort origin, update batching, 16-bit saved coordinates, `physics_quadrant_size` | [TileMapLayer](https://docs.godotengine.org/en/4.7/classes/class_tilemaplayer.html), [Godot 4.3 release](https://godotengine.org/releases/4.3/) |
| Tile shapes and layouts; `texture_origin`, `y_sort_origin` | [TileSet](https://docs.godotengine.org/en/4.7/classes/class_tileset.html), [TileData](https://docs.godotengine.org/en/4.7/classes/class_tiledata.html) |
| Terrain autotiling cost and order dependence | [godot-proposals #7670](https://github.com/godotengine/godot-proposals/issues/7670), [forum](https://forum.godotengine.org/t/autotiling-extremely-slow-at-runtime-alternatives/66619) |
| AStarGrid2D: `update()` clears point data, diagonal modes, partial paths, jumping ignores weights | [AStarGrid2D](https://docs.godotengine.org/en/4.7/classes/class_astargrid2d.html) |
| Navigation cost of per-tile polygons | [Navigation performance](https://docs.godotengine.org/en/4.7/tutorials/navigation/navigation_optimizing_performance.html) |
| 2D batching in the RD renderers from 4.4 | [Dev snapshot 4.4 dev 3](https://godotengine.org/article/dev-snapshot-godot-4-4-dev-3/) |
| Pixel-art stretch and integer scaling | [Multiple resolutions](https://docs.godotengine.org/en/4.7/tutorials/rendering/multiple_resolutions.html) |
| Physics interpolation, 2D and 3D | [Using physics interpolation](https://docs.godotengine.org/en/4.7/tutorials/physics/interpolation/using_physics_interpolation.html) |
| 2D lights cost | [2D lights and shadows](https://docs.godotengine.org/en/4.7/tutorials/2d/2d_lights_and_shadows.html) |
| `time_scale` stretches ticks; `max_physics_steps_per_frame` | [Engine](https://docs.godotengine.org/en/4.7/classes/class_engine.html) |
| Servers, keeping resource references, freeing RIDs | [Optimization using Servers](https://docs.godotengine.org/en/4.7/tutorials/performance/using_servers.html) |
| Thread-safe APIs; building nodes outside the tree | [Thread-safe APIs](https://docs.godotengine.org/en/4.7/tutorials/performance/thread_safe_apis.html), [WorkerThreadPool](https://docs.godotengine.org/en/4.7/classes/class_workerthreadpool.html) |
| Background loading; `load_threaded_get` | [Background loading](https://docs.godotengine.org/en/4.7/tutorials/io/background_loading.html) |
| Mesh LOD, visibility ranges, occlusion culling | [Mesh LOD](https://docs.godotengine.org/en/4.7/tutorials/3d/mesh_lod.html), [Visibility ranges](https://docs.godotengine.org/en/4.7/tutorials/3d/visibility_ranges.html), [Occlusion culling](https://docs.godotengine.org/en/4.7/tutorials/3d/occlusion_culling.html) |
| Large world coordinates; 2D gains nothing from double precision | [Large world coordinates](https://docs.godotengine.org/en/4.7/tutorials/physics/large_world_coordinates.html) |
| Jolt built in from 4.4, new-project default from 4.6; `DEFAULT` is GodotPhysics3D | [Using Jolt Physics](https://docs.godotengine.org/en/4.7/tutorials/physics/using_jolt_physics.html), [PR #105737](https://github.com/godotengine/godot/pull/105737), [Godot 4.6](https://godotengine.org/releases/4.6/) |
| Renderer feature sets | [Renderers](https://docs.godotengine.org/en/4.7/tutorials/rendering/renderers.html) |
| GI options and which bake at runtime | [Introduction to GI](https://docs.godotengine.org/en/4.7/tutorials/3d/global_illumination/introduction_to_global_illumination.html) |
| Ubershaders, pipeline compilation monitors, shader baker | [Pipeline compilations](https://docs.godotengine.org/en/4.7/tutorials/performance/pipeline_compilations.html) |
| Orthographic cameras ignore the directional shadow max distance | engine source `servers/rendering/renderer_scene_cull.cpp` at `4.7-stable`; [DirectionalLight3D](https://docs.godotengine.org/en/4.7/classes/class_directionallight3d.html); [forum](https://forum.godotengine.org/t/3d-shadow-problem-in-othognal-mode/102064) |
| Feature version gates | [4.4](https://godotengine.org/releases/4.4/), [4.5](https://godotengine.org/releases/4.5/), [4.6](https://godotengine.org/releases/4.6/), [4.7](https://godotengine.org/releases/4.7/) |
| Texture import, VRAM compression | [Importing images](https://docs.godotengine.org/en/4.7/tutorials/assets_pipeline/importing_images.html) |
| `PackedScene.pack` and owners; the `.tscn` format | [PackedScene](https://docs.godotengine.org/en/4.7/classes/class_packedscene.html), [TSCN file format](https://docs.godotengine.org/en/4.7/engine_details/file_formats/tscn.html) |
| `EditorScript` runs only from the editor | [EditorScript](https://docs.godotengine.org/en/4.7/classes/class_editorscript.html) |
| Objects from `get_var(true)` can run code | [FileAccess](https://docs.godotengine.org/en/4.7/classes/class_fileaccess.html) |
| JSON types; `from_native`/`to_native` | [JSON](https://docs.godotengine.org/en/4.7/classes/class_json.html) |
| C# signals: custom `+=` not disconnected on free; collections marshal | [C# signals](https://docs.godotengine.org/en/4.7/tutorials/scripting/c_sharp/c_sharp_signals.html), [C# collections](https://docs.godotengine.org/en/4.7/tutorials/scripting/c_sharp/c_sharp_collections.html) |
| C# platform support, debugging setup, diagnostics | [C# basics](https://docs.godotengine.org/en/4.7/tutorials/scripting/c_sharp/c_sharp_basics.html), [GD0001](https://docs.godotengine.org/en/4.7/tutorials/scripting/c_sharp/diagnostics/GD0001.html) |
| The editor hosts .NET with its own runtimeconfig; `GodotSynchronizationContext` | engine source `modules/mono` at `4.7.2-stable` (`mono_gd/gd_mono.cpp`, `GodotSynchronizationContext.cs`) |

Observed on 4.7.2, beyond the documentation (one Apple Silicon machine, Metal, Forward+):

- Saving: a node without `owner` dropped with its subtree while `pack` and `save` return OK; only
  `CONNECT_PERSIST` method connections saved; unnamed nodes; plain `--script` saves without UIDs and
  `--editor --script` saves with them; `EditorScript` refused on the command line; nothing in the tree
  during `_initialize`; a new asset or `class_name` unloadable until `--import`; a wrong `uid` only warned.
  The scene-building script in `building-scenes-headless.md` was run and its saved scene reloaded with
  every cell.
- Tiles: the isometric default layout is stacked; `local_to_map` round-trips on every shape and layout;
  picking through `to_local`; y-sort needing the parent or children (by pixel reads); `z_index` beating
  y-sort; `set_cell` accepting unknown atlas coordinates; the costs of `set_cell`, first-frame internals,
  physics and navigation layers, and `set_cells_terrain_connect`; 16-bit coordinate wrap.
- Pathfinding: `update()` clearing solids; corner-cutting diagonals; corner coordinates from
  `get_point_path`; a full-grid search for an unreachable target; one BFS field against 500 A* queries.
- 2D at scale: the sprite, canvas item, `_draw` and MultiMesh table; `_draw` cached; the upside-down
  `QuadMesh`; leaked canvas-item RIDs.
- 3D at scale: headless reading 0 for every render monitor; RenderingServer instances drawing nothing
  once the mesh is released; leaked RIDs at exit; raycasts seeing the last physics step; monitors reading
  0 before a frame; `load_threaded_get` returning null the second time; `RefCounted` cycles and `preload`
  keeping memory; the node, server and MultiMesh memory table; `Area3D` cost at 2,000 and 8,000;
  collision pairs 0 under Jolt; `DEFAULT` physics engine in a hand-written project; physics
  interpolation; `generate_lods` at runtime; GridMap timings; 32-bit positions.
- Speed: `time_scale` stretching ticks; a `Timer` firing once per frame at most; eight steps after a
  stall.
- Threads: `add_child` from a worker refused and leaked; `position` from a worker unreported; group tasks
  by chunk against by element; low against high priority.
- Large worlds: memory per `TileMapLayer` cell; chunk attach times and frame spikes at 1, 4 and 16 chunks
  per frame; `tile_map_data` built from bytes on a worker; out-of-tree layers built on workers; memory
  returning after `queue_free`; occasional 7–13 ms `add_surface_from_arrays` stalls (Metal only, cause
  unproved); `HeightMapShape3D` against concave shapes in both engines; cycle-over-cycle soak.
- Save files: a `.tres` with an embedded script running it on load; `str_to_var` and `ConfigFile`
  building live objects.
- C#: the four-file project; misleading "class could not be found" causes; `--build-solutions` hiding
  compiler errors and doing nothing without a `.csproj`; export without a solution shipping no assembly;
  custom `[Signal]` `+=` surviving `Free()`; the GC never freeing a `Node`; `Dispose()` leaving the node in
  the tree; a missing parameterless constructor giving a script-less node; the measured marshalling,
  `StringName`, signal and event costs in an export; off-thread access messages; one `await` resume per
  frame; csproj GC settings ignored by the editor binary; server GC frame pauses; JIT first-call hitches.

Not verified: Camera2D jitter fixes and the top-down graphics choices (they need a person to look), Light2D
cost, `NavigationAgent2D` at hundreds of agents, Vulkan and D3D12 behaviour of the chunk stalls, release
memory per object, the floating-origin recipe, desktop NativeAOT.

## Organization and naming

| Guidance | Primary source |
|---|---|
| Case sensitivity in exports; snake_case files and folders; organizing by feature; `.gdignore` | [Project organization](https://docs.godotengine.org/en/4.7/tutorials/best_practices/project_organization.html), [File system](https://docs.godotengine.org/en/4.7/tutorials/scripting/filesystem.html), [PR #98927](https://github.com/godotengine/godot/pull/98927) |
| `ResourceLoader.list_directory` (4.4+); `DirAccess` in exports | [ResourceLoader](https://docs.godotengine.org/en/4.7/classes/class_resourceloader.html), [DirAccess](https://docs.godotengine.org/en/4.7/classes/class_diraccess.html) |
| Named classes; duplicate names | [GDScript basics: registering named classes](https://docs.godotengine.org/en/4.7/tutorials/scripting/gdscript/gdscript_basics.html), [issue #94378](https://github.com/godotengine/godot/issues/94378) |
| Global classes in C# | [C# global classes](https://docs.godotengine.org/en/4.7/tutorials/scripting/c_sharp/c_sharp_global_classes.html) |
| C# members keep their C# names across languages | [C# basics: gotchas](https://docs.godotengine.org/en/4.7/tutorials/scripting/c_sharp/c_sharp_basics.html), [Cross-language scripting](https://docs.godotengine.org/en/4.7/tutorials/scripting/cross_language_scripting.html), [Groups](https://docs.godotengine.org/en/4.7/tutorials/scripting/groups.html) |
| Node names, `add_child` readable names | [Node](https://docs.godotengine.org/en/4.7/classes/class_node.html) |
| Scene-unique names | [Scene unique nodes](https://docs.godotengine.org/en/4.7/tutorials/scripting/scene_unique_nodes.html) |
| Scenes with no dependencies; parenting by lifetime | [Scene organization](https://docs.godotengine.org/en/4.7/tutorials/best_practices/scene_organization.html) |
| When to autoload | [Autoloads versus regular nodes](https://docs.godotengine.org/en/4.7/tutorials/best_practices/autoloads_versus_regular_nodes.html) |
| Nodes are not components | [Godot's design philosophy](https://docs.godotengine.org/en/4.7/getting_started/introduction/godot_design_philosophy.html) |
| Event bus as community practice | [GDQuest pattern](https://www.gdquest.com/library/pattern_event_bus_singleton), [forum](https://forum.godotengine.org/t/autoload-signal-bus-vs-in-scene-signal-connections/111185) |
| Framework design guidelines on type names | [Names of namespaces](https://learn.microsoft.com/dotnet/standard/design-guidelines/names-of-namespaces) |

Observed on 4.7.2, with `.pck` exports run through `--main-pack`: wrong-case `load` returning null and a
wrong-case `preload` failing the script, with no export warning; the `Case mismatch` warning in a project
run; `DirAccess` listing `.remap`/`.import`/`.gdc` names in the pack and `list_directory` listing the
originals; a `class_name` equal to an autoload failing both; two equal `class_name`s and two equal
`[GlobalClass]` names resolving silently to one; files moved with and without their `.uid`; `call_group`
with a snake_case name skipping a C# method; a mismatched `.cs` file name building clean; a reused node
name becoming `@Node@2`; name sanitizing; `%Unique` needing `owner`; a text `.tres` under `.gdignore`
loading from the project and missing from the pack; a custom `Timer` type ambiguous or shadowing.
