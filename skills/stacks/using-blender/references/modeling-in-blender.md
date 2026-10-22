# Building a model in Blender

Read this before authoring geometry, whether by hand or from a script. It is the tool's own craft: what
to build with, in what order, and the failures that are invisible until an exporter or a consumer meets
them.

What the model should look like, and which pieces deserve independent authoring, is a design decision
made before any of this.

## Work at real scale

**One Blender unit is one meter.** Model the thing at the size it is. A door authored 1.9 units tall is
a door; the same door at 19 units is a door that breaks physics, instancing, texel density and every
comparison against the family anchor.

Scene unit settings, and the startup scene they come from, are per-machine state — which is why a
scripted run starts from factory settings and declares its own.

## Block out, then refine

1. **Primitives at correct dimensions.** A cube scaled to the real bounding box of each mass, placed
   where the mass goes. This is the whole model at the stage where changing it is free.
2. **Fix proportion and silhouette here**, against the reference, before any detail exists.
3. **Add structure with modifiers**, not with hand-placed vertices, for as long as you can.
4. **Apply and hand-edit only what the stack cannot express.**

From a script the same order holds: build the masses from parameters, add modifiers through
`obj.modifiers.new(...)`, and hand-place a vertex only where a shape has no parametric description.

## The modifier stack is the model, until you apply it

The stack evaluates **top to bottom**, and the order is not cosmetic:

| Order | Why |
|---|---|
| **Mirror before Subdivision** | Subdividing first rounds the seam before the halves are joined, and leaves a crease down the middle |
| **Mirror before Array** | Mirror the unit, then repeat it; arraying first mirrors the whole run and doubles it |
| **Array before Curve** | The curve deforms what exists; an array added after follows the straight axis, not the curve |
| **Bevel before Subdivision, carefully** | A bevel then subdivided softens twice. Either bevel with enough segments and no subdivision, or hold the edges with creases and let subdivision do the work |
| **Solidify before Bevel** | Bevel the finished shell, not the surface it was made from |
| **Triangulate last, when at all** | Anything after it works on triangles and cannot see the quads you authored |

**Apply scale before Bevel, Solidify or Array.** This is the most common Blender error there is. Those
modifiers work in the object's local space, and the object's scale is applied afterward — so on an
object scaled non-uniformly, a bevel of 2 cm comes out 2 cm on one axis and 6 cm on another, and a
solidify of 1 cm is three different thicknesses. The geometry looks deliberate and is not.

## The traps

| Trap | What you see | The fix |
|---|---|---|
| **Unapplied scale** | Uneven bevels, wrong solidify thickness, a distorted or wrongly sized export | Apply scale before those modifiers and before export. From a script, transform the mesh data and reset the object matrix to identity |
| **Non-manifold geometry** — interior faces, doubled vertices, an edge shared by three faces | Booleans produce nonsense, solidify explodes, the exporter writes geometry the consumer rejects | Merge by distance, delete interior faces, and recalculate normals outward. Select non-manifold before believing a mesh is clean |
| **Flipped normals** | Faces invisible or black in the consumer, correct in Blender's default shading | Recalculate outside, and check with face orientation on rather than by eye |
| **Boolean output** | Ngons, poles and near-coplanar faces that z-fight and shade badly | Use the exact solver, keep the cutter as its own object, and clean up before subdividing. A boolean is a starting point, not a result |
| **An ngon that is not planar** | Shades as a fan and triangulates unpredictably at export, differently in each consumer | Keep ngons flat, or triangulate deliberately so you choose the diagonal |
| **Subdivision left on a game mesh** | Triangle count nobody budgeted, and a different count in each consumer | Apply and decimate to a target, or do not subdivide. A game mesh wants explicit topology |
| **The origin left where it landed** | Every instance placed wrong, and rotation about the wrong point | Set the origin to the declared mating point — never auto-centered on visible bounds, which move every time the part is revised |
| **Mirror without clipping and merge** | A seam that splits open under deformation or shows a hairline at grazing angles | Clip at the axis and merge the seam vertices, with the seam vertices at exactly zero |
| **A linked duplicate treated as a copy** | Editing one edits every other, or the opposite: two parts that should have stayed one drift apart | Know which you made. Linked duplicates share one mesh datablock, and that is the tool's own version of authoring a part once |
| **Everything shaded smooth** | Hard surfaces look soft and rounded; edges that should read as edges do not | Mark the sharp edges and let the rest smooth, rather than smoothing the whole object |
| **Texel density set per part** | One part is blurry beside another in the same kit | Fix a density for the family and divide by it, rather than unwrapping each part to fill its own space |

## Topology, only as much as the consumer needs

- **Quads where it deforms or subdivides.** A deforming joint needs even edge flow across the bend;
  triangles there pinch under deformation.
- **Triangles are fine on static hard surface.** Chasing all-quads on a prop that never bends spends
  effort on nothing — every consumer triangulates on import anyway.
- **Poles pinch.** A vertex with three or five-plus edges distorts under subdivision. Put them on flat
  areas where the distortion has nothing to catch the light.
- **Density follows the camera.** Geometry smaller than a few pixels at the target distance is cost with
  no return; put that detail in the surface treatment instead.

## Before it leaves Blender

- Apply the transforms, or know exactly which the exporter will apply for you.
- Apply or bake the modifier stack, or export with modifier evaluation on — and be able to say which.
- Confirm the origin, the dimensions and the axis against what you declared, by reading them back from
  the object rather than from the viewport header.
- Check the UV layer exists on every loop, and that no UV triangle has zero area.
- Check the material slots are the ones the consumer expects, in the order it expects them.
