---
name: building-isometric-worlds
description: Use when designing, implementing, debugging, or reviewing a 2D isometric or dimetric world's projection, grid-to-screen conversion, elevated or sloped picking, sprite footpoints, depth and occlusion order, stacked surfaces, viewport culling, or quarter-turn view rotation. It supplies engine-neutral coordinate and visibility contracts that keep drawing, interaction, and ordering in agreement. Do not use it for tile simulation or autotiling, general renderer architecture, camera feel, engine APIs, or asset production alone.
---

# Build isometric worlds

Treat the view as one coordinate-and-visibility contract. A scene that looks isometric but uses
different assumptions for drawing, picking, anchors, depth, and culling will fail first at elevation,
overlap, viewport edges, or rotation.

## Keep the boundary narrow

Tile state, autotiling, renderer architecture, and sprite production are their own work, and so are
player-facing pan, zoom, framing, transition feel, input feel, and comfort. This skill still owns the
mathematical quarter-turn transform, inverse picking, depth, culling, and directional-data remap. Use
the engine's and language's own guidance for concrete APIs and ownership.

Authoritative simulation state and snapshots, world-generation stages and seeds, and runtime animation
state belong to the systems that produce them. This skill projects and inspects their accepted semantic
output without taking ownership of those systems.

This skill owns the contract those systems meet: where a world point appears, which surface a pointer
hits, where a sprite touches the ground, which overlapping element is visible, and which world content
may affect the viewport.

## Freeze the coordinate contract

Name every space before writing conversion code:

```text
grid cell + local subcell + world elevation
-> view-oriented grid
-> projected world pixels
-> camera/view coordinates
-> device or pointer coordinates
```

Record axis directions, origin, tile basis vectors, elevation units and sign, camera transform order,
map bounds, rotation convention, and whether coordinates denote a cell corner, centre, surface point,
or object footpoint. Record floor/round and exact-edge tie rules too; implicit rounding usually fails
for negative coordinates or shared diamond edges.

Default to an affine parallel projection. The familiar 2:1 diamond is dimetric; choose true isometric
only when the view or asset contract calls for it. Do not let an engine's perspective default add
foreshortening to a sprite-authored parallel view.

Express the projection once as basis vectors:

```text
project(x, y, z) = origin + x * basis_x + y * basis_y + z * basis_z
```

Derive the inverse from that same basis. Do not maintain a second hand-tuned mouse formula. Read
[coordinate and picking contracts](references/coordinate-and-picking.md) when choosing a projection,
writing its inverse, resolving height, defining slope interpolation, or importing an editor's
coordinate convention.

```text
Good: grid -> orientation -> one projection -> camera; pointer applies exact inverses in reverse.
Bad:  draw with one tile ratio and origin, then copy an unrelated screen-to-tile formula for input.
```

## Make draw and pick share one surface

A flat-plane inverse returns a candidate, not the visible point, when elevation shifts geometry on
screen. Resolve the candidate against the actual surface:

- For one continuous heightfield, solve the projection against the shared surface-height sampler with
  a bounded convergence or ray-intersection method.
- For discontinuities, overhangs, bridges, or stacked floors, gather projected candidate surfaces and
  choose the frontmost selectable hit under the declared occlusion policy.
- Return an explicit miss outside the map. Clamp only when the interaction deliberately promises edge
  clamping; silent clamping turns off-map clicks into edits.

Define slope topology once. Corner heights, chosen triangle diagonal or planar rule, edge-height
interpolation, drawing geometry, normals, picking, placement, and path contact must consume the same
surface function. A four-corner saddle has no unique interior until the topology chooses one.

```text
Good: the rendered triangle and picker call the same height/containment function.
Bad:  render one diagonal, bilinearly pick another surface, and patch disagreement with pixel offsets.
```

## Anchor at the world contact

Give every placeable or moving object a logical footpoint: the world point where it contacts its
support surface. Project that point, then apply a presentation-only sprite offset. Keep the bitmap's
rectangle, pivot, collision footprint, occupied cells, and sorting footprint as distinct data.

For a multi-cell object, declare its occupied world footprint and contact surface; do not infer depth
from the image centre. Use the same footpoint for live rendering, placement ghosts, selection,
animation, and debug overlays. Bottom-centre is a strong default for upright isometric sprites, but
the actual hotspot must be explicit because tall art, asymmetrical bases, and authored offsets vary.

```text
Good: sort and place by a stable ground footpoint; offset the art from that point.
Bad:  sort by texture centre and retune every tall sprite until overlaps look plausible.
```

## Order occlusion, not filenames

Choose the simplest ordering model whose assumptions the world actually satisfies:

- A flat or overhang-free unit-cell surface can use a view-row painter traversal with a documented
  tie order.
- Elevated cells require height or explicit surface order in addition to the row; screen Y alone
  cannot distinguish two surfaces projected onto the same place.
- Tall, multi-cell, moving, or mutually overlapping objects need world footprints or bounding
  volumes. Build only the pairwise dependencies whose screen bounds overlap, then topologically order
  the visible set.
- If dependencies cycle, no whole-sprite painter order is correct. Split geometry/sprites at stable
  occlusion boundaries, use clipping, or use a depth-capable path whose transparency rules are
  explicit.

