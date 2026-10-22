---
name: game-animation
description: Use when designing, implementing, reviewing, debugging, or integrating engine-agnostic runtime game animation, including semantic state and clip contracts, state machines, transitions, blend spaces, layers and masks, one-shots, interruptions, synchronization, in-place versus root-motion authority, animation events, snapshot interpolation, stable pivots or footpoints, and 2D or isometric directional animation. It supplies semantic clip and transition contracts, one movement authority, event-safety rules, and a transition proof matrix. Do not use it for drawing animation assets, simulation truth, character AI, isometric projection, renderer architecture, or engine-specific APIs alone.
---

# Engineer game animation

Make animation a faithful, interruptible presentation of committed game meaning. Choose one owner for
world movement and durable outcomes; use the animation graph to realize poses, timing, and emphasis.

## Establish authority and vocabulary

Record before building a graph:

- authoritative semantic states, actions, phases, and locomotion values the animator may observe;
- whether gameplay, navigation, physics, or animation owns world displacement for each action;
- the presentation clock, pause and time-scale behavior, snapshot interpolation policy, and
  discontinuities such as teleport, spawn, death, or correction;
- clip identities, rig or frame contract, loop policy, authored duration, root displacement,
  direction set, pivot or root, sockets, bounds, and markers;
- allowed transitions, priority, interruption windows, re-entry/reset behavior, and fallback pose;
- layer, mask, additive/reference-pose, and synchronization ownership; and
- target view orientations, movement extremes, frame rates, LODs, rigs, and asset fallbacks.

Name semantic intent separately from assets. `locomotion`, `airborne`, `stunned`, and
`attack-heavy` can survive a clip replacement; `run_v7_take2` cannot. Keep one adapter from semantic
state to animation parameters and requests. The graph must not infer durable gameplay state from the
currently visible frame, pose, blend weight, or engine callback.

```text
Good: committed action phase -> animation request -> pose and presentation markers.
Bad:  animation entered "attack" -> inventory, damage, and cooldown mutate immediately.
```

## Define clips as runtime contracts

For each clip or directional family, declare:

```text
ClipContract {
  semantic-id, rig-or-frame-set, duration, loop-policy
  authored-space, root-curve, stable-base-or-root, visual-bounds
  direction-or-mirror-policy, sockets, sync-markers, presentation-events
}
```

Validate identity and metadata at import. Reject or visibly substitute a missing clip, incompatible
rig, missing direction, invalid mask, unstable base, unexpected root displacement, or marker outside
the clip. Do not repair source mistakes with per-character runtime offsets that disappear on the
next export.

For 2D frames, preserve the logical base or footpoint through trim and packing; use a clip- or family-
level conservative visual bound when frame extents differ. For skeletal clips, validate the expected
root, bind/reference pose, retarget mapping, units, axes, curves, and bone or socket names. Keep source
motion and derived compression/import products distinguishable.

## Build graphs around behavior

Use the least complex graph that expresses the contract:

- use a discrete state for behavior with distinct entry, exit, interruption, or loop semantics;
- use a continuous blend for values such as speed or direction when authored samples interpolate
  coherently;
- use a one-shot or action layer for a bounded action that returns to a base pose;
- use a separate layer and mask only for genuinely independent pose contributions; and
- use a synchronization group or shared phase only when motions contain corresponding events.

Define every transition's source, destination, condition, priority, blend, reset or resume behavior,
and whether it may be interrupted. When several transitions can fire together, resolve them
deliberately. Global “any-state” transitions are appropriate for true high-priority reactions; using
them for ordinary flow hides reachability and interruption conflicts.

```text
Good: stun outranks locomotion and attack; recovery has an explicit interruption and re-entry rule.
Bad:  whichever transition callback runs first decides whether the attack, hit, or death pose wins.
```

Avoid multiplying full-body states for independent dimensions such as locomotion, equipment, injury,
and carried item. Prefer parameters or orthogonal masked layers when their ownership and composition
are actually independent. If two layers both author the same joint, sprite component, root, or socket,
declare precedence and test the overlap.

