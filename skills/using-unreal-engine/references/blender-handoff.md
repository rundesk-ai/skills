# Taking a mesh from Blender into Unreal

Read this when importing authored geometry, when a mesh arrives mirrored, inside out, at the wrong
scale or facing the wrong way, or when choosing export flags for a kit.

Authoring and exporting the mesh — applied transforms, smoothing, UVs, slot names — is Blender-side
work with its own rules. This page owns what Unreal does with the file.

## The three coordinate systems

| System | Handedness | Up | Forward | Unit |
|---|---|---|---|---|
| Blender | right-handed | +Z | −Y | scene-defined; meters by default |
| glTF 2.0 | right-handed | +Y | +Z | meters |
| Unreal | **left-handed** | +Z | +X | centimeters |

Blender to glTF is a **rotation**: −90° about X takes Blender's +Z up to glTF's +Y up. Both frames stay
right-handed, so nothing about winding changes. Blender's own exporter does this; a script that
serializes glTF by hand must supply it, unless it authors in glTF's frame to begin with.

## A handedness mirror already flips the winding

A reader that converts glTF to Unreal typically does this:

```text
(x, y, z) -> (x, z, y), scaled by 100
```

Two things happen at once. The ×100 converts meters to centimeters — nothing subtle. **Exchanging two
axes negates the transform's determinant**, and that single mirror is exactly the right-handed to
left-handed conversion: glTF's +Y up becomes Unreal's +Z up, glTF's +Z forward becomes Unreal's +Y, and
+X does not move.

A mirror reverses the apparent orientation of every triangle. glTF declares counter-clockwise front
faces; after one mirror they are clockwise, which is Unreal's front-face sense. **So the index order
must be preserved.**

**Reverse the indices as well and you double-correct into inside-out front faces.** The surface renders
black or invisible while its normals still look correct, because a two-sided material multiplies the
world normal by the two-sided sign and flips the lighting on what is now a back face.

The opposite case proves the rule: a generator that builds faces directly in Unreal space performs no
mirror, so it **must** reverse the triangle indices at the mesh-description boundary. Same engine,
opposite correction. What decides it is whether a mirror happened upstream, not a house style.

## The FBX path

FBX carries its own axis metadata, so the export flags and the import settings have to agree. Fix
them once per project and assert the result:

- Match the import axis and unit settings to the export's declared forward axis, up axis and unit
  scale; correct a mismatch at export, not with an import-side fix-up.
- Import authored normals without recomputing them, and let the engine compute tangents from the UVs.
- Whether the front axis is forced is a per-family decision, not a default: a piece placed by a
  computed transform and a piece whose forward direction drives gameplay want different answers.
  Declare which, and assert it.

## Calibrate before authoring a kit

Do not reason out the flag set. Export one **asymmetric piece of known dimensions** with a
distinguishable front and left, import it, measure it in the engine, then pin those flags and add a
bounds assertion. Getting this wrong is otherwise discovered only after a whole kit exists, and every
piece has to be re-exported.

## Two import failures that look like success

- **A stale asset at the destination path** makes a failed import appear to have worked. Assert that
  the import task returned an object.
- **Asset compilation is asynchronous.** Finish compilation both before and after assigning materials,
  or the assignment lands on an asset that is about to be replaced.

## Verify in the engine, not in Blender

An attractive Blender render proves nothing about the engine's material response. The gate that
matters is an automation test on the imported asset: dimensions, pivot, section count, material slot
names in order, triangle count and per-triangle non-degeneracy. **Only that test proves the exporter
and the importer pair did what you believe.**

Importers commonly match material slots **by name**, so a slot silently renamed on the Blender side —
a datablock collision appending `.001` is the usual cause — becomes a section with a null material.
