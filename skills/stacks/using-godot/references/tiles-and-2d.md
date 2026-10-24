# Tiles, isometric and 2D at scale

Examples are GDScript; C# uses the same names in PascalCase. Figures are from Godot 4.7.2 on one fast
desktop; read them as ratios.

## TileMapLayer

Use one `TileMapLayer` node per layer (4.3+); `TileMap` is deprecated and gets no new features.

```gdscript
var ts := TileSet.new()
ts.tile_shape = TileSet.TILE_SHAPE_ISOMETRIC          # shape, layout and size before the tiles
ts.tile_layout = TileSet.TILE_LAYOUT_DIAMOND_DOWN     # the isometric default is STACKED
ts.tile_size = Vector2i(64, 32)
var src := TileSetAtlasSource.new()
src.texture = load("res://art/iso_tiles.png")         # an imported file saves as a reference
src.texture_region_size = Vector2i(64, 32)            # may be taller than tile_size for tall art
var source_id := ts.add_source(src)
for x in 4:
	for y in 4:
		src.create_tile(Vector2i(x, y))
```

- **An isometric TileSet defaults to the stacked (staggered) layout, not diamond.** Code that assumes
  `(x + 1, y)` is the next diamond down-right builds a zig-zag. Set `tile_layout` deliberately.
- **Ask the layer for neighbours** — `get_surrounding_cells(c)`, `get_neighbor_cell(c, side)` — on
  isometric, half-offset and hex maps: hex neighbours differ between odd and even rows. A simulation
  outside the engine that needs the same rule copies it from the layer once, in a test.
- `map_to_local` returns the cell centre, and `local_to_map` round-trips on every shape and layout; a
  wrong pick is a coordinate-space bug, not the engine's isometric maths.
- **`set_cell` does not check atlas coordinates**: an unknown tile stores data and draws nothing,
  silently. Check `TileSetAtlasSource.has_tile(coords)` in your placement helper.
- Tall art (a building above its floor diamond) uses a taller `texture_region_size` and
  `TileData.texture_origin` to shift it.

### Picking a cell under the mouse

Convert screen → canvas → the layer's own local space:

```gdscript
var cell := layer.local_to_map(layer.to_local(get_global_mouse_position()))
# from an event: get_viewport().get_canvas_transform().affine_inverse() * event.position
```

`layer.local_to_map(event.position)` works only with the camera at the origin, unzoomed, and the layer
unmoved and unscaled — which is exactly the state a first test runs in.

### Y-sorting units against tiles

With `y_sort_enabled` on a layer, units sort against its tiles only when they are **children of that
layer**, or siblings of it **under a parent that is also y-sorted**. A y-sorted layer alone sorts only its
own tiles and children; units beside it draw in tree order (checked by reading pixels after rendering).

- A tile sorts at its cell centre plus `TileData.y_sort_origin` plus the layer's `y_sort_origin`. Put a
  tall building's sort point at its feet.
- **`z_index` overrides y-sort.** Keep everything that sorts together on one `z_index`.
- A y-sorted layer ignores `rendering_quadrant_size` and groups tiles by row instead, costing more canvas
  items. Keep flat ground on its own unsorted layer and y-sort only walls, buildings and trees.

### What tile edits cost

| Work | Cost |
|---|---|
| `set_cell` over 512×512 | 31 ms, then 8.6 ms to build internals |
| first frame of a 256×256 layer: plain / one physics layer / a navigation polygon on every tile | 38–49 / 67 / 284–586 ms |
| one cell erased on a built map, then `update_internals()` | 0.1–0.35 ms |
| `set_cells_terrain_connect` over 128×128 | 162 ms — about 80 times raw `set_cell` |

- Edits are batched to the end of the frame. `update_internals()` applies them now and is expensive:
  call it once after a batch, never per cell. A scene tile's node does not exist until then.
- **Do not autotile with `set_cells_terrain_connect` at runtime or in generation.** It is slow, and its
  result depends on paint order. Keep terrain ids in your own grid, compute each cell's neighbour mask,
  map mask to atlas coordinates through a table, and `set_cell` directly; on an edit, recompute the cell
  and its eight neighbours.


