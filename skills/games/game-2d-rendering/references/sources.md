# Engineering 2D rendering source map

Use this file to audit a rule, not as more procedure. The rules rest on public engine and specification
contracts, practitioner renderer accounts, reproduced issue reports, visual-test guidance, and anonymized
first-hand records; none of them prescribes one engine architecture.

## Coordinates, placement, and ordering

- Godot's official [Viewport and canvas transforms](https://docs.godotengine.org/en/stable/tutorials/2d/2d_transforms.html)
  documents the local, canvas, global-canvas, stretch, and window transform chain, its inverses, and input
  conversion. This establishes the need to name every space and use the complete transform for draw/input
  agreement; it does not prescribe Godot APIs elsewhere.
- Godot's official [CanvasItem reference](https://docs.godotengine.org/en/stable/classes/class_canvasitem.html)
  documents z-index bands, relative z, Y-sort behavior, texture filter inheritance, and visibility layers.
  It supports semantic bands plus contact-anchor ordering and explicit material/filter state.
- Tiled's official [Working with Objects](https://doc.mapeditor.org/en/stable/manual/objects/) documents that
  tile-object alignment controls placement relative to the object origin; its
  [tileset guidance](https://doc.mapeditor.org/en/stable/manual/editing-tilesets/) further notes that alignment
  is the rotation origin. These are the source for authored logical pivots rather than bitmap centers.
- Factorio's current [RenderLayer prototype contract](https://lua-api.factorio.com/latest/types/RenderLayer.html)
  exposes an ordered semantic layer roster from lowest to highest. It corroborates explicit layer meaning;
  it is not a category list to copy.

## Snapshot and renderer preparation

- Posila's Factorio [Friday Facts 150: New Terrain Experiments](https://factorio.com/blog/post/fff-150)
  describes a synchronized prepare step that collects draw order/data before render proceeds alongside game
  update. This named-practitioner account supports a coherent draw-ready generation; its exact loop and
  animation-in-state decision are Factorio-specific.
- Glenn Fiedler's [Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/) derives previous/
  current state interpolation with an accumulator. The
  gameplay runtime owns that timing contract; here it only keeps presentation interpolation in the read-only adapter.
- Two anonymized first-hand C++ simulation records established that renderer-facing semantic state,
  stable identity, and a read-only adapter prevented engine types and frame timing from entering deterministic
  simulation. These private records are scoped architecture evidence, not a claim that every game needs the
  same snapshot storage or thread model.

## Culling, pooling, batching, pages, dirty work, and LOD

- Godot's official
  [VisibleOnScreenNotifier2D reference](https://docs.godotengine.org/en/stable/classes/class_visibleonscreennotifier2d.html)
  documents rectangular render-culling visibility and its one-frame determination delay. It supports
  conservative visual bounds and warns that visibility feedback has timing; it is not a portable culling API.
- Robert Nystrom's [Object Pool](https://gameprogrammingpatterns.com/object-pool.html) explains the allocation-
  churn use case, fixed pool size/memory tradeoff, and object-reset responsibility. This supports pooling only
  proven expensive churn and testing complete reset.
- Factorio [Friday Facts 227: Rendering, Trees & Scenario talk](https://factorio.com/blog/post/fff-227)
  reports logical sprite atlases for batching, VRAM tradeoffs, mip use at zoom, and mip-level atlas bleed.
  It is the practitioner basis for grouping content normally drawn together and treating padding/mips jointly.
- Factorio [Friday Facts 251: A Fistful of Frames](https://factorio.com/blog/post/fff-251) documents compatible-
  state sprite batches, fixed-size buffer rollover, four vertices per sprite, a static index buffer, and a
  renderer benchmark over about 25,000 sprites. It supports capacity-derived rollover and representative
  render workloads, not one universal buffer size.
- Factorio [Friday Facts 264: Texture streaming](https://factorio.com/blog/post/fff-264) reports allocation/
  eviction stalls and fragmentation, thousands rather than hundreds of draw calls outside atlases, 128×128
  virtual pages, and lower mip detail to bound zoomed-out residency and upload time. These are shipped-system
  tradeoffs, not portable constants.
- Posila's [Friday Facts 323: Animated water](https://factorio.com/blog/post/fff-323) reports a 3 ms prepare-
  render regression when animation forced full terrain rebuild, then per-chunk caching of static draw-order
  data with global-time animation kept dynamic. It establishes the static/dynamic split and chunk-local
  invalidation lesson.
- Posila's [Friday Facts 333: Terrain scrolling](https://factorio.com/blog/post/fff-333) describes reusing the
  previous terrain texture, shifting it, and filling newly exposed regions, plus the bandwidth cost of the old
  two-screen copy. It supports dirty/reuse work only when the backend actually preserves unchanged pixels.
- Khronos' [`glDrawElements` reference](https://registry.khronos.org/OpenGL-Refpages/gl4/html/glDrawElements.xhtml)
  and [OpenGL 4.6 core specification](https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf) establish
  index types and API capability queries. The 16-bit 65,535 index fact is a type contract; sprite/page capacity
  still depends on the engine's vertex layout and command path.
- An anonymized first-hand renderer crash occurred when a zoomed-out sprite batch crossed its 16-bit
  command path's capacity. Another record found that a fixed safe zoom changed with window size. These are
  scoped failure evidence for derived rollover and independent capacity guards, not a universal engine limit.

## Sampling, alpha, and shaders

- Unity's current [Sprite Atlas reference](https://docs.unity3d.com/Manual/sprite/atlas/sprite-atlas-reference.html)
  documents padding as a buffer preventing overlap, mip generation, filtering, rotation/tight packing, sRGB,
  platform overrides, and the memory cost of readable texture copies. It supports treating atlas image,
  metadata, sampler, and platform settings as one package.
- Godot issue [#76435](https://github.com/godotengine/godot/issues/76435) reproduces a one-pixel atlas border
  artifact at fractional sprite positions under multiple integer stretch scales. Godot issue
  [#66527](https://github.com/godotengine/godot/issues/66527) reproduces a pixel-art sprite stopping blurred at
  some subpixel positions, and [#86634](https://github.com/godotengine/godot/issues/86634) records camera-
  smoothing jitter when display/update timing differs. Issue reports establish real interactions to test;
  they do not prove one portable fix or current behavior in every Godot release.
- Khronos' [`glBlendFunc` reference](https://registry.khronos.org/OpenGL-Refpages/gl4/html/glBlendFunc.xhtml)
  and [OpenGL 4.6 core specification](https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf) establish
  straight/premultiplied blend factors, separate source/destination contribution, and sRGB destination
  linearization before blending when enabled. The rules express the math portably and routes API state to
  the active engine.
- NVIDIA engineer Neil Bickford's response in
  [NVTT mipmaps with white edges](https://forums.developer.nvidia.com/t/nvtt-for-photoshop-creates-mipmaps-with-white-edges/208856)
  identifies a 2021.2 Texture Tools defect: channels were resized independently without intended
  premultiplication, allowing hidden white RGB to bleed into semitransparent black. The 2023.1 release fixed
  the reported case. This is maintainer failure/resolution evidence for alpha-aware filtering.
- Shawn Hargreaves'
  [How Shawn learned to stop worrying and love premultiplied alpha](https://shawnhargreaves.com/blog/how-shawn-learned-to-stop-worrying-and-love-premultiplied-alpha.html)
  is named-practitioner evidence for filtering/edge artifacts and treating premultiplication as a pipeline
  decision rather than an isolated blend flag.
- The [GLSL 4.60 specification](https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf), section
  3.3, permits only whitespace or comments before `#version`. Engine cross-compilers can be stricter, so the
  rules require the pinned toolchain and generated backend variants rather than generalizing one compiler's
  diagnostic.
- An anonymized first-hand shader record reproduced nonzero RGB at zero alpha as bright transparent-
  corner wedges; duplicated tint logic caused one shader to miss the coverage guard. A second record found a
  runtime atlas package rejected after its generated manifest and independently hard-coded loader cardinality
  drifted. These observations support one-home shader math, reference vectors, generated schema constants,
  and visible fallback status.

## Visual and headless proof

- Chromium's versioned
  [Ash pixel unit testing guide](https://chromium.googlesource.com/chromium/src/+/refs/tags/137.0.7125.0/ash/test/pixel/README.md)
  captures the real rendered UI, compares benchmark images pixel by pixel, retains platform identity, warns
  that local and CI hardware can differ, requires stable animation state, and versions intentional baseline
  changes. It supports deterministic production-renderer capture plus reviewed diffs.
- An anonymized first-hand tiling record passed an offline composite built from duplicated placement
  assumptions while the live high-DPI window showed large seams. A later adjacency system required repeated
  screenshot fixes until the complete adjacent-state pair matrix was executed through the shipped pure
  emitter. These records support the headless-production-code/live-window split and exhaustive finite
  matrices; they do not imply that every renderer can produce deterministic golden images across GPUs.

