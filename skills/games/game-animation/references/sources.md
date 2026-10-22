# Engineering game animation source map

Use this file to audit a rule, not as more procedure. The rules rest on engine documentation, an
interchange specification, asset-tool contracts, and practitioner timing guidance.

## State graphs, transitions, blends, and layers

- Epic Games, Unreal Engine 5.8,
  [State Machines](https://dev.epicgames.com/documentation/en-us/unreal-engine/state-machines-in-unreal-engine),
  documents entry, states that produce poses, directed transitions, blend behavior, and reset-on-
  entry semantics. It establishes that transition direction and re-entry are explicit graph
  contracts; it does not require one graph structure or semantic vocabulary for every game.
- Godot stable,
  [Using AnimationTree](https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html),
  documents one-shots and aborts, blend trees, time seek/scale, state machines, immediate/synchronized/
  at-end transition modes, crossfades, reset, priority, and advance conditions. This supports the
  state/blend/one-shot selection and explicit transition table. Exact nodes and priority rules remain
  Godot-specific.
- Unity 6,
  [Animation State Machines](https://docs.unity3d.com/6000.0/Documentation/Manual/AnimationStateMachines.html)
  and [Animation Layers](https://docs.unity3d.com/6000.0/Documentation/Manual/AnimationLayers.html),
  document state/transition graphs plus override or additive layers and body masks. They corroborate
  separating independent pose concerns and declaring composition; they do not prove that layering is
  simpler or cheaper for an unmeasured graph.

The recommendation to minimize full-body state multiplication, reserve global transitions for true
high-priority reactions, and declare overlapping-layer ownership is a conclusion drawn from these
graph capabilities and their interaction surface.

## Clip and import contracts

- Khronos Group,
  [glTF 2.0 animation specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html#animations),
  defines animation samplers, input/output accessors, interpolation, channels, target nodes, and
  translation, rotation, scale, and morph-weight paths. This establishes explicit sampled clip data
  and target bindings for one interchange format; the skill's semantic IDs, root policy, masks, and
  validation schema are broader integration requirements.
- Aseprite, [Tags](https://www.aseprite.org/docs/tags/) and
  [Slices](https://www.aseprite.org/docs/slices/), documents named animation ranges and playback
  directions plus slice bounds, pivots, and JSON export. This supports stable 2D clip grouping and
  pivot metadata rather than filename order or trimmed centers.
- Tiled, [Working with Objects](https://doc.mapeditor.org/en/stable/manual/objects/), documents that
  tile-object alignment changes an image relative to its object origin and that isometric alignment
  defaults differ from other orientations. This supports keeping a logical contact point independent
  from bitmap bounds; detailed art production and isometric projection are separate work with their
  own contracts.

The clip contract and import rejection/fallback rules are a synthesis of these sources. No source mandates one
file format, clip naming convention, direction count, rig, frame rate, or runtime graph.

## Motion authority and presentation time

- Epic Games, Unreal Engine 5.8,
  [Root Motion](https://dev.epicgames.com/documentation/en-us/unreal-engine/root-motion-in-unreal-engine),
  distinguishes movement-component-driven characters with animation layered on top from animations
  whose root-bone displacement drives character motion when extraction is enabled. It also exposes
  root locking and extraction modes. This supports choosing one displacement authority; collision,
  networking, and interruption details must be verified in the active engine.
- Unity 6, [How Root Motion works](https://docs.unity3d.com/6000.0/Documentation/Manual/RootMotion.html),
  independently documents body/root transform projection and applying or baking motion from clips.
  It corroborates that root data and runtime object motion are separate contracts, not that every
  action should use root motion.
- Glenn Fiedler,
  [Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/) (2004), derives rendering
  between previous and current simulation states using the accumulator remainder. It supports
  presentation-only snapshot interpolation; the gameplay runtime owns the fixed-step and overload
  policy, and the article is practitioner derivation rather than an engine requirement.

The explicit authority handoff, teleport/correction discontinuity, and no-feedback-to-simulation
rules are safeguards built on those separate motion and presentation clocks.

## Events, synchronization, and durable facts

- Epic Games, Unreal Engine 5.8,
  [Animation Notifies](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-notifies-in-unreal-engine),
  documents events and duration states synchronized to animation, including sound, particles, sync
  markers, sockets, blend-weight thresholds, trigger chance, LOD filtering, leader/follower behavior,
  and queued versus more precise montage delivery. These features establish both useful presentation
  timing and multiple conditions under which delivery varies.
- Unity 6,
  [Add an Animation Event to an imported animation clip](https://docs.unity3d.com/6000.0/Documentation/Manual/AnimationEventsOnImportedClips.html),
  documents calling a function at a specified imported-clip time with a parameter. It corroborates
  clip-timed callbacks; it does not guarantee authoritative, once-only delivery through blending,
  seeking, replay, rollback, or LOD.

Derived pair: **good** commits damage or transfer in the authoritative action timeline and lets a
marker present the fact; **bad** lets a filtered, blended, skipped, or repeated presentation callback
be its only owner. This is a conservative conclusion from documented notify variability,
not a statement that engine animation events can never call gameplay code.

## 2D and isometric synthesis boundaries

- Stable bases, frame-family bounds, and semantic clip names are contracts shared with 2D art
  production; placement and depth remain renderer and projection work.
- World-facing to view-facing remap, explicit mirror eligibility, and rotation-wide attachment tests
  are conclusions drawn from those projection and placement contracts. No cited source establishes one universal
  four- or eight-direction layout.
- State/transition proof belongs here because it is animation-domain behavior. General automated-test
  structure, visual renderer proof, and performance claims are separate work.

## Good/bad pair mapping

- **Semantic action authority:** Epic's documented notify filters, blend thresholds, chance, and
  delivery modes establish why a visible frame or callback is an unsafe sole owner. The committed-
  action pair keeps the durable fact in the gameplay runtime's action timeline.
- **Transition priority:** Unreal and Godot expose directed transition, priority, and reset behavior.
  The stun/recovery pair applies those explicit contracts instead of allowing callback arrival to
  choose a pose.
- **Movement authority:** Epic and Unity distinguish in-place presentation from extracted root
  displacement. The two good examples select one owner; the bad example applies both documented
  motion sources and therefore double-integrates movement.
