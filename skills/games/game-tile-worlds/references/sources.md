# Sources

This skill synthesizes engine-neutral contracts; engine and
tool documentation below supplies evidence about concrete failure modes and established data
models, not a requirement to adopt those products.

## Grid identity, coordinates, and storage

- Amit Patel, [Hexagonal Grids](https://www.redblobgames.com/grids/hexagons/), and
  [Implementation of Hex Grids](https://www.redblobgames.com/grids/hexagons/implementation.html).
  Practitioner reference with executable explanations. It establishes canonical cube/axial
  constraints, table-driven neighbors, conversions between coordinate representations, dense and
  sparse storage choices, and the recommendation to encapsulate storage behind map accessors.
- Amit Patel, [Grid parts and relationships](https://www.redblobgames.com/grids/parts/).
  Practitioner reference distinguishing cell faces, edges, and vertices across square, triangular,
  and hexagonal grids. It supports modeling an edge relationship directly instead of duplicating it
  as unrelated cell state.
- Tiled 1.12.2,
  [JSON Map Format](https://doc.mapeditor.org/en/stable/reference/json-map-format/).
  Primary format documentation. Tile layers have explicit width/height data; infinite maps store
  tile data in chunks with cell-coordinate origins, including negative coordinates. This supports
  bounded dense and unbounded chunked models and motivates mathematical floor division at negative
  chunk boundaries.
- Godot stable,
  [GridMap](https://docs.godotengine.org/en/stable/classes/class_gridmap.html).
  Primary engine documentation. It describes a 3D grid of equal-sized cells split internally into a
  sparse collection of octants. This is evidence for the sparse-volume option, not a universal
  mandate for octrees or 3D storage.
- Unity 6,
  [Working with Heightmaps](https://docs.unity3d.com/6000.0/Documentation/Manual/terrain-Heightmaps.html).
  Primary engine documentation. It represents the height of each terrain point as one value in a
  rectangular array. Together with sparse 3D GridMap cells, this establishes that a surface field
  and an independently occupied volume have materially different data contracts.
- Tiled 1.12.2,
  [Working with Layers](https://doc.mapeditor.org/en/stable/manual/layers/).
  Primary tool documentation. Layer order determines rendering order, while offsets and parallax can
  fake depth. This supports the warning not to treat presentation order as authoritative elevation
  or stacked occupancy.

## Terrain connectivity and rule coverage

- Tiled 1.12.2,
  [Using Terrains](https://doc.mapeditor.org/en/stable/manual/terrain/).
  Primary tool documentation. It distinguishes corner, edge, and mixed terrain sets; states that
  neighboring tiles may be adjusted after an edit; exposes missing patterns; and defines relative
  probabilities only among matching choices. It supports semantic connectivity signatures, explicit
  rule coverage, reverse-neighbor invalidation, and separating valid transitions from variation.
- Tiled 1.12.2,
  [Automapping](https://doc.mapeditor.org/en/stable/manual/automapping/).
  Primary tool documentation plus worked failure cases. It documents explicit Empty/Ignore/Other
  semantics, output overlap that can create partial rocks, ordered versus simultaneous rules, and an
  AutomappingRadius needed when edits influence nearby matches. It supports explicit empty-state
  semantics, deterministic rule ordering, overlap tests, and dependency-radius validation.
- Godot stable,
  [TileMapLayer](https://docs.godotengine.org/en/stable/classes/class_tilemaplayer.html).
  Primary engine documentation. Terrain connection calls can update neighbors and warn that missing
  terrain combinations produce unexpected results. Half-offset pattern mapping cannot safely be
  implemented as coordinate addition. These observations support topology-owned pattern transforms
  and complete/failing-visible connectivity tables.
- Unity Technologies,
  [2D Extras](https://github.com/Unity-Technologies/2d-extras).
  Maintainer source and practitioner examples. Pipeline, Terrain, Rule, Hexagonal Rule, and
  Isometric Rule tiles use different neighbor sets and grid types. This corroborates selecting the
  signature from topology and content rules instead of assuming one universal 8-neighbor mask. The
  repository is archived in favor of the package, so it is not used for current version claims.

## Footprints, commands, and atomic edits

- RTS Engine,
  [Advanced Building Placement Module](https://docs.gamedevspice.com/rtsengine/manual/08_Modules/10_Advanced_Building_Placement.html).
  Vendor practitioner documentation. It defines an occupied cell area and pivot for previews, while
  its 2022.3.0 and 2022.3.1 changelogs record bugs where rotation failed to update or occupy the
  correct cells. This is direct field evidence for storing a declared anchor, transforming the full
  footprint for every orientation, and sharing that result between preview and placement. Its API
  details are not generalized.
- Robert Nystrom,
  [Command](https://gameprogrammingpatterns.com/command.html).
  Named practitioner book chapter. It shows commands carrying the small amount of prior state needed
  for undo and explains that replay can record commands instead of full world snapshots. It supports
  command-shaped edits and changed-subset undo records.
- IETF RFC 6902,
  [JSON Patch](https://www.rfc-editor.org/rfc/rfc6902.html), sections 3 and 5.
  Standards-track specification for ordered partial updates. Operations are evaluated sequentially;
  failure terminates evaluation, and HTTP PATCH application is atomic. The skill does not prescribe
  JSON Patch for games; it adopts the established batch contract that a failed compound edit must
  not expose partial state.

## Dirty propagation and rebuild policy

- Robert Nystrom,
  [Dirty Flag](https://gameprogrammingpatterns.com/dirty-flag.html).
  Named practitioner book chapter. It defines primary versus derived data, marking derived state
  dirty when primary data changes, deferring costly work until needed, and clearing the flag after
  reprocessing. This supports one authoritative semantic grid and rebuildable derived products.
- Godot stable,
  [TileMapLayer](https://docs.godotengine.org/en/stable/classes/class_tilemaplayer.html).
  Primary engine documentation. It warns that runtime updates are costly, exposes modified-cell
  update sets, and batches internal work until the end of the frame. This supports accumulating
  exact dirty sets instead of forcing work per write.
- Unity 6,
  [Tilemap Collider 2D component reference](https://docs.unity3d.com/6000.0/Documentation/Manual/tilemaps/work-with-tilemaps/tilemap-collider-2d-reference.html).
  Primary engine documentation. `Max Tile Change Count` switches collision generation from
  accumulated incremental changes to a full regeneration. This supports measuring a crossover and
  keeping both incremental and full rebuild paths correct.
- Guillaume Pierre,
  [We Built This City on Bits 'n Maps: Four Design Techniques for Simulating Cities in *SimCity* and
  *Cityscapes: Sim Builder*](https://www.gdcvault.com/play/1034401/We-Built-This-City-on), GDC 2024.
  The public session description distinguishes maps, networks and globals, agents, and
  building-to-building connections in responsive city simulations. This is named-practitioner scope
  evidence that world products have materially different dependency shapes; it does not prescribe
  the local/regional/global invalidation table or prove a particular incremental algorithm.

## Good/bad pair traceability

| Pair | Evidence | Lesson synthesized here |
|---|---|---|
| A: canonical conversion and floor chunking | Red Blob coordinate/storage guides; Tiled JSON chunks | Centralize coordinate policy and handle negative chunk coordinates mathematically instead of scattering rounding rules. |
| B: semantics rather than atlas IDs | Tiled terrain and JSON format; Dirty Flag | Keep durable terrain meaning primary and resolve rebuildable tile variants from it. |
| C: complete rotated footprint | RTS Engine placement guide and rotation bug changelogs | Compute, validate, and claim every occupied slot from one anchor/orientation contract; an anchor-only claim cannot prevent overlap. |
| D: one preview/commit plan | RTS Engine preview areas and placement failures; Command; RFC 6902 | Plan one bounded change set, render that plan, recheck preconditions, and commit all-or-nothing. |
| E: dirty closure and batching | Dirty Flag; Godot TileMapLayer; Unity Tilemap Collider 2D | Accumulate affected outputs, batch rebuild work, and measure when a full rebuild wins. |

## Synthesized conclusions

The following are reasoned design conclusions rather than claims that one upstream source states
verbatim:

- Store resolver read offsets and invert them to calculate the exact dirty closure. Tiled and Godot
  establish that neighboring cells change and that the radius matters; the inverse-offset formula is
  the engine-neutral way to keep read and invalidation contracts aligned.
- Derive cosmetic variation from a stable coordinate key. Tiled establishes relative weighted
  choice; the stable key prevents unchanged cells from flickering and makes preview, reload, and full
  rebuild comparable.
- Maintain both `slot -> owner` and `owner -> exact placement`. The practitioner rotation failures
  show why footprints drift; the two indexes make conflicts fast and removal/undo exact.
- Compare incremental output with a full rebuild in tests. Dirty Flag and both engine documents show
  that derived data may be deferred or fully regenerated; equality between paths is the correctness
  oracle independent of optimization policy.
- Classify a derived product as local, regional, or globally coupled from what it reads, not from the
  size of the edit that triggered it. Tiled supplies bounded neighborhood reads, Godot and Dirty Flag
  supply deferred dirty work, Unity supplies an explicit incremental/full crossover, and Pierre's
  practitioner taxonomy establishes that networks and globals differ from cell maps. The three-class
  table and requirement to expose any full-world fallback are a conservative integration
  rule, not terminology copied from one source.
