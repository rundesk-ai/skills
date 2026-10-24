# Large and infinite worlds

A world too big to hold — a Factorio-style map, a planet of city blocks — is your own compact data in
fixed-size chunks, with engine nodes only for the chunks near the camera. How to chunk is an
engine-neutral decision; this is what Godot charges for each part. Figures are from Godot 4.7.2 on one
fast desktop: measure the worst frame on the slowest target before trusting a budget.

## Keep the world out of the scene tree

| Holding 409,600 cells | Memory |
|---|---|
| `TileMapLayer`s, one per 64×64 chunk or one big layer | about 360 bytes per cell either way |
| RenderingServer canvas items, draw only | about 85 bytes per cell |
| your own `PackedByteArray` / `PackedInt32Array` | 1 / 4 bytes per cell |

A 1024×1024 world held entirely in `TileMapLayer`s is about 380 MB; held as bytes it is 1 MB. In 3D,
a `MeshInstance3D` costs about 4.5 KB: 40,000 nodes took 236 MB against 54 MB for one MultiMesh.

- **The world is data; a chunk's nodes are its view.** Generate, simulate and save from packed arrays,
  and build a `TileMapLayer`, a mesh or a MultiMesh only for chunks in the loaded ring.
- **One node subtree per chunk, with chunk-local coordinates**, so a chunk loads as one `add_child` and
  unloads as one `queue_free`, and tile coordinates stay inside the 16-bit range a `TileMapLayer` saves.
- Off-screen chunks cost almost no render time — 100 loaded chunks with one on screen drew in 0.14 ms —
  because canvas items and 3D instances are culled by their bounds. Unload for memory, not for speed.

## Build on workers, attach on the main thread under a budget

The scene tree is not thread-safe, but building nodes **outside** the tree is allowed, and plain data
(packed arrays, images) can be built anywhere.

1. A `WorkerThreadPool` task generates the chunk's cells and, for 3D, its vertex arrays, reading only
   immutable or locked world data.
2. It pushes the finished data onto a queue guarded by a `Mutex`.
3. The main thread pops chunks in `_process` and attaches them under a time **and** count budget.

```gdscript
const BUDGET_USEC := 3000
const MAX_PER_FRAME := 3

func _process(_delta: float) -> void:
	var start := Time.get_ticks_usec()
	var n := 0
	while n < MAX_PER_FRAME and Time.get_ticks_usec() - start < BUDGET_USEC:
		_queue_mutex.lock()
		var job = _ready_chunks.pop_front()
		_queue_mutex.unlock()
		if job == null:
			break
		_attach(job)
		n += 1
```

- **Each chunk is milliseconds on the main thread.** A 64×64 `TileMapLayer` chunk cost 2–3 ms to attach:
  one per frame held 16.7 ms frames, sixteen per frame produced a 47 ms frame. Load a ring wider than the
  screen so a chunk is ready before it is seen.
- **Budget by count as well as time.** In 3D, `ArrayMesh.add_surface_from_arrays` took 0.04 ms at the
  median and 7–13 ms four or five times per 256 chunks, so a 4 ms time budget still produced 18 ms
  frames. Measure the worst frame, not the average.
- **On the default render thread model, build arrays on workers and create Mesh and Shape resources on
  the main thread.** Building the `ArrayMesh` on a worker ran without errors but moved the stall into
  `add_child`; the separate render thread model removed it but is marked experimental and logged errors
  at exit.
- **2D chunk data as bytes**: assigning `layer.tile_map_data` from a `PackedByteArray` built on a worker
  matched `set_cell` cell for cell (0.33 ms to assign). The layout — a 2-byte header, then 12 bytes per
  cell: `int16 x, int16 y, uint16 source, uint16 atlas_x, uint16 atlas_y, uint16 alternative` — is
  observed, not documented; pin it with a round-trip test so an engine upgrade fails loudly.
- **Collision for terrain is a `HeightMapShape3D`**, about 1 ms; a 131,072-triangle
  `ConcavePolygonShape3D` cost 56 ms on the main thread, and Jolt defers that cost to the moment the body
  enters the space, so a worker does not save it. Buildings get primitive shapes, or none and a grid
  lookup. A `HeightMapShape3D` is centred on its node: offset it by half a chunk.
- **Props: one `MultiMeshInstance3D` per prop type per chunk**, filled with one `buffer` assignment built
  on the worker, with `visibility_range_end` so distant chunks drop their props. One MultiMesh for the
  whole world is never culled and shares one LOD.
- Budget `ResourceLoader.load_threaded_request` streaming the same way. One owner calls
  `load_threaded_get`: the second call for a path returns `null`.

## Unloading, and proving memory comes back

- Unload is one `queue_free` of the chunk's root, plus everything nothing frees for you: server RIDs,
  dictionary and cache entries, `RefCounted` back-references, and `preload`s (see
  [Performance and memory](performance-and-memory.md)).
- A chunk still loading when the player leaves is awaited, then dropped instead of attached.
- **Soak-test it**: walk the camera in one direction for minutes, and compare
  `MEMORY_STATIC`, `RENDER_VIDEO_MEM_USED`, `OBJECT_RESOURCE_COUNT` and `OBJECT_ORPHAN_NODE_COUNT`
  between load-unload cycles, sampled about 30 frames after an unload. The first cycle never returns to
  the starting baseline (allocator pools, pipelines); a leak is growth from cycle to cycle. Over four
  cycles of 256 chunks, cycles 2 to 4 matched exactly. `MEMORY_STATIC` reads 0 in release builds.

## Far from the origin

`Vector2`, `Vector3` and node positions are 32-bit in official builds, though GDScript `float` is 64-bit:
`x = 50000.01` is stored as `50000.0117`, a 0.3-pixel move is lost entirely at `x = 10,000,000`, and a
1 cm move is lost at a million units. The docs suggest staying within roughly 16,384–32,768 units for a
top-down game.

- **Keep simulation positions as integers** — chunk coordinates plus a local offset — and convert to
  view space at the boundary. In C#, `Vector3` is the same 32-bit `real_t`.
- **Re-centre in whole chunks** (community practice; the recipe was not run here). When the camera's target passes a threshold, subtract a whole number of
  chunks from every world root and the camera, add it to an `origin_chunk` the view adds back, and call
  `reset_physics_interpolation()` on everything that moved. Particles in global coordinates and
  world-space shader effects jump on the shift.
- A double-precision engine build needs custom editor and export templates, and does not help 2D
  rendering at all.
