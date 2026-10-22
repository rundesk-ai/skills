# References, and generated imagery among them

Read this before gathering references for a model, and before using an image model to make one.

A reference is what the model is judged against. A folder of images nobody can account for is a mood
board: it constrains nothing, and every disagreement about the result becomes a matter of taste.

## Account for every reference

Name each reference and what it establishes — silhouette, proportion, construction, material, wear,
scale. One image rarely establishes more than two of those, and an image used for a feature it does
not show is how invented detail enters a family.

- **Separate approved direction from experiments.** An owner approved a look at a scope and a date;
  record both. A modified candidate does not inherit the approval its baseline had.
- **Prefer the thing over a picture of a picture.** A photograph of the real object, a measured
  drawing, or an asset whose look is already accepted beats an artist's impression of any of them.

## Generated imagery is a source candidate

An image model supplies **appearance direction**. An editable, deterministic source owns the geometry
that ships. The two are not interchangeable, and the distinction is what keeps a kit rebuildable.

It earns its place where you need one more angle on a part you are about to author, a proportion study
you have no photograph for, or a quick comparison between two directions before committing. It does
not earn a place in the delivered asset.

The chain, when a generated image is used at all:

1. Declare the use and the contracts it must satisfy — scale, anchors, seams, sockets, layers.
2. Generate against labeled references, constrained rather than open-ended.
3. Retain the candidate, with the prompt, the references and the settings beside it.
4. Carve, rebuild or normalize it into the editable source. Never trace an unvalidated image into
   final geometry.
5. Declare explicit scale, anchors, masks and channel roles.
6. Export, check mechanically, then review at actual game scale in an assembled view.

## Refuse on sight

These never survive into an asset, whatever else the image gets right:

- warped or impossible geometry;
- invented text and signage;
- perspective baked into what should be a flat or orthographic reference;
- arbitrary lighting that contradicts the scene it will be used in;
- uncontrolled grain and model artifacts;
- architectural or object scale that contradicts the scale anchor.

Some of these a check can catch; several need a person to look. Treat the list as an automatic
refusal, not as evidence that a detector exists for each one.

## A reused seed is not a consistency system

Holding a family together takes more than one setting. Fix the camera, the palette structure, the
prompt, the reference set and the cleanup pass together. For a variant, hold proportions, silhouette,
registration and pose fixed, and change only the requested feature.

Even then, what you have is a template-controlled comparison, not a guarantee that two assets share an
identity. The assembled family view at one physical scale is what settles that.

## Validate a raster before it directs anything

Where a generated image is taken further than a sketch, declare and check its contracts: dimensions,
alpha, palette, registration and repeat behavior. A mechanical check rejects the clear failures
cheaply; readability, rights and whether the thing looks right still need a reviewer.

**Whether the image can be decomposed decides how far it can go.** A full-bleed backdrop can stay one
image, because nothing downstream needs components out of it. Anything that must yield stable,
registered parts has to survive being taken apart — and a beautiful flattened view routinely fails
that.

**Rights are a separate gate from appearance.** Neither visual acceptance nor a tool's own label
settles whether an image may be used. Record the provenance of every reference you keep, including the
ones you reject, with the reason.
