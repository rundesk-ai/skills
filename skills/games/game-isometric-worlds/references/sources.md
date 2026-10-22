# Sources

This skill synthesizes public documentation, source code,
named-practitioner explanations, public failure reports, and anonymized project evidence.
It does not prescribe one engine, tile ratio, height grammar, sort constant, or picking algorithm for
all isometric games.

## Projection, inversion, and editor coordinates

- Unity,
  [Creating an Isometric Tilemap (2020.1)](https://docs.unity3d.com/2020.1/Documentation/Manual/Tilemap-Isometric-CreateIso.html),
  distinguishes its default dimetric cell ratio (`1, 0.5, 1`) from true isometric (`y = 0.57735`),
  documents parallel isometric layouts and Z-as-Y height, and demonstrates that a flat Y sorting axis
  orders stacked Z tiles incorrectly. The named numeric sort bias is Unity-specific and is not reused
  as a portable constant.
- Clint Bellanger,
  [Isometric Tiles Math](https://clintbellanger.net/articles/isometric_math/), derives one common
  diamond grid-to-screen transform and its algebraic inverse from half-tile basis vectors. This is
  named-practitioner teaching for a 2:1 convention, not proof that every game should use that ratio,
  handedness, origin, or rounding policy.
- Tiled,
  [Editing Tilesets](https://docs.mapeditor.org/en/stable/manual/editing-tilesets/) and
  [Working with Objects](https://docs.mapeditor.org/en/stable/manual/objects/), documents tile-object
  alignment, drawing offsets, and bottom-centre alignment as the unspecified default for isometric
  tile objects. This supports separating a world footpoint from bitmap bounds; projects must still
  honor explicit imported alignment rather than assuming Tiled's default.
- Tiled,
  [Working with Layers](https://docs.mapeditor.org/en/stable/manual/layers/) and the
  [TMX map format](https://docs.mapeditor.org/en/stable/reference/tmx-map-format/), documents that
  non-staggered isometric object coordinates use a projected coordinate space and that map orientation,
  render order, tile dimensions, offsets, and layer order are separate stored contracts. These are
  editor/file semantics, not a runtime renderer architecture.

## Height-aware picking and conservative bounds

- OpenTTD source at commit
  [`abf2843`, `landscape.h` projection functions](https://github.com/OpenTTD/OpenTTD/blob/abf28430690ee05aaf4f81b20ac9f0e8d63f66ef/src/landscape.h#L81-L117)
  defines `RemapCoords`, flat `InverseRemapCoords`, and a separate height-aware inverse contract. It
  establishes a production source example where forward projection includes elevation and the flat
  inverse explicitly assumes `z == 0`; its integer scale and axis convention are OpenTTD-specific.
- OpenTTD source at the same commit,
  [`InverseRemapCoords2`](https://github.com/OpenTTD/OpenTTD/blob/abf28430690ee05aaf4f81b20ac9f0e8d63f66ef/src/landscape.cpp#L121-L170)
  and
  [`GetPartialPixelZ`](https://github.com/OpenTTD/OpenTTD/blob/abf28430690ee05aaf4f81b20ac9f0e8d63f66ef/src/landscape.cpp#L238-L337),
  starts from the flat inverse, performs bounded fixed-point height sampling, approaches discontinuous
  foundations from behind so regions remain clickable, and derives extra map-edge allowance from the
  configured height limit. This supports height-aware picking, shared slope sampling, and derived cull
  margins. Its iteration counts, malus, slope catalogue, and clamping behavior are implementation
  evidence, not universal constants.

## Depth, occlusion, and rotation failures

- Shaun LeBron,
  [Drawing isometric boxes in the correct order](https://shaunlebron.github.io/IsometricBlocks/),
  derives projected-overlap and separating-axis dependencies for non-intersecting axis-aligned boxes,
  orders them topologically, demonstrates a dependency cycle, and discusses splitting/clipping or a
  depth buffer. This named-practitioner construction supports escalating beyond one scalar key; it does
  not directly cover intersecting volumes, arbitrary meshes, transparency, or a broad-phase strategy.
- OpenRCT2 issue
  [#22617](https://github.com/OpenRCT2/OpenRCT2/issues/22617) reproduces sloped wooden supports drawing
  over a diagonal track beneath them in a specific stacked crossing. It is public failure evidence that
  tile membership and nominal elevation alone do not settle multi-piece occlusion; it does not establish
  the skill's proposed data schema.
- OpenRCT2 merged pull request
  [#25002](https://github.com/OpenRCT2/OpenRCT2/pull/25002) records a track drawing glitch caused by
  bounding-box differences across camera angles; the author notes one rotation happened to avoid the
  bug. It supports making bounds and ordering first-class in every orientation, but its exact track
  bounds and fix are asset-specific.
- OpenRCT2 issue
  [#18479](https://github.com/OpenRCT2/OpenRCT2/issues/18479) reproduces objects over water disappearing
  near the viewport bottom after tile-element reordering, and
  [#24805](https://github.com/OpenRCT2/OpenRCT2/issues/24805) records a backside tunnel occlusion/reveal
  failure. Together they support combined viewport-edge, stacked-layer, and orientation/reveal tests;
  open or historical issues are failure reports, not proof of a general solution.
- Microsoft,
  [Xbox Accessibility Guideline 109: Object clarity](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/109),
  requires important game objects and interactive elements to remain identifiable and recommends
  assessing clarity in game context. It supports player-view composition checks rather than isolated
  sprite review. It does not define an isometric zoom set, projection, or sorting algorithm.

## Anonymized project evidence

- In one 2D isometric city-builder, a flat-plane inverse selected the wrong tile on raised and sloped
  terrain until drawing and picking shared one height sampler and topology; a height-derived cull
  expansion prevented raised far-edge holes; and hand-picked seam scenes missed overlap combinations
  that an exhaustive adjacent-state matrix later exposed. These support the draw/pick parity,
  derived-cull, and exhaustive-proof defaults.
- In the same project, numeric projection checks passed while the live window showed separated
  terrain tiles caused by a pixel/point content-scale mismatch. This supports keeping live rendered
  inspection after mathematical tests.

This is one game in one engine: practitioner failure evidence, not an independently reproducible
benchmark.

## Good/bad mapping

- The one-basis/inverse pair applies Bellanger's algebra, OpenTTD's paired forward/flat inverse, and
  Tiled's explicit coordinate contracts. The complete reverse-transform pipeline is a
  conservative integration rule.
- The draw/pick shared-surface pair applies OpenTTD's height-aware inverse and slope sampler plus the
  anonymized mismatch/fix. The exact intersection method remains topology-dependent.
- The footpoint pair applies Tiled's isometric bottom-centre alignment and drawing-offset distinction.
  Calling bottom-centre a default, rather than a requirement, preserves the source's explicit override.
- The dependency-graph pair applies LeBron's partial-order construction and cycle counterexample, with
  OpenRCT2 #22617 as a shipped-world failure. Stable tie-breaking is a determinism conclusion, not a
  claim made by those sources.
- The rotation pair applies OpenRCT2 #25002 and the anonymized combined cull/order evidence. The remap
  table is algebra derived and round-trip checked for the coordinate convention documented in the
  reference, not copied from an engine.
- The multiscale composition matrix is a conservative integration rule. Xbox object
  clarity supports in-context inspection; OpenRCT2 failures support rotation, stacked-layer, and
  viewport-edge cases. None establishes that three zoom samples are sufficient for every game, so
  projects must add camera states and semantic fixtures required by their actual player contract.
