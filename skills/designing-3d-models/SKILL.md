---
name: designing-3d-models
description: Use when planning, designing, reviewing or revising 3D models and the reusable parts they are built from, including deciding what a model should look like, gathering and judging references, choosing which pieces deserve independent authoring, keeping a shared part such as a window or a wheel consistent across assets, and judging the result against its references. It supplies the build order from the whole model to its parts, the tests that decide what becomes a part, the mating and variant contracts a kit needs, and the review that separates form defects from surface defects. Do not use it for the mechanics of one modeling tool, engine import settings, 2D art, or texture painting as a task of its own.
---

# Design a model and the parts it is built from

**Establish the whole, decide the parts, refine one representative, then multiply.** A model is
accepted against its references at the camera it will be seen from — never against a close render
that flatters it, and never because a script ran without error.

Two failures cost the most, and both are decided before any geometry exists. **Authoring a second
window because nobody looked for the first** leaves two that drift apart. **Polishing parts before
the assembled proportions work** spends the effort where it cannot be seen.

## State the target before modeling

Record, and keep current as the work moves: the intended use and the camera it is seen from; the
named references and what each one establishes; the scale anchor; proportion goals; material
families; edge treatment; detail limits; and the explicit refusals.

**A reference without evidence for a feature is a gap, not permission to invent one.** Where the
references do not settle a detail, say so and ask, rather than inventing a historical or anatomical
fact that then has to be unpicked from every asset in the family.

Keep this record where the work resumes from, not in a chat log, and update it at every meaningful
iteration so a later session does not re-litigate settled decisions. Read
[the modeling workflow](references/modeling-workflow.md) for its fields and for resuming after a
break.

## Gather references, and judge them

Work from images of the real thing and from assets whose look is already accepted. Name each one and
what it establishes — silhouette, proportion, material, wear, construction — because a reference
folder nobody can account for becomes a mood board and stops constraining anything.

**Generated imagery is a source candidate, never production geometry.** Generation supplies appearance
direction; an editable, deterministic source owns the shape that ships. Judge a generated reference
against the real thing before letting it direct a shape. Read
[references and generated imagery](references/reference-imagery.md) before gathering references or
using an image model: it holds the refusal list, the consistency rules and the raster checks.

## Work from the whole toward the parts, and back

| Stage | Produce | Review before going further |
|---|---|---|
| Whole-model blockout | Cheap assembled masses, and alternatives where proportions are unresolved | Silhouette, physical scale and proportion beside an existing family anchor, at the target camera |
| Part plan | The useful parts, their local origins and mating dimensions — existing parts found before new ones | The decomposition serves the whole; invisible fasteners are not parts |
| Representative assembly | One part in its context: a window in its wall, a wheel on its axle | Fit, transitions, overlap and relative scale. Revise the part and the assembly together |
| Form and surfaces | Refined forms, intentional edges and normals, UVs, first materials | Clay and material views separately, so a form defect is not mistaken for a surface one |
| Family review | The variants together with the accepted anchor, at one physical scale | Shared visual language, deliberate variation, and no small asset enlarged to hide a scale mismatch |
| Delivery | Reproducible source, exported asset, evidence in the consumer | The approved look survived delivery |

At each iteration: render, name the largest visible defect, change **one** coherent cause, and render
the same view again. Fix mass and proportion before adding surface noise. Keep the camera, light and
framing fixed across a comparison — another angle is a separate, labeled case. If repeated edits do
not move the named defect, record what failed and revisit the premise instead of adding detail.

Develop one representative to the agreed standard before multiplying production. A passing part census
is not a look, and an agent finding no defect is not acceptance.

## Decide what becomes a part

Once the proportions work, decide what deserves independent authoring. Too little decomposition makes
reuse and revision hard; too much spends care on pieces nobody sees. **Consider a part when it passes
one of these:**

| Test | Why it earns a part |
|---|---|
| **It repeats** — here, or in an asset that comes later | Authoring once and placing it N times spends one part's care instead of dividing it N ways, and makes all N consistent by construction |
| **It varies independently** of its neighbors across variants or stages | The variation gets an explicit parameter, and the family declares which combinations it supports |
| **It has a mating contract** — something places it, or it butts against a piece authored elsewhere | A mating dimension needs something to belong to |
| **It moves independently** | It keeps the pivot its motion needs |
| **It reads as its own shape at the target camera** | It deserves explicit attention |

**Stop when another subdivision buys no visible control, no reuse and no consumer requirement.** A
rock stays one object. A material boundary does not require an object boundary. Continuity in an
organic form outweighs tidy decomposition.

Keep three ideas apart: **design parts** you reason about, **authoring objects** you edit, and
**delivered meshes** the consumer receives. A muzzle can be a design part inside one continuous
animal mesh; a house can keep separate window sources and still deliver one consolidated mesh.

## Look before you author

Decomposition buys reuse only if a part can be found. Two houses built a month apart produce two
different windows unless something makes the second author look for the first.

1. **Search by role before authoring.** A part that passes the tests for your asset is the part you
   use.
2. **If it nearly fits, parameterize it — do not fork it.** A fork is two parts to correct the day the
   look changes, and they drift apart because nothing compares them.
3. **If it genuinely differs, author it and record why it is not the existing one.** That reason is
   the valuable half: it stops the next author re-deciding it.
4. **Register every part, including one-offs**, with its role, dimensions, mating origin, the source
   that authors it, and the assets that consume it. A part not worth reusing is worth recording as
   such.

Read [modular kits](references/modular-kits.md) once the proportions work and you are writing the
part table: it holds the parts catalog, pivot policy, manifest, mating arithmetic and variants.

## Prove it

1. The whole-model comparison against the named references, at the target camera.
2. The representative part shown in its assembly, and the family lineup at one physical scale.
3. Every part in the declared table present, with its origin at its **declared mating point** rather
   than auto-centered on its visible bounds, and the declared count per role.
4. The reproducible source committed, and the render paths and exact invocation recorded.
5. The owner's actual verdict on appearance, or "not yet given". A passing check is not a look.

## References

- Read [the modeling workflow](references/modeling-workflow.md) when starting or resuming a model,
  choosing the route for a rigid, organic, vegetation or continuous form, or handing off surfaces.
- Read [modular kits](references/modular-kits.md) when deciding parts, pivots, manifests, mating
  dimensions or variants.
- Read [references and generated imagery](references/reference-imagery.md) before gathering
  references or using an image model.
- Read [sources](references/sources.md) when auditing what a rule rests on.
