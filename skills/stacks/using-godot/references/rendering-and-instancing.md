# Rendering, instancing and cameras

Examples are GDScript; C# uses the same engine names in PascalCase.

## Many identical things

Every `MeshInstance3D` is a node the engine processes, culls and submits. How much that costs depends on
the renderer:

- **Forward+ instances automatically**: `MeshInstance3D` nodes sharing a mesh and an opaque or
  alpha-tested material are drawn together with no setup. Alpha-blended and depth-prepass materials are
  never instanced this way.
- **Mobile and Compatibility do not**, so a node each is a draw call each.
- On every renderer, thousands of nodes still cost CPU time in the scene tree.

When the profiler shows either cost, draw one mesh many times from a `MultiMeshInstance3D`:

```gdscript
var multi := MultiMesh.new()
multi.transform_format = MultiMesh.TRANSFORM_3D
multi.use_colors = true                    # before instance_count, or it has no effect
multi.mesh = mesh
multi.instance_count = transforms.size()   # allocates; set once, not per instance
for i in transforms.size():
	multi.set_instance_transform(i, transforms[i])
$Instances.multimesh = multi
```

- **Set `instance_count` once, after the format and flags.** Setting it clears and resizes the buffers,
  and `use_colors`, `use_custom_data` and the transform format can only change while it is 0.
- **One MultiMesh per mesh-and-material pair.** Each distinct material is another draw.
- The whole MultiMesh shares one AABB, so instances are not culled individually and a MultiMesh spanning
  the world is never culled. Split by region when that shows in a measurement, not before.
- For large counts, fill a `PackedFloat32Array` and assign `buffer` once instead of one call per
  instance.

Rebuilding the whole buffer on a change is fine until measured otherwise.

## Materials

A material on the mesh applies to every instance. Per-instance variation comes from instance colours or
custom data read in a shader, not from more materials.

Meshes and materials are `Resource`s: assigning the same instance in two places shares it.
`duplicate()` gives a separate one, but shallowly — sub-resources stay shared unless you use
`duplicate_deep()` (4.5+). Sharing accidentally is the usual cause of "changing one changed them all".

## Cameras and projection

`Camera3D.projection` is `PROJECTION_PERSPECTIVE`, `PROJECTION_ORTHOGONAL` or `PROJECTION_FRUSTUM`.

**Orthographic when equal sizes must read as equal** — a builder, a board, a cross-section, a tactics
grid. Perspective converges parallel lines, so of two identical objects the further looks smaller, and a
tall one tapers.

In orthographic mode **`size` is the vertical extent in metres**, with `keep_aspect` defaulting to
height. To fit something wider than it is tall, divide its width by the viewport's aspect:

```gdscript
camera.size = maxf(extent.y, extent.x / aspect) * margin
```

Read the viewport size from the viewport when the game has a window, and recompute on its
`size_changed` signal. A headless run reports a placeholder size, so code that frames the camera from it
will look wrong only in headless tests.

`near` and `far` still clip in orthographic mode. A camera pulled well back needs a `far` to match, or
the far side of the world is silently missing.

## A camera rig

Putting the camera under a parent node and rotating the parent gives an orbit around the parent's
origin. Panning then means moving the parent, and moving it along its own basis keeps panning
screen-aligned at any angle:

```gdscript
position += basis.x * right + basis.y * up
```

Scale a drag by metres per pixel — the view height over the viewport height — so a drag moves the same
amount of world at every zoom.

## Renderer and quality

`rendering/renderer/rendering_method` selects Forward+, Mobile or Compatibility: a project-wide decision
with different feature sets, not a quality slider, and Compatibility is the only one for the web. MSAA
and shadow-atlas sizes are project settings; ambient light, fog and tonemapping live in the
`Environment` of a `WorldEnvironment`; whether a light casts shadows is on the light. A change to any of
them changes how everything looks, so it belongs in a commit that says so.

Shadows cost per light and per shadow-casting object. One directional light with shadows is usually the
whole budget worth spending before there is art to light.
