# Normals, UVs, slots and color

Read this before authoring smoothing, unwrapping, assigning material slots or writing vertex data —
and when a mesh imports black, with an empty slot, or with a tint nobody asked for.

## The normals migration

Blender 4.1 removed `use_auto_smooth`, the auto-smooth angle and `calc_normals_split()`. A script
copied from an older tutorial raises `AttributeError`, which reads as your mistake.

Smoothing is now:

- the `sharp_face` and `sharp_edge` boolean attributes, or
- true custom split normals, set with `normals_split_custom_set_from_vertices()`.

Do not rely on a bundled smooth-by-angle node group resolving in a background run. **Author normals
explicitly** and let the consumer recompute tangents from the UVs rather than recomputing normals.

## FBX must carry smoothing

Export FBX with the face smoothing type set explicitly. Without it, some importers fall back to
opening a dialog — which in a headless run means a hang or a killed job, not an error message.

## Procedural geometry has no UVs, and nothing will tell you

A mesh built from `from_pydata` or bmesh has no UV layer until you make one. Downstream, a missing or
degenerate layer produces **NaN tangents and black shading**, and the importer will not warn.

- **Unwrap solvers are operators.** They need context, and they are not deterministic — the same mesh
  can unwrap differently between runs.
- **Project instead.** Take the UV axis pair from the dominant component of the face normal, project,
  and divide by a fixed texel density in the part's own space. The same mesh then always produces the
  same layout, and density is comparable across a family.
- **Authored end-face UVs collapse.** A face whose projection axis pair is degenerate for its normal
  yields a zero-area triangle. Pick the axis pair per face, not per object.
- **Rebuild UVs after decimating**, per loop triangle. A decimate moves vertices without maintaining
  the layout, and the seams smear across the atlas.
- **Assert it**: a UV layer on every loop, and no UV triangle with zero area.

## Material slot order is the section index

Importers commonly build the section list in slot order and then match the slots **by name**. Where a
name does not match, a typical importer produces a section with a **null material and logs nothing** —
the mesh renders with the engine default and looks like a material bug.

Two things break the names silently:

- **Renaming a material** in the script without updating the consumer's expectation.
- **A datablock collision.** Creating a material inside a loop gives `Leaves`, `Leaves.001`,
  `Leaves.002`, because `bpy.data.materials.new()` never fails on a duplicate name.

Fix the slot order and names per family, and assert three things in the consumer's gate: the slot
**count**, the slot **names in order**, and the **assigned material**. Count alone passes while the
order is wrong.

## Color space, and what a texture channel means

Keep the channel roles explicit and do not infer them from a picture:

- broad color to the albedo map;
- relief to the normal or height representation;
- reflectance variation to roughness;
- deliberate wear to masks or decals.

A plausible color image is evidence for the color channel and for nothing else.

Where a consumer converts linear vertex colors to sRGB bytes on import, **vertex colors used as data
are not tints**: blend weights, masks or indices written to a color layer come back through a gamma
curve and are no longer the numbers you wrote. Use a dedicated attribute layer for data, or
pre-compensate deliberately and record that you did.

## An alpha mask is a separate file

A diffuse format without an alpha channel — JPEG, most notably — cannot carry a cut-out mask. Ship the
mask as a separate image, reference it from the material, and **assert the reference resolves before
export**. A cut-out material with no mask renders a leaf card as an opaque rectangle, and the failure
appears only once the asset is in the scene.

## Instancing shares one material set

Instanced meshes share a single material set, so per-instance variation has to be baked into vertex
colors or per-instance custom data. **Reserve that channel in the kit convention before authoring**,
not after: adding it later means re-exporting every piece.
