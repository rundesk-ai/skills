# Runtime art contract

Read this when defining a sprite family, modular environment kit, animation sheet, generated-art
handoff, or atlas export.

## Brief one family before drawing volume

Record the contract in a small asset-family specification:

| Field | Decision |
|---|---|
| Player meaning | What the asset and each state must communicate |
| View and scale | Camera/view, native on-screen size, allowed zoom, target displays |
| Style | Pixel grid or filtered raster, perspective, palette roles, outlines, light direction |
| Placement | Logical base/pivot, visible bounds, footprint, layer and occlusion role |
| Interaction | Selection/collision shapes, sockets, state vocabulary |
| Animation | Semantic clips, frame order/durations, loop policy, base motion |
| Variants | Structural differences, cosmetic differences, allowed transforms |
| Identity and lineage | Stable semantic ID, accepted master, source and rights record |
| Generation | Tool or model version, seed, parameters, and ordered references when reproducible inputs exist |
| Export | Stable ID, format, alpha mode, trim, rotation, padding, scales, atlas grouping |
| Proof | Representative scenes, target devices, automated validation, reviewer |

The brief is an interface between art, design, simulation, and rendering. If a field is unknown,
prototype it before scaling production.

Treat the accepted master as the frozen editable or raster source approved for derivation. Keep it
even when generation inputs are recorded: a later tool, model, dependency, or hosted-service version
may not reproduce the same pixels from a seed. A manifest should make the accepted source and every
derived runtime product traceable without turning the prompt or current atlas location into identity.

## Choose a raster contract deliberately

### Pixel art

Choose a reference pixel density and integer presentation strategy. Keep the source on that grid;
validate with the actual nearest-neighbor sampler and target camera. Do not mix independently chosen
pixel densities in one scene unless the style intentionally calls for it.

### Filtered raster or painted sprites

Author enough source resolution for the maximum intended display and derive platform sizes through a
repeatable export. Validate downsampling, edge colors, alpha, compression, mipmaps, and minification
in the runtime. Nearest filtering is not a universal “2D” default; it visibly blocks antialiased
edges.

### Vector-derived raster

Keep vector source editable, but freeze the rasterization settings for production: artboard bounds,
scale factors, stroke alignment, color profile, antialiasing, and naming. Inspect the raster result at
every target size; vector source does not guarantee legible small icons or consistent pixel edges.

## Store placement independently of packed rectangles

For every gameplay-visible region, retain:

- a stable semantic ID that does not depend on atlas page or coordinates;
- original untrimmed size and the trim offset;
- the base/pivot in original-image or declared local coordinates;
- optional sockets/hot spots and named interaction shapes;
- semantic layer/occlusion role;
- animation clip, frame index, duration, and intended loop behavior where applicable.

The art import step also derives a conservative clip-level visual bound as the union of every frame's
untrimmed authored pixels after applying its pivot and authored visual offset. Store that union with the clip
metadata and recompute it whenever frames, pivots, offsets, or import settings change. The renderer consumes
the union, then expands it for runtime shadows, particles, filters, and other effects it owns. It must not
rescan current frames or guess a global authored overhang.

An atlas packer may rotate or trim pixels only if the loader consumes the corresponding metadata.
Repacking should change page and UV data without changing semantic IDs or placement.

## Build modular kits from a coverage matrix

List required adjacency and gameplay conditions before making variants. A useful matrix may include:

- isolated, straight, corner, T, cross, cap, and transition cases;
- foreground/background or lower/upper layer roles;
- flat, slope, ledge, stair, wall-base, and wall-top cases where the world supports elevation;
- intact, damaged, active, inactive, highlighted, and disabled states;
- allowed rotations/reflections and asymmetric exceptions;
- common repeated clusters used to expose visible tiling.

Keep decoration separate from connectivity where possible. A structural tile set with controlled
overlay variants scales better than duplicating every connectivity case for every weed, crack, and
decal combination.

## Validate animation sheets as data

Frame count is not a quality metric. Evaluate whether key poses communicate anticipation, action,
impact, recovery, locomotion phase, or state change at gameplay size. Preserve timing per frame when
the authoring tool supports it; uniform timing can erase a deliberately held pose.

Run an overlay or onion-skin check for the base/pivot and any gameplay socket across the clip. If the
sprite intentionally translates, declare whether the motion is authored visual offset, animation
root motion, or simulation movement; do not let more than one layer own it.

## Pack without losing meaning

Atlas settings are a rendering contract, not an artist-only optimization:

- Padding and edge bleed must match filtering and mip behavior.
- Rotation requires loader and shader support and may be inappropriate for direction-sensitive data.
- Trimming requires original bounds and offsets; otherwise pivots and nine-slices move.
- Flattened paths require globally unique names; preserving semantic namespaces is safer.
- Premultiplied versus straight alpha must match the blend pipeline.
- Multiple resolution exports need deterministic suffixes or manifests and equivalent metadata.

Validate both loose-source and packed-runtime views during pipeline development. Ship and approve the
packed path.

## Review generated or outsourced art

Use the same acceptance contract regardless of source. Require editable or agreed source material,
stable naming, provenance records, export settings, and a technical validation result. For generated
families, compare a contact sheet for perspective, light, palette, proportions, edge treatment, and
near duplicates before integrating individual images.

Report validation failures without silently rewriting source art. Automatic repair can hide the
reason an asset changed and make the next export reintroduce the defect.
