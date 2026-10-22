# Render contracts

Read this when defining snapshot lifetime, coordinate conversions, sprite pivots, visual bounds, or
semantic layer ordering.

## Extract a coherent render snapshot

Write the seam as data before choosing scene nodes or draw calls:

```text
RenderFrame
  simulation_tick / snapshot_generation
  previous_time, current_time, presentation_alpha
  viewport contract and active detail policy
  items[]

RenderItem
  stable_id + generation
  semantic kind and visible state
  previous/current transform or one committed transform
  logical anchor and conservative visual bounds
  semantic pass, depth anchor, local sublayer
  resource/style IDs, tint, opacity, effect flags
```

Include only fields the presentation needs. A convenient dump of the entire world expands coupling and
makes the renderer infer semantics the simulation already decided.

Choose one lifetime model:

- **Copied frame:** extract compact values into frame-owned storage. This is easy to reason about and safe
  to hand across threads, but extraction and copying must remain bounded.
- **Immutable generation:** borrow a view pinned to an immutable generation until submission completes.
  This avoids copying but requires explicit ownership and reclamation.

Do not combine a borrowed container with mutable element pointers. A container that remains allocated can
still move, replace, or recycle its elements. Stable ID plus generation prevents a pooled visual from
silently representing a newly reused entity slot.

If render preparation overlaps simulation, publish a complete generation in one operation. Never expose a
half-updated mixture of positions, styles, and visibility. Collecting a draw-ready view before the next
update does not mandate one thread model.

Keep renderer-only state renderer-only:

- interpolation and smoothing;
- animation playback phase and cross-fade;
- cached command ranges and GPU handles;
- culling, LOD, pooling, and debug visualization; and
- transient highlights that are not authoritative game facts.

Fixed-step snapshot timing and the interpolation clock belong to the gameplay runtime; this reference owns
only the data and lifetime contract presented to the renderer.

## Name every coordinate space

Maintain a small executable coordinate ledger:

| Space | Unit and origin | Axis direction | Owner | Conversion and rounding |
|---|---|---|---|---|
| Model/grid | Domain-specific | Declared by model | Simulation | Model projection |
| World/canvas | World unit or authored pixel | Declared | Projection adapter | Model ↔ world |
| View | Camera-relative | Declared | View transform | World ↔ view |
| Screen/input | Logical point/pixel | Platform convention | Viewport | View ↔ screen |
| Framebuffer | Physical pixel | Backend convention | Window/render target | Screen ↔ framebuffer |
| Texel/UV | Texel and normalized UV | Texture convention | Asset/atlas metadata | Region ↔ UV |

Implement each edge once and derive its inverse from the same parameters. The complete chain—not a partial
camera inverse—must drive render placement, screen-space culling, hit/pick overlays, and debug labels. A
screen coordinate passes through canvas, stretch, and window transforms; it is not merely a translated world
coordinate.

Prove:

- forward/inverse round trips at origins, edges, negative coordinates, and maximum supported magnitudes;
- physical frame edges at every supported aspect ratio and display scale;
- the same world point through drawing, culling, picking/highlight, and input conversion; and
- conversions before first presentation and during resize, when viewport metrics may be incomplete.

Do not round inside each transform. Preserve precision through the chain and apply an intentional sampling
rule at the final presentation boundary. Independent rounding in world, camera, and framebuffer spaces turns
one continuous motion into conflicting one-pixel decisions.

## Place from a logical pivot

Define the point that touches the world:

- feet or ground contact for an actor;
- base or foundation socket for a prop;
- tile hotspot for a terrain sprite;
- hand/socket for an attachment; or
- explicit center for a truly centered effect.

Store this pivot in asset/manifest metadata. Trimming transparent bounds, swapping animation frames, changing
resolution variants, or repacking an atlas must not move it. The pivot controls both placement and the
rotation origin.

```text
Good: world contact + authored pivot -> frame rectangle is an implementation detail.
Bad:  world position - current bitmap width/2 -> every trim or frame size shifts the actor.
```

Keep separate rectangles when their purposes differ:

- logical footprint for simulation or interaction;
- tight opaque or mesh bounds for overdraw decisions;
- conservative visual bounds for culling and dirty expansion; and
- effect/shadow bounds when they extend beyond the sprite.

A tall sprite can be logically off-screen while its visible canopy remains on-screen. Cull and invalidate by
the conservative visual bound or by a world query expanded with the maximum overhang derived from metadata.

## Order by semantic relationships

Write the layer roster from the intended picture, not from the scene tree. A typical structure is:

```text
background -> terrain -> terrain detail -> ground shadows
-> entities and structures -> overhead/roof -> particles/effects -> world UI -> screen UI
```

Within a simply occluding pass, sort from the shared ground/contact anchor: coarse semantic bands plus a
contact-depth key, not one universal Y-sort for the entire scene.

Use a total stable key:

```text
(pass, depth, local_sublayer, stable_id, component_index)
```

The stable suffix prevents equal-depth items from flickering when container iteration, threads, or pool reuse
changes. It need not encode gameplay priority; it only makes an otherwise equal visual decision repeatable.

This total key applies only when one scalar depth represents the scene's occlusion. Complex isometric scenes
can define a partial order from overlapping world footprints and stacked surfaces. When the projection's
rules supply that order, preserve it and use the tuple only as a stable tie within otherwise
unconstrained groups. Never collapse an isometric dependency graph into `depth` for batching convenience.

When one object must appear both below and above its peers, emit separate components into separate passes.
Do not alternate magic z offsets until one frame looks right.

Separate opaque/cutout and genuinely translucent policies where the renderer supports them. Ordinary alpha
blending depends on destination contents, so translucent overlap needs a deliberate painter order. Batch
formation happens after semantic ordering and may merge only consecutive compatible commands.

Prove ordering with adversarial overlaps:

- equal anchors and stable-ID reversal;
- tall vs short sprites sharing the same feet;
- an entity crossing a prop's contact line;
- multi-component visuals that straddle a pass;
- translucent effects crossing page or material boundaries; and
- pool release/reacquire in a different iteration order.
