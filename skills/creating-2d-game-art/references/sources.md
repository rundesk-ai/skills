# Sources

Official tool documentation establishes file and metadata contracts;
platform guidance supports accessibility checks; named practitioner material supports pipeline and
visual-review heuristics. Tool defaults are examples, not universal engine settings.

## Runtime metadata and placement

- [Aseprite: Slices](https://www.aseprite.org/docs/slices/) documents named slice bounds, nine-slice
  centers, pivots, and JSON export. This supports exporting explicit pivots and slice metadata rather
  than deriving placement from a packed rectangle.
- [Aseprite: Tags](https://www.aseprite.org/docs/tags/) documents named animation ranges and playback
  directions. It supports semantic clip grouping; the requirement to preserve gameplay
  meaning and timing is an integration conclusion, not a claim that tags define game authority.
- [Tiled: Editing Tilesets](https://doc.mapeditor.org/en/latest/manual/editing-tilesets/) documents
  object alignment, drawing offsets, isometric grid orientation, collision shapes, custom hot spots,
  tile metadata, and animation previews. It supports separating a sprite's visible image, placement
  origin, and interaction shapes.
- [Tiled: Working with Objects](https://doc.mapeditor.org/en/stable/manual/objects/) explains that
  tile-object alignment changes the image relative to the object origin and that isometric defaults
  differ from other map orientations. This is the source for the base-point warning.

Derived pair: **good** exports a stable logical base/pivot and explicit shapes; **bad** derives
placement and collision from each PNG's current alpha bounds. Tool contracts expose these as
separate data because image rectangles do not reliably represent gameplay placement.

Integration rule: Aseprite's exported per-frame bounds and pivots make a clip-level union
derivable. Storing that union is a conservative integration rule for stable culling across animation,
not an Aseprite requirement. It covers authored frame pixels and offsets only; renderer-owned runtime
effects add their own bounds.

## Atlas and sampling contracts

- [libGDX TexturePacker](https://libgdx.com/wiki/tools/texture-packer) documents padding, edge bleed,
  duplicate padding, rotation, whitespace stripping, path flattening, alpha mode, texture filters,
  scale variants, and indexed animation regions. It explicitly warns that rotation and stripping
  require special draw handling and that bleed prevents filtered samples from taking unwanted RGB
  from transparent pixels.
- [Unity 6: Prepare sprites for a 2D Pixel Perfect Camera](https://docs.unity3d.com/6000.0/Documentation/Manual/urp/2d-pixelperfect-prep-sprites.html)
  documents a consistent pixels-per-unit contract, point filtering, uncompressed source, and custom
  pivots for that specific pixel-perfect pipeline. This skill limits it to pixel-art-style
  presentation; it does not prescribe point filtering for antialiased raster art.
- [Unity: Sprite import settings](https://docs.unity3d.com/Manual/texture-type-sprite.html)
  documents pixels per unit, sprite meshes and pivots, wrap modes, point/bilinear/trilinear filters,
  mipmaps, border replication, and platform overrides. It supports choosing import behavior by asset
  and target rather than applying a scene-wide “2D” preset.

Derived pair: **good** declares trim, rotation, padding, alpha, sampling, and stable names and tests
the packed output; **bad** treats an atlas as a visual collage. The bad path produces shifted pivots,
name collisions, rotated regions, seams, or halos when the loader and packer disagree.

## Readability and accessibility

- [Xbox Accessibility Guideline 102: Contrast](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/102)
  covers gameplay cues as well as UI, recommends checking changing backgrounds, warns against
  red/green-only distinctions, and supports configurable contrast. Its numerical thresholds are
  platform guidance for scoped elements; this skill uses the broader requirement to measure
  important assets in context and not rely on color alone.
- [Xbox Accessibility Guideline 109: Object clarity](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/109)
  addresses identifying important game objects and distinguishing interactive elements from visual
  noise. It supports native-scene readability checks; it is a guideline, not a guarantee that one
  silhouette or outline treatment works for every art direction.
- Michael Geig's named-practitioner article,
  [3 steps to improve your game's graphics](https://www.gamedeveloper.com/art/3-steps-to-improve-your-game-s-graphics),
  uses silhouette checks before lighting and stresses fresh-context review. This is a practitioner
  heuristic, not an empirical effect-size study; the skill treats silhouette as an early diagnostic,
  not a universal definition of visual quality.

Derived pair: **good** reviews state cues at real size across representative backgrounds and uses
multiple visual channels; **bad** approves an enlarged transparent-background sprite whose critical
state is color-only. The failure is loss of meaning in motion, visual noise, or differing vision.

## Production pipeline and validation

- [Aseprite: Command Line Interface](https://www.aseprite.org/docs/cli/) documents scripted export of
  sprite sheets and JSON data plus frame tags, slices, filename formats, trimming, packing, and other
  declared options. It supports repeatable derivation from an accepted editable master. It does not
  guarantee byte-identical output across tool versions, operating environments, or external image
  generators.
- Jeff Hanna, [The Polished Pipeline](https://media.gdcvault.com/GD_Mag_Archives/GDM_December_2005.pdf),
  *Game Developer*, December 2005, describes keeping source and processed assets separate, validating
  submissions before they consume pipeline resources, returning actionable failures, and avoiding
  silent automatic source changes. It is an experienced production account from a 2005 tool context;
  the durable lesson is explicit validation and traceable transformation, not its tooling details.
- [Implementing Robust and Scalable Art Integration](https://gdcvault.com/play/1014906/Implementing-Robust-and-Scalable-Art)
  is a GDC Europe 2011 production case by Bill Green and Jeff Hanna describing delivery checkpoints
  and coordination between changing art and code. The public overview establishes the checkpoint
  model; it does not expose quantitative comparison data.
- [Technical Artist Bootcamp: The Dual Power of Metanodes in Maya](https://www.gdcvault.com/play/1025950/Technical-Artist-Bootcamp-The-Dual)
  is Andrew Christophersen's 2019 ArenaNet practitioner session. Its overview identifies brittle
  naming conventions as a failure mode and advocates serialized metadata. This skill applies that
  lesson to stable sprite identities without copying its Maya-specific implementation.
- W3C,
  [PROV Overview](https://www.w3.org/TR/prov-overview/), defines provenance as information about the
  entities, activities, and people involved in producing data or a thing, and describes identifying
  objects, attribution, and processing steps. This supports recording source and transformation
  lineage. The skill requires a fit-for-project manifest; it does not prescribe W3C PROV
  serializations for a game pipeline.

Derived pair: **good** keeps editable source, declared export settings, stable metadata, validation,
and packed derived output; **bad** hand-edits derived atlases or lets validation silently repair
source. The replacement makes failures reproducible and prevents the next export from undoing a
hidden fix.

Integration rule: record an accepted master as well as generator version, seed, parameters, and
ordered references when those inputs exist. The sources establish explicit export inputs,
transformations, and provenance; they do not establish that a seed reproduces pixels across changing
models, hosted services, tool versions, or nondeterministic operators. For the same reason, a
generated sheet is source imagery until the project supplies and validates stable frame IDs, clips,
timing, pivots, trim offsets, and loader metadata.

## Limits

No cited source establishes a universal palette size, sprite resolution, animation frame count,
atlas dimension, outline style, or pixel density. Those are project, platform, and art-direction
decisions and must be proven in a representative scene. Legal ownership and model-training rights
for generated assets vary by source and jurisdiction; follow the project's current legal policy
rather than inferring permission from visual similarity or a file format.
