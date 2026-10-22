# Pixels, shaders, and proof

Read this before changing pixel snapping, texture filters, atlas sampling, alpha, blending, shaders, render
targets, or visual regression coverage.

## Choose a sampling policy per asset family

For intentional pixel art, default to:

- nearest sampling for magnification;
- integer output scaling when the product permits it;
- one declared texel-to-logical-unit relationship; and
- snapping at the final framebuffer transform, applied consistently to the camera/world container and the
  sprites it carries.

Do not independently round a camera, parent, child, and vertex. Their errors compound into shimmer, gaps, or
one-pixel relative motion. Odd sprite dimensions and half-unit pivots require an explicit convention; “all
positions are integers” is not enough when the final transform lands the pivot between physical pixels.

Pixel snapping deliberately quantizes motion. If smooth subpixel movement matters more than a fixed pixel
grid, choose smooth sampling or render the world to a fixed low-resolution surface and integer-scale that
surface. Do not toggle unrelated settings until one screenshot looks acceptable: filter, transform snapping,
camera timing, stretch, and fractional positions interact.

For continuously scaled or antialiased art, use linear filtering and suitable mipmaps for minification.
Nearest sampling makes blended edge texels blocky; disabling mipmaps at deep zoom can shimmer and stress cache.
Validate the chosen policy at every supported scale instead of assigning one sampler to the scene.

## Treat an atlas as a runtime package

Keep together:

- image pages and mip levels;
- sprite rectangles, rotation/trim, original size, and pivot metadata;
- padding/extrusion and transparent-edge treatment;
- sampler, wrap, color-space, alpha, compression, and platform overrides; and
- loader schema/version and generated lookup constants.

Generate and validate these as one contract. If a strict loader rejects a new manifest field and silently
installs a fallback, byte-identical atlas pixels do not protect visual quality. Surface fallback use in logs,
debug UI, or tests so a degraded image is not approved as the intended result.

Linear filtering samples neighboring texels, and mip generation expands that neighborhood. Use packer-generated
edge extrusion and padding appropriate to every used mip, or isolate regions/pages whose downsampled footprints
would meet. Mipmapped sprites cannot be packed as tightly as unmipped ones, because downscaled levels bleed
into their neighbours.

Do not rely on a universal half-texel nudge. Region coordinates, normalized UV conventions, backend sampling,
rotation, and mip level determine the correct inset. Generate region-safe UVs from the atlas contract and test
the actual runtime sampler.

## Keep alpha and color math consistent

Choose one alpha representation for each pipeline:

```text
Straight source:       rgb is independent; blend rgb with (src_alpha, 1-src_alpha)
Premultiplied source:  rgb already includes alpha; blend rgb with (1, 1-src_alpha)
```

Use the appropriate separate alpha factors when the destination alpha is retained. The active engine or
backend owns the API spelling.

The importer, decoded texture, mip generator, vertex tint, fragment shader, intermediate target, readback,
and final compositor must agree. Double-premultiplication darkens edges; straight data with premultiplied
blending glows; premultiplied data with straight blending darkens.

Under premultiplied alpha:

- fully transparent output is `(0, 0, 0, 0)`;
- multiply RGB and alpha consistently when applying opacity;
- guard any transform that maps black to non-black by coverage; and
- filter/downsample in a representation that cannot pull hidden RGB into visible edge pixels.

Resizing channels for mips without premultiplying first produces white mip edges; a duplicated shader
transform that colors zero-alpha texels produces bright wedges. Both failures are caught by tiny reference vectors containing
opaque, partial, and zero coverage—not by inspecting only the source PNG.

Blend in the intended color space. An enabled sRGB framebuffer linearizes the stored destination before
blending. If a backend or intermediate target skips that conversion, identical blend
factors can still produce different edges and gradients.

Preserve painter order for ordinary translucency. Draw opaque/cutout content under its declared depth policy,
then translucent content in its semantic back-to-front order unless a proven order-independent technique is
being used. Additive and multiply effects are separate compositing contracts, not flags to mix into an alpha
batch accidentally.

## Treat a shader as part of the material contract

Before replacing a stock shader, enumerate what the old path supplied:

- transform and coordinate conventions;
- texture region and sampler/wrap behavior;
- vertex color, tint, opacity, and premultiplication;
- clip/stencil/depth behavior and render-target color space;
- per-frame and per-instance uniform ownership; and
- the material identity used for batching.

A shader that compiles but drops vertex tint, changes alpha convention, samples outside an atlas region, or
uses unique state per sprite is a renderer regression.

Keep shared shader math in one include or generated source supported by the toolchain. If a CPU reference,
asset generator, and shader must implement the same transform, pin them with shared reference values and name
which implementation is authoritative. Copy-pasted transforms drift.

Follow the pinned shading-language and engine toolchain contracts. For GLSL, `#version` must precede everything
except whitespace and comments, but cross-compilers may impose stricter conventions; prove freshly generated
variants on every required backend. Route exact toolchain syntax and uniform/batching mechanics to the active
engine skill.

## Build an honest proof stack

### Headless contract cases

Keep pure renderer policy callable without the graphics engine where practical:

- snapshot adapter output and lifetime/generation checks;
- coordinate forward/inverse and final snap functions;
- pivot placement and conservative bounds;
- semantic sort keys and stable ties;
- cull, dirty-halo, chunk-edge, LOD, and page-rollover decisions;
- atlas manifest/loader schema and resource fallback state; and
- alpha/color reference vectors.

For finite adjacency or variant systems, enumerate the complete pair/state matrix. Hand-picked scenes trend
toward the cases already understood. Use the shipped pure emitter or selector, not a duplicate test
implementation.

### Renderer captures

Render a deterministic fixture through production shaders, atlas metadata, command formation, and backend.
Freeze random seed, snapshot, presentation time, viewport, display scale, font/assets, and feature flags.
Store the actual image, approved baseline, and diff. Hardware can produce small differences, so maintain
explicit platform baselines or a justified tolerance rather than making the threshold wide enough to hide seams.

Never auto-approve a new golden because the test failed after an intentional change. Inspect the diff and
version the approval. A golden protects against change; it does not prove the approved picture was correct.

### Live target inspection

Automated capture does not replace the live window. Exercise:

- required graphics backends and device classes;
- minimum, typical, and maximum aspect ratios and display/content scales;
- every zoom/LOD boundary, resize/fullscreen transition, and camera motion direction;
- atlas page and command rollover, dense overlap, and translucent pass crossings;
- missing/rejected assets and fallback visibility; and
- shader effects at zero, partial, and full coverage.

Inspect motion as well as stills. A single frame cannot reveal shimmer, jitter, stale dirty chunks, pool
flashes, or LOD thrash. Report which live targets were not available.
