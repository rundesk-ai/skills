---
name: building-tile-based-worlds
description: Use when designing, implementing, or reviewing tile maps, board grids, terrain autotiling, multi-cell placement, occupancy, stacked cells, map-edit commands, or incremental tile-world updates. It supplies engine-neutral contracts for grid storage, neighborhood rules, transactional edits, footprints, and dirty propagation. Do not use it for pathfinding, engine APIs, isometric projection or depth, camera behavior, or generic rendering.
---

# Build tile-based worlds

Make semantic grid state authoritative. Treat sprites, meshes, colliders, connectivity masks, and
chunk products as derived views that can be rebuilt from it. This separation keeps saves stable,
previews honest, and incremental updates comparable with a full rebuild.

## Establish one grid contract

Write the contract before choosing containers or editor tools:

- topology: square-4, square-8, hex, or a custom graph of cells, edges, and vertices;
- coordinate type, axis names, origin, orientation, and allowed rotations;
- ordered neighbor offsets and whether each relation is an edge, corner, or vertical connection;
- bounded, wrapped, or unbounded border semantics;
- cell size and the one service that maps canonical cell coordinates to world positions and back;
- storage model, chunk size, empty-cell meaning, and serialization order;
- height model, occupancy categories, and edit revision rules.

Use integer logical coordinates for authoritative cell identity. Keep screen, local, and world
coordinates outside cell keys. Keep isometric conversion and draw-depth math outside the grid;
do not let its projection become the simulation grid.

For half-offset or hex layouts, route every neighbor, rotation, pattern paste, and conversion through
the topology object. Arithmetic that happens to work on one row parity will fail on the other.

```text
# Good — Pair A: storage and conversions share one canonical contract.
cell = topology.worldToCell(worldPoint)
chunk = floorDiv(cell, chunkSize)
local = cell - chunk * chunkSize

# Bad — Pair A: tools invent coordinates independently.
cell = round(worldPoint / tilePixels)
chunk = truncateTowardZero(cell / chunkSize)
```

Mathematical floor division matters when unbounded maps admit negative coordinates. Test the cells
immediately on both sides of zero and every chunk boundary.

## Choose storage from world shape

Prefer the simplest representation that preserves the contract:

| World shape | Default storage | Deviation trigger |
|---|---|---|
| Small, fixed rectangle | Dense row-major array | Holes dominate or resize is frequent |
| Large or unbounded 2D world | Sparse map of fixed-size chunks | A dense region is proven simpler and cheaper |
| Irregular finite hex board | Dense rows behind an accessor or sparse coordinate map | Memory evidence justifies compressed rows |
| Independent cells at several heights | Sparse 3D chunks | Only one surface value can exist per horizontal cell |

Keep chunking behind grid accessors. Persist chunk coordinates and local coordinates explicitly, and
sort coordinates canonically when save bytes, hashes, replays, or network messages must be stable.
Do not make hash-map iteration order part of simulation behavior.

Separate stable semantic fields such as terrain, elevation, moisture, ownership, or damage from
derived presentation identifiers.

```text
# Good — Pair B: durable meaning selects presentation.
cell.terrain = GRASS
sprite = resolveVisual(cell, neighborhood(cell), stableVariationKey(cell))

# Bad — Pair B: an atlas slot becomes world truth.
cell.tileId = 184  # meaning changes when the atlas or transition set changes
```

## Model height explicitly

Choose one height model; do not overload render order, sprite origin, or a layer name:

- **Surface field:** store one elevation plus surface properties per horizontal cell. Use it when
  overhangs and independently occupied levels cannot exist.
- **Stacked slots:** key state by `(cell, level)` and define vertical adjacency, support, and clearance.
  Use it for floors, bridges, cliffs, or discrete stacked boards.
- **Sparse volume:** key state by `(x, y, z)` in chunks. Use it when arbitrary cells can exist above or
  below one another.

Define whether a wall, road, river, or door occupies a cell or the edge between two cells. If it is a
relationship, give the edge a canonical identity such as the sorted endpoints; duplicating it into
both cells creates disagreement during edits.

## Resolve connectivity from semantics

Define the visual rule as a pure function:

```text
visual = resolve(kind, orderedNeighborSignature, stableVariationKey)
```

Build `orderedNeighborSignature` from topology relations, not from sprite IDs. Select only the
relations the art set models: edges for pipes and roads, corners for corner transitions, or both for
blob terrain. Store those read offsets with the resolver so invalidation can be derived from the same
contract.

Keep transition validity separate from cosmetic variation. Enumerate supported signatures and make
missing combinations visible in validation. Choose a deliberate fallback tile only when it preserves
meaning; an arbitrary closest match hides holes until a rare neighborhood appears in production.

Use a stable variation key derived from world seed, canonical coordinate, and a versioned rule salt.
If a chosen variation changes gameplay, persist that choice as semantic state instead of regenerating
it. Weighted variation changes frequency, not connectivity validity.

When a semantic cell `x` changes and an output at `c` reads `c + d`, invalidate `x - d` for every read
offset `d`. This reverse-dependency rule handles edge, corner, and extended patterns without a
hand-maintained magic radius.

## Own complete footprints and occupancy

Define each placeable item's footprint as canonical local offsets from a declared anchor. For every
allowed orientation, transform the offsets using the topology's discrete rotation, then reject
duplicates and out-of-contract coordinates. Include occupied height slots, required support, and
reserved edges when those affect validity.

Maintain both directions:

```text
occupantAt[slot] -> ownerId
placementOf[ownerId] -> anchor, orientation, exact occupied slots and edges
```

