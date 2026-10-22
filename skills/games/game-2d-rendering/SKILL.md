---
name: game-2d-rendering
description: Use when designing, implementing, reviewing, or debugging an engine-agnostic 2D renderer or render seam, including snapshot extraction, sprite placement and pivots, coordinate transforms, draw order, culling, pooling, batching, atlas or page limits, dirty chunks, LOD, pixel snapping and filtering, alpha, blending, shaders, or visual proof. It supplies contracts that keep pixels faithful to authoritative state and keep render work bounded without corrupting order. Do not use for asset creation, isometric projection math, tile simulation, engine APIs, profiling methodology, or camera feel alone.
---

# Engineer 2D rendering

Make the renderer a bounded, read-only projection of authoritative state. Preserve semantic order before
optimizing draw submission, and prove pixels through the shipped pipeline rather than a reconstruction.

## Establish the render contract

Record before changing code:

- authoritative state and the frame/tick boundary the renderer may observe;
- model, world, view, screen, framebuffer, and texel spaces, including units, axes, origins, scale, and
  the single owner of each transform;
- the placement anchor and visual bounds for every sprite family;
- semantic passes and the stable ordering key within each pass;
- pixel-art or smooth-sampling policy per asset family, plus alpha encoding and blend contract;
- target aspect ratios, display scales, zoom range, backends, and device capability floors; and
- maximum visible items, vertices, indices, atlas pages, draw commands, and dirty work admitted per
  frame, expressed as derived limits rather than folklore constants.

Treat unknown capacity or visual values as named assumptions with a proof case. Do not make a fixed zoom
floor, one developer window, or one atlas size the safety mechanism.

## Build one read-only presentation seam

Extract or borrow one coherent render snapshot through an explicit adapter. Include stable identity and
generation, semantic visible state, previous/current presentation transforms when interpolation is needed,
the logical placement anchor, visual/cull bounds, order fields, and resource/style identifiers. Keep engine
objects, mutable simulation storage, texture handles, and derived pixels out of the authoritative model.

The adapter owns meaning-to-visual mapping. A renderer should consume “shown surface,” “carried item,” or
“damaged appearance,” not rediscover those facts from convenient raw fields. When a visible state changes,
change the snapshot schema, adapter, and contract proof together.

Choose either a compact copied snapshot or a generation-owned immutable view whose lifetime spans render.
Never retain a pointer into storage that may move or mutate. Render-local interpolation, animation phase,
pool occupancy, culling, and LOD must not write back into authoritative state.

Read [render contracts](references/render-contracts.md) when defining snapshot lifetime, coordinate
conversions, pivots, visual bounds, or semantic order.

## Place and order by meaning

Place a sprite from an authored logical pivot such as feet, contact point, socket, or tile hotspot—not
from the bitmap center or trimmed rectangle. Keep the pivot stable across frames and variants. Compute
placement, culling, picking overlays, and dirty expansion from the same transform and metadata contract.

For ordinary 2D scenes whose occlusion is representable as one depth value, define draw order as a
stable semantic tuple, for example:

```text
(pass, depth-from-ground-anchor, local-sublayer, stable-id)
```

Use explicit passes for relationships such as ground, ground detail, shadows, entities, overhead, effects,
and UI. Split one visual into components when it must straddle another pass. Do not globally sort by atlas,
material, node creation order, or sprite center: those are submission details, not scene meaning.

When the projection's own rules establish pairwise occlusion dependencies for tall, multi-cell, or
stacked content, that partial order owns visibility. Consume its dependency-ordered stream or stable rank;
do not replace it with a scalar depth tuple. Batch only adjacent compatible commands after that order.

```text
Good: semantic order -> stable command stream -> batch adjacent compatible commands.
Bad:  group by texture -> recover painter order with ad hoc z offsets.
```

## Bound work without breaking the picture

Cull by conservative visual bounds before allocating or updating render representations. Expand the query
for sprite overhang, effects, and any projection displacement derived from the content contract. Track
visible, culled, live, emitted, and pooled counts so “viewport-bounded” is observable.

Batch only adjacent commands that are compatible in texture/page, shader and material state, uniforms,
sampler, blend, clip/stencil, target, and semantic order. Derive command capacity from the actual index
format and backend limits; assert before append and roll to another ordered page before overflow. A larger
batch is not a win if it changes overlap or crashes at an extreme viewport.

Consume the authoritative semantic/visual closure from the system that derives it. In a tile world,
adjacency, autotile, footprint, and cross-chunk invalidation belong to the tile rules, not the renderer.
The renderer expands that emitted closure only for projected sprite overhang, filter kernels, effects,
visibility caches, and render-cache chunk ownership. Rebuild only dirty visible chunks or commands. Define
one owner for shared chunk edges so a boundary cannot be emitted twice or omitted.

Use pooling only after churn is proven material. Reset every visible property and detach every external
reference on release; generation-check reused identities. Prefer compact value command buffers when pooled
scene objects create more lifecycle state than they remove.

Read [scaling and updates](references/scaling-and-updates.md) when work involves culling, pooling, batch
compatibility, page ceilings, dirty regions/chunks, cached draw data, or semantic LOD.

## Make sampling and compositing explicit

Choose nearest sampling, integer output scale, and final-transform snapping for intentionally crisp pixel
art. Choose linear/minification filtering and suitable mipmaps for continuously scaled art. Do not apply
one scene-wide sampler policy to both.

For atlases, generate padding/extrusion and mip-safe borders with the atlas metadata. Region-safe UVs,
filtering, wrap mode, mip generation, and compression are one package; a correct source PNG does not prove
the runtime sample.

Choose straight or premultiplied alpha end to end: importer, texture data, tint, shader output, intermediate
targets, and blend state must agree. Under premultiplied alpha, zero coverage must contribute zero RGB and
color transforms must preserve that invariant. Preserve translucent order; a texture sort cannot commute
ordinary alpha compositing.

Read [pixels, shaders, and proof](references/pixels-shaders-and-proof.md) before changing pixel snapping,
filters, atlas sampling, alpha, blending, shaders, render targets, or visual regression coverage.

## Prove the renderer in layers

1. **Headless contracts:** exercise production snapshot adapters and pure command/geometry emitters. Prove
   coordinate round trips, pivots, bounds, stable order, cull expansion, dirty propagation, LOD boundaries,
   page rollover, alpha reference values, and exhaustive adjacency/state matrices where finite.
2. **Renderer capture:** freeze seed, state, presentation time, viewport, display scale, and capabilities;
   render through the shipped shaders and submission path; retain actual, expected, and diff artifacts.
3. **Live target:** inspect the real window on required backends, aspect ratios, display scales, zoom
   extremes, movement, resize, fallback assets, and effect combinations. A build, process, offline
   composite, or headless invariant is not visual sign-off.
4. **Capacity guard:** drive the largest supported viewport and densest visible state through every page and
   LOD transition. Assert no page exceeds its index/vertex/resource ceiling and no foundational surface
   develops holes.

Use production code as the test surface. An offline compositor that independently repeats placement or
blend logic can reproduce the same mistake and return a false green. Keep debug overlays for anchors,
bounds, order keys, pages, chunks, and dirty regions; they turn a pixel symptom into a contract failure.

Report the observed symptom, violated contract, correction, headless proof, renderer/backend proof, capacity
evidence, and untested platforms or visual combinations. Read [the source map](references/sources.md) when
auditing or extending a rule.
