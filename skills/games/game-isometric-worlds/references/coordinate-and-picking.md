# Coordinate and picking contracts

Use this reference when choosing projection dimensions, deriving grid/screen conversion, importing
isometric editor data, or making elevated and sloped surfaces pick exactly where they draw.

## Choose and name the basis

For a common diamond view with `+x` down-right, `+y` down-left, and `+z` up the screen, define:

```text
half_w = projected half-width of one grid cell
half_h = projected half-height of one grid cell
rise   = projected pixels per world height unit
origin = projected location of world (0, 0, 0)

screen_x = origin_x + (x - y) * half_w
screen_y = origin_y + (x + y) * half_h - z * rise
```

This is one handedness, not a universal naming scheme. Mirroring the view or swapping axes changes
signs. Preserve the declared basis instead of correcting formulas until a screenshot looks right.

A 2:1 diamond uses `half_h / half_w = 0.5` and is the usual pixel-art dimetric choice. A true
isometric projection has a different vertical ratio; choose it deliberately and make assets, editor
data, picking, and culling use the same result. Projection geometry does not require a power-of-two
tile size.

## Derive the known-height inverse

Remove the origin and known elevation first:

```text
a = (screen_x - origin_x) / half_w       = x - y
b = (screen_y - origin_y + z * rise) / half_h = x + y

x = (a + b) / 2
y = (b - a) / 2
```

With unknown height, setting `z = 0` yields only a flat-plane candidate. For this basis, an elevation
of `z` moves the true candidate by `z * rise / (2 * half_h)` along both grid axes. That relationship
is useful for convergence, but it does not decide which of several visible surfaces the pointer hits.

Keep projection and inverse in one module with shared constants. Test the algebra against fractional
points before applying floor or map bounds; an integer-only round-trip can hide half-cell errors.

## Invert the entire transform chain

A device coordinate normally includes more than the isometric basis:

```text
world projected point
-> world-container transform
-> camera/view transform
-> viewport or safe-area transform
-> device scale
```

Pointer conversion applies those inverses in reverse order before the grid inverse. Use the live
transform values that drew the frame. Do not manually subtract a remembered pan and divide by a
nominal zoom while the renderer also applies pivot, safe-area, device-scale, or orientation transforms.

## Define cell ownership at boundaries

Keep the inverse result fractional until the hit policy runs.

- Use mathematical floor for half-open cells; integer truncation maps negative fractions toward zero.
- State which adjacent cell owns an exact shared edge or corner. Stable half-open rules prevent hover
  flicker as floating-point noise changes sign.
- If a tool selects a projected diamond rather than an abstract grid cell, run a containment test and
  check the neighbouring candidates around a boundary.
- Apply map bounds after resolving the candidate. Return miss by default; clamp only for interactions
  that explicitly promise clamping.

## Resolve height according to topology

Select the method from the world shape:

### Known plane or layer

When the tool already knows the target plane, invert with that plane's `z` and test its footprint.
This is appropriate for a dedicated floor editor, not for choosing among visible stacked surfaces.

### One continuous heightfield

Start from the flat candidate and solve `z = height(x, y)` through the projection. A bounded fixed-point
iteration works for many constrained tile slopes; a ray/triangle intersection works for an explicit
mesh. Approach rules matter at discontinuous foundations or cliff faces: an iteration can converge to
the hidden side and make a visible region unpickable.

Declare a maximum iteration count, convergence tolerance, and deterministic fallback. Test the steepest
supported relief and both view-facing directions. Never add an unbounded loop to input handling.

### Discontinuous or stacked surfaces

Fixed-point height sampling is insufficient when one screen ray may meet a roof, bridge, ground, and
underground surface. Query conservative candidate surfaces, intersect their actual geometry or hit
polygons, then select by visible depth and the tool's selectability policy. A reveal or underground
mode changes that policy; it does not change the stored world point.

## Share slope topology

Store or derive the surface from one authority, commonly corner heights plus a declared split. For a
four-corner tile:

```text
corner heights -> chosen triangle diagonal -> two surface equations
```

The diagonal is observable on a saddle. Drawing one split while picking or placing against another
creates a region that looks above or below its interactive surface. Put triangle selection and height
sampling in one pure function used by render geometry, picking, placement, grid overlays, and any
surface-following object.

Pin continuity at shared edges: neighbours that claim a continuous seam must return the same endpoint
and interpolated edge heights. A ramp or bridge should expose its run-axis edge heights, not only one
centre elevation; equal centre values do not prove a traversable or visually continuous seam.

## Separate footpoint from pixels

Represent an object placement as:

```text
world footpoint or support footprint
projected footpoint
sprite hotspot relative to its image rectangle
optional presentation offset
```

Bottom-centre is a useful default for upright tile objects and a common map-editor default for
isometric tile objects. Still import the editor's declared alignment and drawing offset explicitly.
The sorting and placement point stays stable when an animation frame or skin changes size.

Debug by drawing a small cross at the projected footpoint and outlines for the occupied world footprint,
projected hit shape, and bitmap bounds. If changing the bitmap moves the cross, presentation data has
leaked into the world contract.