The reverse record makes removal and undo exact; never reconstruct an old footprint from a mutable
definition. During a move, let the owner overlap its own old footprint but reject every conflicting
owner in the destination set.

```text
# Good — Pair C: validate and claim the rotated footprint as one set.
slots = footprint(definition, anchor, orientation)
require every slot is inBounds, supported, and freeOrOwnedBy(item)
claimAll(item, slots)

# Bad — Pair C: reserve only the anchor and trust the visual bounds.
require occupantAt[anchor] is empty
occupantAt[anchor] = item
```

Return structured rejection reasons with the exact conflicting cells or edges. The UI can then mark
the same facts the commit path will enforce.

## Plan once, preview and commit the same edit

Represent every brush stroke, terrain fill, placement, move, removal, or stacked edit as a request.
Run one pure planner against an immutable snapshot:

```text
EditPlan {
  baseRevision
  ordered primary changes with before and after values
  occupancy releases and claims
  affected semantic cells and edges
  rejection reasons
}
```

The preview renders `EditPlan`; it does not run an approximation. Commit rechecks the base revision
or recorded preconditions, applies the complete plan, increments the revision, records the changed
before-values for undo, and enqueues invalidation once. If any precondition fails, apply nothing and
replan from current state.

```text
# Good — Pair D: preview and execution consume one validated plan.
plan = planEdit(snapshot, request)
preview(plan)
commit(plan) only if world.revision == plan.baseRevision

# Bad — Pair D: preview and execution implement separate placement rules.
preview = testVisibleColliders(cursorShape)
commit = testAnchorCellAndSpendResources(request)
```

Apply changes in canonical order when conflicts, events, replays, or deterministic simulation can
observe ordering. Encapsulate edits as commands when undo, redo, replay, or tooling needs them; store
the small changed subset rather than copying the entire world.

## Propagate dirt from primary changes

Have the mutation boundary emit one change set. Derive affected outputs from declared dependencies:

| Derived product | Dependency default | Edit behavior |
|---|---|---|
| Local | Exact read offsets or footprint intersections | Invert the reads into a bounded dirty closure |
| Regional | Chunk, connected component, watershed, or other declared region | Queue and coalesce that named region for a synchronization point |
| Globally coupled | The result can depend on arbitrary world state | Run a declared global or proven incremental algorithm; never disguise it as a local update |

Classify each product before optimizing it. A local semantic edit must not trigger hidden whole-world
work through an innocent-looking getter, render request, or per-cell callback. If policy selects a
full rebuild because the dirty set crossed a measured threshold, expose that selection in metrics
and run it once, not once per changed cell.

1. Add changed cells, changed edges, released footprints, and claimed footprints.
2. Expand local products using each resolver's reverse read offsets or footprint dependencies.
3. Resolve regional products to their declared chunks, components, or bounded recomputation areas.
4. Mark every derived cache that consumes the affected semantics.
5. Union repeated work by cell, edge, region, chunk, and cache type.
6. Rebuild lazily when queried or once at the scheduled synchronization point.
7. Clear dirty state only after the new product is installed successfully.

```text
# Good — Pair E: accumulate an exact dirty closure and rebuild once.
dirty.merge(impactOf(plan))
endOfTick: rebuild(dirty.take())

# Bad — Pair E: each cell write immediately rebuilds the whole map.
for change in plan.changes:
    write(change)
    rebuildAllDerivedData()
```

Measure a crossover for switching from incremental to full rebuild; do not assume incremental is
always cheaper. Keep correctness independent of that choice by comparing the installed incremental
or regional product with a clean full-reference build from the same semantic state. If a product is
deliberately approximate, declare its error or invariant contract and compare it with a separate
reference instead of silently weakening equality.

## Prove the contracts

Add small exhaustive fixtures before large visual maps:

- round-trip canonical cell/world samples and test negative chunk boundaries;
- verify neighbor count, opposite-direction symmetry where applicable, and border behavior;
- enumerate every supported connectivity signature and assert missing ones fail visibly;
- compare local autotile recomputation with a full-map recomputation after each edit;
- compare every incremental and regional derived-data path with its clean reference across isolated,
  clustered, chunk-seam, and threshold-crossing edits;
- rotate asymmetric footprints through every allowed orientation and verify occupancy's two indexes;
- reject a batch midway and assert the world is unchanged; apply then undo and assert exact equality;
- assert previewed cells, reasons, and costs equal the committed plan;
- replay the same ordered requests from the same seed and compare semantic hashes;
- serialize, reload, and compare semantic state without comparing rebuildable presentation caches;
- benchmark sparse edits, large fills, and edits spanning chunk seams before tuning chunk size or the
  incremental/full-rebuild threshold.

Instrument changed semantic cells, expanded dirty cells, affected regions, touched chunks, rebuild
time, selected rebuild policy, and fallback-rule hits. A regional or full rebuild may be correct;
unobserved use makes a hidden world scan or policy regression hard to distinguish from intended work.

## Keep boundaries clear

- Use the engine's own guidance for API names and lifetime rules.
- Leave simulation cadences and globally coupled fields, networks, stocks, or agent systems to the
  world simulation; this skill owns their tile-coordinate dependency and dirty-set boundary.
- Leave staged seeded generation, cross-stage invariants, repair, and seed sweeps to world
  generation; this skill owns the authoritative grid and the tile products installed from it.
- Treat pathfinding and agent movement as consumers of semantic grid state; do not make them owners
  of terrain, placement, or occupancy truth.

Read [references/sources.md](references/sources.md) when auditing these rules, changing topology or
terrain strategy, or adapting a good/bad pair.