- Do not set `physics_quadrant_size` to 1: it stops merging collision shapes, and the first frame tripled.
- **Saved tile coordinates are 16-bit**: a cell at `(40000, 0)` comes back as `(-25536, 0)`. A world that
  can pass ±32,767 cells gives each layer chunk-local coordinates; see [Large worlds](large-worlds.md).

## Pathfinding on grids

Use `AStarGrid2D` or your own field on a grid game; disable `navigation_enabled` on the layers.

- **`update()` wipes every solid point and weight.** Set `region`, `cell_size`, `offset` and
  `cell_shape`, call `update()`, then apply solids from your map data — and again after every later
  `update()`. A query before the first `update()` logs "Grid is not initialized" and returns `[]`.
- **The default diagonal mode cuts between two diagonal walls.** Use
  `DIAGONAL_MODE_ONLY_IF_NO_OBSTACLES` for units with a body, or `NEVER` for four-way movement.
- `get_point_path` returns cell corners unless `offset` is half a cell. Prefer `get_id_path` and convert
  each cell with `layer.map_to_local`, which is right on every shape; set `cell_shape` to match an
  isometric layer.
- **An unreachable target searches the whole grid** (33 ms on 512×512). Keep a connected-component id
  per cell, recomputed on map change, and refuse a job whose target is in another component before
  asking A*. In a colony sim, "no path" is common.
- `jumping_enabled` returns sparse waypoints and ignores weights.
- **Many units to one destination share one field.** 500 `get_id_path` calls to one goal took 178 ms;
  one breadth-first distance field over a `PackedInt32Array`, in GDScript, took 13 ms and matched every
  path length. Each unit steps to its lowest neighbour. Recompute on map change, across frames or on a
  worker.
- Per-tile navigation polygons build a region per cell. For free movement, bake one navigation polygon
  per chunk; a hundred `NavigationAgent2D`s is reported (not measured here) to drop frame rate sharply.

## Many sprites

20,000 moving sprites, windowed, Forward+:

| Approach | Render CPU | Update cost |
|---|---|---|
| 20,000 `Sprite2D` nodes | 2.2 ms | 3.4 ms setting `position` |
| 20,000 RenderingServer canvas items | 2.2–3.0 ms | 1.7 ms |
| one node drawing 20,000 textures in `_draw` | 0.2–0.4 ms | 0.7–0.9 ms per redraw |
| one `MultiMeshInstance2D`, buffer rebuilt each frame | 0.03–0.14 ms | 2.6 ms filling the buffer |

- 2D batching is on in every renderer from 4.4 (20,000 sprites sharing a texture were 2 draw calls); in
  4.0–4.3 only Compatibility batched.
- Nodes are fine to about 10,000 on desktop; past that, a `MultiMeshInstance2D` (8 floats per instance:
  `[a.x, b.x, 0, origin.x, a.y, b.y, 0, origin.y]`) or one `_draw` per chunk. A `QuadMesh` for 2D needs
  `size = Vector2(w, -h)` or the texture draws upside down. A MultiMesh does not y-sort its instances
  against other nodes.
- `_draw` output is cached until `queue_redraw()`, so static decoration drawn once is nearly free.
- RenderingServer canvas items you create are yours to free; see [Performance and memory](performance-and-memory.md).

## Pixel art and cameras

The defaults blur pixel art: set `rendering/textures/canvas_textures/default_texture_filter=0`
(Nearest), stretch mode `viewport` and scale mode `integer` (4.2+); use stretch mode `canvas_items`
instead when the game needs sub-pixel motion or a high-resolution UI.

A `Camera2D` updates in idle time by default, so following a body moved in `_physics_process` stair-steps
when the frame rate is not a multiple of the tick rate. Set the camera's `process_callback` to physics,
or enable `physics/common/physics_interpolation` (2D since 4.3) and call `reset_physics_interpolation()`
after a teleport. (Documented; not verified here by eye.)
