# Scaling and updates

Read this when work involves culling, live representation churn, batching, atlas or command ceilings,
dirty regions/chunks, cached draw data, or semantic level of detail.

## Cull before materializing work

Query authoritative spatial data or the render snapshot with a conservative visible region, then create or
update render representations only for the result. Hiding a node after it was allocated, animated, sorted,
and submitted does not recover the CPU or lifetime cost.

Expand the cull region from declared content facts:

```text
visible world bounds
+ maximum sprite overhang
+ projection/elevation displacement
+ effect and shadow radius
+ one update/prefetch ring when motion requires it
```

Avoid a hand-tuned margin that happens to cover today's sprites. Recompute it when metadata or the projection
contract changes. For heterogeneous objects, use per-family bounds or a broad phase rather than one enormous
global margin.

Track at least candidates, visible items, culled items, live representations, emitted primitives, and draw
commands. Compare these across map/world size while holding viewport and scene density constant. Profile
and benchmark with a performance method of their own; these counters only show what is bounded.

## Pool only expensive churn

Pool when measurement shows repeated allocation, engine registration, or resource creation is material and
the maximum live set can be bounded. A pool trades allocation churn for a fixed memory and reset policy; it
is not a universal optimization.

On acquire, assign every property that can affect a pixel or callback: identity generation, transform,
pivot, bounds, texture region, shader/material, uniforms, tint, opacity, blend, layer/order, clip, listeners,
animation, visibility, and debug state. On release, stop callbacks, detach external references, and return the
item to a known inert state.

Test reuse across unlike items. A same-kind reacquire can hide stale state that appears only when one pooled
object follows another resource, blend mode, animation, or semantic layer.

Prefer compact frame-owned commands when objects are cheap values. A retained node per possible world item,
even hidden, defeats viewport-bounded rendering; a complicated pool can also cost more than rebuilding a
small command list.

## Batch after ordering

Construct a semantic command stream first. Scan it in order and extend a batch only while every compatibility
field matches:

```text
render pass / target
texture or atlas page
shader/program and material variant
uniform or instance-data compatibility
sampler and wrap state
blend/depth/stencil/clip state
primitive/index format
```

Flush when any field changes. Instrument the flush cause; “many draw calls” is not actionable until the
breaks are attributed.

Do not sort the entire stream by texture to increase batch size. Group content that is normally drawn
together into the same logical atlas so batching follows from order; never sacrifice painter order for one
atlas.

## Derive every page ceiling

Record capabilities from the active engine/backend and the chosen command format:

- maximum texture dimensions, layers/slots, and practical memory budget;
- index type and maximum addressable vertex index;
- vertices and indices emitted per sprite/primitive;
- per-command vertex/index byte capacity;
- uniform, instance, and descriptor/texture limits; and
- engine-side caps lower than the graphics API.

For a 16-bit index stream, the largest value is 65,535; that does not automatically mean 65,535 sprites.
Derive the primitive count from vertices per primitive, base-vertex behavior, reserved vertices, and the
engine's actual command path. Assert capacity before appending and start a new ordered page while the current
one is still valid.

```text
Good: can_append(next) -> append; otherwise flush/page rollover -> append.
Bad:  camera zoom floor chosen so the developer's window usually stays under the buffer.
```

Test exactly below, at, and above every ceiling, plus the largest supported viewport. Verify both command
counts and the pixels where pages meet. A safety threshold must be independent of aspect ratio and display
size.

## Invalidate dependency footprints

Define invalidation beside the rule that derives it. The gameplay/tile adapter must first emit the complete
semantic visual closure. For tile worlds, the tile rules own adjacency read offsets,
connectivity/autotile changes, footprints, and cross-chunk semantic closure. The renderer then adds only its
own dependencies. A changed emitted visual may affect:

- itself as supplied by the authoritative semantic closure;
- objects whose order relationship crosses it;
- shadows, glows, particles, and overlays extending beyond it;
- atlas/cache entries or aggregate summaries derived from it; and
- filtered output whose kernel samples outside the logical change.

Expand the supplied closure by those render-only dependencies, then intersect it with visible cached
chunks. Version cached inputs so a stale entry cannot masquerade as valid merely because its world rectangle
still matches.

Choose chunks in stable world coordinates. Define edge ownership and include any halo needed to compute
neighbors, but emit shared pixels/geometry from one owner. Otherwise independent rebuild order produces gaps,
double coverage, or discontinuous patterns at chunk/page seams.

Cache the least-derived reusable data that remains valid. When animation is driven by global time and does
not change geometry, cache per-chunk static draw data and keep the animation in dynamic shader inputs, rather
than caching finished images that every frame invalidates.

Dirty-region rendering is useful only when the actual backend or retained cache can reuse unchanged work.
Do not add dirty bookkeeping to a path that redraws the complete target regardless.

## Change representation at scale

Define LOD semantically, by what remains readable and necessary at a screen footprint:

- full animated sprite or detailed geometry nearby;
- simplified sprite, reduced animation, or merged decoration at mid scale;
- aggregate mark, baked chunk, density, or summary at overview scale.

Foundational coverage such as terrain must switch to another complete representation, never drop individual
pieces into holes. Optional clutter may disappear if that is an explicit category policy.

Use one detail policy shared by related layers. Add hysteresis or discrete zoom bands so tiny scale changes do
not thrash representation and pools. Preserve stable identity across the transition where selection or hover
must survive.

Keep LOD render-only unless gameplay explicitly defines different information. A different window size or GPU
may choose different presentation detail without changing simulation, commands, saves, or replay.

Enforce a hard independent capacity guard even when LOD is expected to activate first. Misconfiguration or a
new viewport must fail safely rather than overrun a command buffer.

Prove:

- every semantic category immediately above and below each transition;
- pan/zoom oscillation around thresholds;
- selection, overlays, and animation continuity through a transition;
- dirty edits at chunk borders in every active LOD;
- page rollover inside ordered translucent content; and
- missing, late, or rejected cached data falling back without changing authoritative state.