## Choose one movement authority

Default to **in-place animation** when gameplay, navigation, or physics owns position and collision.
Drive presentation speed and phase from committed velocity, distance, gait, or action state; correct
foot sliding by aligning authored stride and playback/blend behavior, not by adding a second position
integrator.

Choose **root motion** when authored displacement is intentionally the action's motion source and the
runtime can apply it through collision, navigation, networking, replay, and interruption policy.
Extract and apply the declared root delta once. Define what happens when collision blocks it, the
action is interrupted, the target moves, or correction occurs.

```text
Good: controller owns locomotion; animation consumes velocity and remains in place.
Good: authored vault root delta is applied once through the movement/collision contract.
Bad:  controller displacement and root displacement both advance the actor, then a snap hides drift.
```

Do not switch authority implicitly inside a blend. If an action changes authority, make acquisition,
handoff, and release explicit and prove them at every interruption point.

## Keep event semantics safe

Use clip markers for presentation facts whose timing belongs to the motion: footsteps, cloth, trails,
particles, camera accents, and synchronization landmarks. Treat marker delivery as a presentation
stream that may be filtered, blended, skipped by a seek, repeated after a correction, or suppressed
at an LOD unless the active engine proves otherwise.

Commit durable gameplay facts—damage, item transfer, resource use, cooldown, spawn, objective state—
through the authoritative action timeline. Animation may consume that committed fact or align a
presentation marker with its named phase; it must not be the only owner. Make presentation events
idempotent or give them occurrence identity when replay, seek, rollback, or correction can redeliver
them.

For a gameplay event that must visually coincide with contact, define the action phases and timing in
semantic data shared by gameplay and animation. Do not scatter duplicate “about frame 7” constants
through code and content.

## Handle interpolation, direction, and isometric views

Interpolate visual transforms between coherent previous/current simulation snapshots on the
presentation clock. Do not feed the interpolated pose back into simulation. Mark teleports, spawns,
large corrections, attachment changes, and other discontinuities so interpolation snaps or uses a
declared transition instead of crossing invalid space.

For 2D and isometric actors:

1. Keep facing in world or model space as authoritative semantic data.
2. Convert world facing into view facing through the active view rotation.
3. Quantize or blend into an authored view-direction family with explicit boundary and idle-facing
   rules.
4. Select the clip variant, then place every frame from the same world contact footpoint.
5. Derive depth from the support/contact contract, not a changing bitmap center.

Mirror a direction only when asymmetry, handed actions, text, equipment, lighting, sockets, and
silhouette remain correct. Rotation must remap facing, attachments, directional effects, selection,
and animation together; rotating only the sprite creates a visually plausible but semantically wrong
actor.

## Prove transitions through the shipped path

Validate imported/packed assets and the actual runtime graph, not only source previews:

- enumerate every state and transition; prove reachability, priority, fallback, reset/resume, and no
  unintended dead end;
- interrupt one-shots near start, middle, marker boundaries, and end with every higher-priority state;
- sweep zero, threshold, typical, and maximum speed/direction inputs through blends and sync groups;
- verify root or base stability, root-delta application, foot sliding, socket alignment, union bounds,
  masks, and additive reference poses;
- exercise pause, slow/fast time, variable render rate, dropped frames, seek, replay, save/resume,
  correction, and teleport according to the declared product contract;
- rotate through every isometric orientation and direction boundary with asymmetric equipment and
  attachments;
- force missing clips, missing directions, incompatible rigs, reduced LOD, and substitute assets;
- trace semantic state, graph state, normalized phase, blend weights, active layers, selected clip,
  consumed root delta, and emitted presentation events in a debug view; and
- inspect the live target at gameplay scale. A graph screenshot or import success is not proof of
  movement, contact, interruption, or visual correctness.

Deliver the authority map, semantic parameter/action schema, clip contracts, graph and transition
table, layer/mask ownership, movement-authority policy, event rules, 2D/isometric mapping, import
validation, proof matrix, and unresolved engine or content limits. Read
[the source map](references/sources.md) when auditing or changing these rules.
