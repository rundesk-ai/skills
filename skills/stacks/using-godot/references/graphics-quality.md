# Graphics quality

Every setting here changes how the whole game looks: it belongs in a commit that says so, with a capture
before and after. A headless run renders nothing.

## Limits that drop things silently

- **Forward+ counts lights, decals and reflection probes together** against
  `rendering/limits/cluster_builder/max_clustered_elements` (512 in view). A city at night with more street
  lights than that stops drawing the extras without an error.
- **Mobile and Compatibility light at most 8 omni and 8 spot lights per mesh**; a long road mesh under a
  row of lamps shows only eight. Split the mesh, or use Forward+.
- The renderer is a project-wide decision with different feature sets, not a quality slider; only
  Compatibility exports to the web.

## Global illumination for a world built at runtime

- `LightmapGI` bakes only in the editor, so it cannot light a generated city or anything the player
  builds.
- `VoxelGI.bake()` runs in an exported game — viable for a level generated before play.
- **SDFGI needs no bake** and follows structures built during play; it is the most expensive, and dynamic
  objects receive its light without casting into it. On desktop, start with SDFGI and give players a
  setting to turn it off.

## Shadows for a strategy or builder camera

**With an orthographic camera, `directional_shadow_max_distance` is ignored** (by design, in the engine
source), so the shadow map spans the camera's whole near-to-far range: a camera with `far = 2000` blurs
shadows over two kilometres. Set `near` and `far` to just enclose the scene's depth, and prefer
`directional_shadow_mode = SHADOW_ORTHOGONAL` — the PSSM splits slice by depth, which hardly varies
looking down. With a perspective camera, set `directional_shadow_max_distance` (default 100) to the
visible area.

## Shader stutter

Ubershaders (4.4+, Forward+ and Mobile) remove most first-use compilation hitches, but these still
compile on first use: the first 2D draw, changing MSAA or shadow settings at runtime, the first VoxelGI,
SDFGI or probe, and viewports with different MSAA. Compatibility compiles every material the first time
it is seen. Watch `Performance.PIPELINE_COMPILATIONS_*`, and pre-warm while loading by drawing one of each
material and effect — one chunk of each biome — behind the loading screen.

## Judgment calls for a top-down camera

Not measured; capture an A/B per project. TAA smears moving units and screen-locked markers, so MSAA 2× or
4× usually suits a builder; volumetric fog costs a lot and is mostly invisible from a high camera.

## Textures and export

A texture assigned only from code stays lossless and unmipmapped — see
[Performance and memory](performance-and-memory.md). `rendering/textures/vram_compression/import_etc2_astc`
is off by default and must be on to export for mobile and for an arm64 macOS build.
