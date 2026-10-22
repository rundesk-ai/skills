---
name: using-blender
description: Use when building or driving Blender — blocking out geometry with primitives and the modifier stack, cleaning up non-manifold or boolean output, setting origins, UVs and normals, running it headless from Python, exporting to glTF or FBX, or working out why a script that behaved in the interface produces different or empty geometry in a background run. It supplies the modifier orders and the traps that reach an exporter, the determinism contract, the data-API rules that replace operators, and the assertions that catch a bad export before its consumer does. Do not use it to decide what a model should look like or how it should be decomposed, or for engine-side import settings, material graphs and texture painting.
---

# Drive Blender from a script

**A model that cannot be rebuilt is a screenshot.** Everything here serves one property: the same
inputs produce the same geometry on another machine, in a build with no display, next month. Blender
interactively is a different program from Blender headless, and most of the traps below are that
difference.

This skill covers running Blender and getting geometry out of it correctly. What the model should
look like, and which parts deserve independent authoring, is design work with its own procedure.

## Confirm the version before using the API

Blender's Python API breaks between releases, and a script written against an older one fails in ways
that read as your mistake. 4.1 removed `use_auto_smooth`, the auto-smooth angle and
`calc_normals_split()`; smoothing is now the `sharp_face` and `sharp_edge` boolean attributes or true
custom split normals. 4.4 changed actions to layers, strips and channelbags.

Read the installed build's own documentation rather than recalling the API. Where a Blender MCP is
connected, use it to look up the real signature, inspect a file and render a preview for triage —
and commit nothing it produces.

## The determinism contract

```sh
blender -b --factory-startup --python-exit-code 1 --python author-<asset>.py
```

- **`--factory-startup` every time**, and **`--python-exit-code 1` before `--python`**: Blender exits
  0 on an uncaught traceback, so without it a crashed script reports success.
- **Seed every random draw from stable inputs** and never iterate a Python `set` of bmesh elements.

**Read [Headless and determinism](references/headless-and-determinism.md)** before writing a script that
must run in a build, or when a script that behaved in the interface misbehaves in background mode. It
holds the invocation flag by flag, the ordering hazards, name collisions and the depsgraph.

- **Hash the geometry, not the file.** Neither format is byte-stable: FBX embeds a timestamp and
  GUIDs, glTF a generator string. Hashing the file churns on a no-op re-export and tells you nothing.

## Build with data, never operators

`bpy.ops` calls resolve against a context that does not exist in background mode, act on global
selection state, push an undo step and force a depsgraph re-evaluation each time. A script built from
operators works in the interface and produces different or empty geometry headlessly.

Use `bpy.data`, `bmesh` and `mesh.from_pydata`. Where an operator is genuinely unavoidable, wrap it in
`bpy.context.temp_override(...)` and say in a comment why no data-API path exists.

```python
# Good: apply a transform without an operator.
mesh.transform(obj.matrix_world)
obj.matrix_world = mathutils.Matrix.Identity(4)
```

**Call `depsgraph.update()` before `evaluated_get(depsgraph)`**, and **hold references, not names** —
Blender silently renames a colliding datablock to `name.001`.

## Build with primitives and modifiers, not with placed vertices

Block out the masses as primitives at real scale — **one Blender unit is one meter** — fix the
proportions there, and add structure through the modifier stack for as long as it can express the
shape. A model whose geometry comes from parameters and modifiers can be re-authored at a different
size or count; one made of placed vertices can only be edited.

The stack evaluates top to bottom and the order changes the result. **Apply scale before bevel,
solidify or array** — those work in local space, so a non-uniform scale makes the result uneven.

**Read [Building a model](references/modeling-in-blender.md)** before authoring geometry. It holds the
stack orders, the traps that survive into an export — unapplied scale, non-manifold geometry, boolean
output, an origin left where it landed — and how much topology the consumer actually needs.

## UVs and normals

- **Procedural geometry has no UVs, and the importer will not tell you.** Project UVs rather than
  unwrapping, because unwrap solvers are operators and are not deterministic.
- **Author normals explicitly**, and export FBX with `mesh_smooth_type='FACE'`; without it some
  importers open a dialog, which hangs a headless run.

**Read [Normals, UVs, slots and color](references/shading-uvs-and-materials.md)** before authoring
smoothing, unwrapping, assigning material slots or writing vertex data, or when a mesh imports black,
with an empty slot, or with an unwanted tint.

## Export

**Pick the format from what consumes it, and record why.** A consumer's own reader is usually
stricter than the format: it may require exactly one buffer, a flat node list, and `POSITION`,
`NORMAL`, `TEXCOORD_0` and non-empty `indices` on every primitive. Bake any texture-transform
extension into the UVs at author time unless you have confirmed the reader honors it.

**Apply transforms before export.** Unapplied scale distorts, negative scale flips winding and
normals, and unapplied rotation leaves the pivot's axes disagreeing with the consumer's.

**Declare the axis convention, the unit scale and the pivot, then assert them.** Where a consumer
mirrors handedness, the winding is already handled by that mirror — flipping winding as well
double-corrects into inside-out faces.

**Calibrate before authoring content.** Do not reason out the export flags: export one asymmetric
piece of known dimensions, have the consumer import and measure it, then pin that flag set. Getting
this wrong is otherwise discovered only after a whole kit exists.

## Assert before the export

In the script, before exporting, against the **evaluated** mesh: bounds against the declared size, the
pivot at the declared point, no face with an area below about `1e-8`, no loose geometry, a UV layer on
every loop with no zero-area triangle, every `material_index` in range, and every declared material
slot used.

These assertions prove what left Blender, not what arrived. The consumer still needs its own import
gate — dimensions, pivot, sections, slot names in order — and that gate belongs to the consumer's side.

## References

Read [the sources](references/sources.md) when auditing a rule or after a Blender version change.