Represent a stacked surface with stable identity, footprint, height interval or support geometry,
selectability, and occlusion role. A label such as `ground`, `bridge`, or `underground` is not enough
when two instances of the same layer can cross at different heights. Keep an object's dependent pieces
in an assembly contract so a support cannot sort in front of the deck it belongs behind.

Read [depth, visibility, and rotation](references/depth-visibility-and-rotation.md) when the world has
multi-cell objects, stacked surfaces, transparent occluders, aggressive culling, or rotatable views.

```text
Good: establish visible overlap dependencies from world extents, then use a stable tie only when
      neither object occludes the other.
Bad:  reduce every object to `x + y + z` and use arbitrary ID order to hide contradictory overlaps.
```

## Cull from possible pixels

Cull against projected visual extent, not only an anchor or flat inverse rectangle. Invert the
viewport at the supported elevation extremes, take a conservative world bound, then expand for each
visible class's sprite overhang, footprint, animation, and effect extent. Derive the elevation margin
from the projection and the declared height limit; a guessed tile count fails when relief, tile ratio,
or orientation changes.

Keep logical occupancy bounds and visual bounds separate. The former answers simulation questions;
the latter answers whether any pixel can reach the viewport. When the camera or orientation changes,
recompute through the same transform chain rather than swapping axis names in an old cull formula.

## Treat every rotation as a complete view

Keep stored world coordinates orientation-independent. Define a finite world-to-view remap and exact
inverse for each supported orientation, including non-square map dimensions. Feed the remapped point
through the unchanged projection when that matches the rendering model.

Rotate every directional consumer together: projection input, inverse pick, depth direction, cull
bounds, footprint extents, slope or edge directions, directional sprite selection, and editor/minimap
overlays. Rotating only the container or the artwork may preserve appearance while leaving selection,
occlusion, or culling in the old orientation.

```text
Good: orientation is a tested transform used by draw, pick, depth, cull, and directional lookup.
Bad:  rotate the picture 90 degrees and keep the old painter key, hit test, and bounding boxes.
```

## Inspect composed worlds through the player view

Inspect semantic world state and its projected result together. Make diagnostic overlays resolve
stable surface, object, support, footprint, and generator-output IDs from the same snapshot used to
draw; do not infer meaning back from sprite names or screen positions. Keep generator stage, seed, and
rule evidence upstream, then carry stable identities through projection so a visible defect can be
traced to world data, content metadata, or view math.

Review a deliberately small composition matrix before accepting a large world:

- whole-world or region context at minimum supported zoom;
- normal navigation and editing at typical player zoom;
- object, seam, picking, and state readability at maximum supported zoom;
- all supported quarter-turn orientations, including non-square bounds and directional art;
- flat, minimum, and maximum elevation plus cliffs, slopes, bridges, underground reveals, and stacked
  selectable surfaces;
- quiet and dense compositions with tall overhangs, animated extents, map edges, and viewport edges.

Use identical semantic fixtures across orientations and zooms. If the same semantic state projects,
picks, sorts, or culls differently from the declared view contract, fix this projection boundary. If
the semantic state itself contains repeated impossible support, adjacency, placement, or generation
results, fix its owning tile, simulation, content, or generator rule instead of adding sprite offsets
or orientation-specific exceptions here.

Generated-world screenshots are evidence only when they show the actual player camera and can be
matched to semantic fixtures, invariants, and stable IDs. A beautiful wide shot cannot prove close
picking, stacked occlusion, rotation parity, or viewport-edge coverage.

## Prove parity and boundaries

Automate mathematical proof separately from live visual proof:

- Round-trip integer and fractional grid points through forward/inverse transforms at every
  orientation, including negative coordinates, boundaries, and non-square maps.
- Pin centres, corners, shared edges, rounding ties, maximum elevation, both slope facings, saddles,
  cliffs or discontinuities, and off-map misses.
- Compare the surface identifier and local point chosen by picking with the surface actually submitted
  for drawing at the sampled pixel.
- Overlay footpoints, footprints, projected bounds, sort dependencies, and cull bounds in a diagnostic
  view; remove or gate the overlay before shipping.
- Exercise tall-over-short, multi-cell overlap, bridge-over-ground, underground reveal, transparent
  occluders, and at least one deliberately cyclic painter case.
- Sweep every viewport edge, supported zoom, maximum visual overhang, and orientation; a tile or object
  whose pixels touch the viewport must not be culled.
- Assert four quarter-turns return identity and every orientation map round-trips exactly.
- Capture the composition matrix at minimum, typical, and maximum player zoom for every orientation;
  link each failure to the semantic fixture and projected IDs that produced it.
- Inspect the running renderer. A numeric round-trip cannot detect a content-scale, pivot, blend, or
  sprite-bounds mismatch that exists only in the live pipeline.

Deliver the named coordinate spaces, projection and inverse, surface-height/topology contract,
rounding and hit policy, footpoint convention, ordering model with its assumptions, stacked-surface
schema, cull derivation, orientation maps, automated fixtures, multiscale composition evidence, and
unresolved visual sign-offs. The evidence and limits behind these defaults are in
[sources.md](references/sources.md).
