# Performance and memory at simulation scale

Examples are GDScript; C# uses the same names in PascalCase. Figures are from Godot 4.7.2 on one fast
desktop; read them as ratios.

## Measure the right build, in the right run

- **A headless run renders nothing**: draw calls and video memory read 0, and a MultiMesh reads back
  zeros. Measure rendering in a short windowed run that quits itself; assert MultiMesh contents through
  your own data.
- **`Performance` monitors are sampled once per main-loop iteration**, so the node count reads 0 in
  `_ready` with 10,000 nodes in the tree. Read them after a frame.
- Profile an export before tuning boundary costs; the editor binary distorts them (figures in
  [The C# boundary](csharp-boundary.md)).
- `Performance.PIPELINE_COMPILATIONS_*` counts shader pipeline compilations — the cause of a first-use
  hitch.

## Nodes, servers and MultiMesh

| 40,000 boxes, windowed | Build | Static memory |
|---|---|---|
| `MeshInstance3D` nodes | 56 ms | 236 MB |
| RenderingServer instances | 19 ms | 154 MB |
| one MultiMesh, buffer assigned once | 5 ms | 54 MB |

A node costs memory before it costs frame time. Forward+ drew 40,000 identical nodes in one draw call
and culled 24,520 of them; the single MultiMesh drew all 480,000 triangles, because it is culled as one
box. RenderingServer instances keep per-instance culling at a third of the nodes' memory.

### RenderingServer directly

```gdscript
var _mesh := BoxMesh.new()          # a member: the RID dies with the last reference to the resource
var _rids: Array[RID] = []

func spawn(xf: Transform3D) -> void:
	var rid := RenderingServer.instance_create2(_mesh.get_rid(), get_world_3d().scenario)
	RenderingServer.instance_set_transform(rid, xf)
	_rids.append(rid)

func _exit_tree() -> void:
	for rid in _rids:
		RenderingServer.free_rid(rid)
```

A mesh held only in a local variable is freed, and its instances draw nothing with no error. Every RID
you create is freed by you; the log reports `RID allocations … leaked at exit` otherwise.

### Per-instance data

- `MultiMesh.use_custom_data` gives four floats per instance, read as `INSTANCE_CUSTOM` in the shader's
  `vertex()` only — `fragment()` fails to compile with it; pass it on through a `varying`.
- `instance uniform` is per node, not per MultiMesh instance, scalars and vectors only, at most 16 per
  shader. Nodes varied this way keep automatic instancing; a unique material per node does not.
- A runtime `ArrayMesh` has no LOD; `ImporterMesh.generate_lods()` builds it at runtime and headless.
  `visibility_range_begin`/`_end` hide by distance and `visibility_parent` swaps a merged far mesh for
  its children up close (HLOD).
- Occlusion culling is off by default and baking needs the editor; a top-down strategy camera has
  little to occlude, and LOD plus visibility ranges pay more.
- `GridMap` holds a 200×200 builder grid in 3 nodes (5.5 ms to fill, then 8–18 ms of rebuild spread over
  the next frames); batch edits into one frame, and keep the authoritative grid in your own arrays.

## Physics at simulation scale

- **Do not give every agent an `Area3D`.** 2,000 cost 1.1–1.7 ms a frame and 8,000 cost 12–14 ms. Keep
  proximity, aggro and influence in your own grid or spatial hash; keep areas for a few player-facing
  triggers. Under Jolt, `monitoring = false` halves the cost of an area that is only detected.
- **A query sees the last physics step.** A body placed or moved this frame is still hit at its old
  position until the next step. Test placement against your occupancy grid; use the ray only to find the
  cell under the cursor — and on a flat grid, `Plane(Vector3.UP, 0).intersects_ray(from, dir)` needs no
  physics at all.
- Under Jolt the collision-pairs monitor reads 0, areas ignore static bodies unless
  `areas_detect_static_bodies` is set, and a ray's `face_index` is -1 unless enabled.
- Physics engines are not deterministic across machines. A simulation that must replay or run in lockstep
  takes no gameplay result from physics.
- **Smooth a fixed-tick simulation with physics interpolation** (2D from 4.3, 3D from 4.4): enable
  `physics/common/physics_interpolation`, move things only in `_physics_process`, and call
  `reset_physics_interpolation()` after a teleport, a spawn or an origin shift. What is drawn is a tick
  behind. MultiMesh instances need `set_buffer_interpolated`; RenderingServer instances are not
  interpolated for you.

## Speed controls

**`Engine.time_scale` stretches each tick; it does not add ticks.** At 4× the physics step is four times
longer, bodies tunnel, and a simulation stepped in `_physics_process` gives different results at each
speed. A `Timer` fires at most once per frame, so it cannot drive 200 ticks a second. After a 500 ms
stall the engine ran only 8 physics steps (`max_physics_steps_per_frame`) and dropped the rest of the
time.

Drive the simulation from your own accumulator, where speed changes the number of ticks and never their
size:

```gdscript
const TICK := 1.0 / 20.0
const MAX_TICKS_PER_FRAME := 40      # or one slow frame demands ever more ticks
var speed := 1                       # 0 paused, 1, 2, 4
var _acc := 0.0

func _process(delta: float) -> void:
	if speed == 0:
		return
	_acc += delta * speed
	var n := 0
	while _acc >= TICK and n < MAX_TICKS_PER_FRAME:
		sim.step()
		_acc -= TICK
		n += 1
	if n == MAX_TICKS_PER_FRAME:
		_acc = 0.0                   # drop the backlog: the game slows rather than freezes
```

Keep `Engine.time_scale` at 1 and use `get_tree().paused` for menus, so the camera, UI tweens and audio do
not speed up with the simulation.

## Threads

- **The live scene tree is not thread-safe, and misuse is not always reported.** From a worker,
  `add_child` logs an error and the node leaks as an orphan; setting `position` passed silently; in C# a
  read returns a default value. Workers compute plain data; the main thread applies it, or the worker
  uses `call_deferred`. Building nodes outside the tree on a worker is allowed.
- **Step simulation chunks with `high_priority = true`.** `WorkerThreadPool.add_group_task` defaults to
  low priority, capped by `threading/worker_pool/low_priority_thread_ratio` (0.3): a GDScript chunk step
  scaled to 3.95 times on 16 cores at low priority and 12.9 times at high. Leave long background builds —
  chunk generation, loading — at low priority so they cannot starve the step.
- **Give a task a chunk, not an entity** — at least about 0.1 ms of work. One task per element was three
  times slower than a plain loop.
- Workers may write distinct indices of a preallocated array; resizing a shared container, or a shared
  counter, needs a `Mutex`. Do not modify one `Resource` from several threads. Wait for every task.
- The separate render thread model and `physics/3d/run_on_separate_thread` are experimental; do not
  ship them untested.

## Memory and leaks

- **Orphans**: a node removed with `remove_child`, or never added, and never freed. Assert
  `Performance.OBJECT_ORPHAN_NODE_COUNT` stays flat across a spawn-despawn cycle in a debug run;
  `print_orphan_nodes()` names them; exit prints `N ObjectDB instances were leaked`, and `--verbose`
  lists each.
- **`RefCounted` cycles are never freed** — `building.residents` ↔ `citizen.home` is the usual one. Make
  one direction a `WeakRef` or an id, and clear links on despawn.
- **`preload` pins a resource for as long as the script is loaded**; use `load()` for anything you mean
  to unload. The resource cache is otherwise weak.
- **Pooling**: instantiating a small scene costs about 3 µs and freeing it about the same; pool only past
  a few hundred churns per frame. `Node.duplicate()` was ten times slower than instantiating the
  `PackedScene`. A pooled node outside the tree is an orphan until freed.
- **Textures used in 3D are VRAM-compressed with mipmaps.** A texture assigned only from code, or made
  with `ImageTexture.create_from_image`, stays lossless without mipmaps — four to six times the video
  memory, shimmering at a distance. Set the import options explicitly; call `generate_mipmaps()` and
  `compress()` on runtime images.
