# World-space and specialized UI

Use this reference for Widget Components, simulated pointer interaction, drag-and-drop, projected markers,
or other UI that does not behave like an ordinary player-screen widget.

## Choose world space only when it communicates world attachment

Use a Widget Component for a bounded number of surfaces that must exist in 3D space, such as an in-world
terminal, VR panel, or diegetic display. Do not use it by default for every health bar, nameplate, resource,
or interaction marker.

Each Widget Component can create a widget and render target. Define draw size, space, pivot, redraw mode,
redraw interval, visibility, distance, collision, and ownership deliberately. At scale, measure render-target
memory, redraw work, overdraw, and live widget count.

For many markers, prefer one player-owned screen-space layer that accepts plain indicator descriptions,
projects world positions, culls and prioritizes them, resolves overlap, clamps to the safe zone, and pools
the visual entries. For each indicator define:

- actor/component/socket or stable world position source;
- on-screen, off-screen, behind-camera, distance, and occlusion behavior;
- viewport/safe-zone clamping and edge-arrow rules;
- overlap, clustering, priority, and maximum visible count;
- local-player and team visibility; and
- invalid-target cleanup during destruction, streaming, travel, and replay.

A marker never issues gameplay commands to its represented Actor. It emits a semantic selection or
interaction request through the owning player-action boundary.

## Keep interaction player-specific

Widget Interaction Components simulate Slate input. Give each virtual user and pointer a stable distinct
index when simultaneous users or hands exist. Define trace source, interaction distance, hit testing, pressed
keys, focus, capture, and cleanup. Do not let a world widget bypass the same gameplay command validation used
by screen UI.

CommonUI is not recommended for Widget Component interfaces because its routing depends on viewport paint,
focus, and activation order.

## Make drag-and-drop a transaction

- Keep the drag visual separate from authoritative item state.
- Carry stable source, payload identity, allowed operations, and originating local player.
- Validate the drop target and gameplay command at drop time; the world may have changed during the drag.
- On rejection, restore the source visual and explain why. On cancellation, controller loss, travel, or widget
  destruction, clear capture and transient state.
- Support keyboard/gamepad alternatives for every required drag operation; pointer drag alone is not complete.
