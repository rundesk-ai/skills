# Modular kits: parts, pivots, mating, manifests, variants

A kit is a set of pieces that must fit each other and fit an assembler written against them. Every
rule here exists because one of those two fits can break without anything reporting an error.

Read this once the whole-model proportions work and you are deciding what deserves independent
authoring. `modeling-workflow.md` owns the stages before that point.

The part tests, and the split between design parts, authoring objects and delivered meshes, are in
`SKILL.md`.

## The workflow for a complex asset

1. **Establish the whole-model blockout.** Compare proportions and silhouette before fine modeling.
2. **Write the part table as data before authoring parts.** Role, expected count, mating origin,
   shared variants and stages, surface assignments. Revise it deliberately as the design develops.
3. **Refine a representative assembly.** Develop one part in its context, inspect both, and change
   either when the fit or the proportions fail. Do not finish every isolated part before seeing them
   together.
4. **Expand accepted patterns.** Reuse the source part and keep placement logic separate from its
   geometry. An assembly-specific transition is explicit authored work, not a hidden one-off.
5. **Review surfaces and the family together**, before multiplying production.
6. **Assert the part census before any export consolidation**, and record which source parts become
   which delivered mesh.

Stages and variants declare the combinations the family actually supports rather than taking every
cross product.

## The part census, asserted where the scene is

Give every object a `role` property. Before export, gather objects by role and assert the count the
form requires — a cart has two wheels, a wagon four, a sled none, and exactly one hitch — then assert
each part's origin at its **declared mating point** rather than auto-centered on its visible bounds,
and that no object is missing from the table.

**This is provable only with the scene in memory.** A part count recorded in a manifest beside the
exported file is a claim the exporter made about itself. The census proves an authoring contract, not
quality and not a runtime object count.

## The parts catalog: look before you author

The search-parameterize-register steps are in `SKILL.md`. Per part the catalog records: role, id, the source that authors it, dimensions, local mating origin,
material slot, the assets that consume it, a geometry digest, and one render at a fixed scale.

**Generate it from the part tables in the sources; never maintain it by hand.** That is why the
workflow above puts each part table in the source as data. A hand-edited catalog drifts within a week and then costs
more than it saves.

Where no catalog exists yet, say so and register parts in the kit's own manifest. **The first kit with
parts meant for reuse builds the catalog with itself.** Do not invent a private index format — an
undocumented contract is worse than an absent one.

## Pivot policy is declared per family and asserted

There is no single right pivot; there is a rule that each family declares one and a check enforces it.

- A piece placed by a computed transform between two endpoints wants a **centered** pivot.
- A piece dropped onto a grid wants a **corner** pivot, so it snaps.
- A piece that stands on ground wants its **base envelope** on the placement origin, and sunk far
  enough that it does not float on the steepest slope it is allowed on.

**Pick from the consumer, and write down which one you picked.** The failure this prevents: a pivot
nobody asserted drifts a few millimeters on a re-export, every instance in the world moves with it,
and it reads as a placement bug that gets debugged in the wrong module for a day.

Assert the **consequence** where you can, not only the declared number — that no base floats above
sloped ground is a sharper check than that a number matches the one you wrote down.

## The manifest is the mating contract

A manifest records, per piece: name, file, dimensions, pivot, axis, triangle count, material slot
count, degenerate count and a geometry digest, plus the digest of the source that produced them. It is
not documentation. **Those numbers are load-bearing in the assembler's code.**

Where an assembler scales a piece to fit a span, the authored length appears as a divisor. Re-author a
600-unit beam at 610 and every beam is scaled wrong by 1.7%: the structure still assembles, still
renders, and nothing fails. Three conventions are locked together there — the pivot is centered, the
long axis is fixed, and the assembler scales one axis — and breaking one silently breaks the others.

Two checking strategies, both correct, for different things:

- **Hardcode the numbers the consumer depends on**, in the consumer's own test. Changing them then
  requires editing the test, which is the review moment you want. This catches **authoring drift**.
- **Read the manifest for values that legitimately differ per asset**, and assert the imported mesh
  against the recorded value. This catches **export and import corruption**.

A kit needs the first kind for its mating dimensions. Reading a mating dimension from the manifest the
source just wrote proves only that the source agrees with itself.

**Never hand-edit a manifest.** It is generated output, and the source digest inside it exists so that
a hand edit or a stale regeneration is caught offline.

## Exact arithmetic at mating vertices

Mating faces must be *equal*, not nearly equal. Two mechanisms punish "nearly":

- **Hairline light leaks.** A gap of a few thousandths of a unit is still a gap. At a grazing angle the
  background shows through as a bright thread along the seam, and it moves with the camera, so it
  reads as flicker rather than as a modeling error.
- **Z-fighting.** Two faces meant to be coplanar but differing in the last float bits alternate which
  one wins the depth test, per pixel and per frame.

Both come from accumulating a position by repeated addition (`pos += step`) instead of computing it:
every added step carries its rounding error forward, so the far end of a long run is off by the sum.

- **Author on whole units.** Integer dimensions make every half-extent an integer or an exact half,
  and both are exactly representable in binary floating point.
- **Parameterize, do not accumulate.** Compute item *n* from *n* — `lerp(a, b, i / count)` — so it does
  not depend on item *n−1*. Let one piece absorb the remainder by scaling, rather than leaving a slack
  gap.
- **Snap mating vertices to the exact declared coordinate before export.** A bevel, a boolean or a
  decimate can move a vertex by a fraction of a unit, and the piece still passes a bounds check while
  its mating face no longer matches its neighbor.

## Variants are an axis of the kit, not a late addition

Treat variation as part of the delivery shape from the start: species by stage by condition, or
material by damage state. Then:

- **Enumerate the combinations the family supports**, rather than assuming every cross product exists.
- **Name every variant by rule**, so an id can be computed rather than looked up, and the consumer can
  bind to it without a table of exceptions.
- **Check completeness as a cross product**: walk every declared combination and assert its asset
  exists. A missing variant otherwise appears at runtime as a silently absent object.
- **Decide the consolidation shape before the meshes exist.** Whether each variant is its own mesh, or
  one mesh with swappable sections, changes what is exported. Deciding after the fact means
  re-exporting all of them.
