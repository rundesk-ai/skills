# Instancing and cameras

Examples are GDScript; C# uses the same engine names in PascalCase.

## When automatic instancing does not happen

Forward+ draws `MeshInstance3D` nodes that share a mesh and an opaque or alpha-tested material together
with no setup. **Alpha-blended and depth-prepass materials are never instanced this way**, and Mobile and
Compatibility do not instance at all, so there each node is a draw call.

## MultiMesh order of operations

```gdscript
var multi := MultiMesh.new()
multi.transform_format = MultiMesh.TRANSFORM_3D   # the default is TRANSFORM_2D
multi.use_colors = true                           # flags before instance_count, or they error
multi.mesh = mesh
multi.instance_count = transforms.size()          # allocates; set once, after format and flags
multi.buffer = packed_floats                      # one assignment, not one call per instance
$Instances.multimesh = multi
```

- `use_colors`, `use_custom_data` and the transform format can change only while `instance_count` is 0;
  setting `instance_count` clears and resizes the buffers.
- **One MultiMesh shares one bounding box**: instances are not culled one by one, it is never culled while
  any part is on screen, and every instance gets the same LOD. Split by chunk, one per mesh and material.

## Orthographic cameras

- **`size` is the vertical extent in metres** (`keep_aspect` defaults to height). To fit something wider
  than tall, divide its width by the aspect:

  ```gdscript
  camera.size = maxf(extent.y, extent.x / aspect) * margin
  ```

- **`near` and `far` still clip in orthographic mode**, and with a directional light they also set the
  whole shadow range (see [Graphics quality](graphics-quality.md)). Enclose the scene's depth and no more.
- A headless run reports a placeholder viewport size for the whole run. Frame the camera from
  `display/window/size/viewport_width`/`_height` and follow the real size through `size_changed`, or the
  framing looks wrong only in tests.
