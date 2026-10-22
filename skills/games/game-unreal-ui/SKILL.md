---
name: game-unreal-ui
description: Use when implementing, reviewing, debugging, or testing player-facing Unreal HUDs, overlays, menus, UMG or runtime Slate widgets, CommonUI, UI input and focus, responsive scaling, accessibility, or interface performance. It supplies a version-aware state-to-view and semantic-action routing workflow. Do not use for deciding what a HUD should show independent of Unreal, editor-only tooling, simulation rules, or web UI.
---

# Build game UI in Unreal

Make application and game state legible without letting widgets own it. UI reads a bounded snapshot
or view model and emits semantic actions through the boundary that owns each behavior.

For a new or reworked HUD system, read [HUD system architecture](references/hud-system-design.md)
first: layers per local player, one-way data flow, notifications and failure states.

## Define the interface contract

1. Read the repository rules, architecture, owning requirement, and current controller, camera,
   input, module, and plugin state.
2. Record the exact read-only view data, UI states, available actions, owning application or gameplay
   boundary, validation/result behavior, loading/empty/error/disabled states, input devices, target
   resolutions, localization, and accessibility semantics. Require a simulation command only when an
   action changes authoritative simulation state.
3. Identify the update owner, event lifetime, initial focus, Back/Escape behavior, modal behavior,
   focus restoration, local-player ownership, screen layers, and pause/time policy before building widgets.

Do not add UMG, CommonUI, MVVM, Slate Insights, or another plugin/module dependency without the
approval and module update required by the host repository.

## Choose the smallest Unreal UI stack

- Use **UMG** first for HUDs, selection panels, build menus, inventories, alerts, and overlays.
- Use **Slate** for a low-level custom runtime widget only when UMG cannot meet the named behavior or
  measured performance need.
- Consider **CommonUI** only for proven complex layered navigation or cross-platform input. Epic
  marks its core production-ready in UE 5.8, but specifically notes that a PC-only single-layer
  interface may not benefit from it.
- Do not adopt **UMG MVVM** as architecture by default. It is a Beta, plugin-gated facility in UE
  5.8; a small typed C++ view model and event-driven update is enough until evidence says otherwise.

CommonUI changes viewport and input routing. If approved, use activatable widgets only where
activation genuinely changes the input route. Its legacy Input Action Data Tables are not Enhanced
Input actions.

Read [widget architecture and lifecycle](references/architecture-and-lifecycle.md) before choosing
the screen owner, viewport path, widget lifetime, state model, or C++/Widget Blueprint seam.

## Hold the C++ and Widget Blueprint seam

| C++ owns | Widget Blueprint owns |
|---|---|
| Snapshot adapter and typed view data | Layout and visual composition |
| Command dispatch and validation result | Styling and presentation animation |
| Lifecycle, subscription, focus contract | Named widget assembly |
| Testable state translation | Tunable visual details |

Widgets never query mutable authoritative internals or change authoritative state directly.
Blueprint-facing properties are read-only. Expose explicit semantic actions to the owning gameplay,
session, settings, platform, or application boundary, and present rejection with a stable reason and recovery.

Use `NativeOnInitialized` for one-time instance setup. Treat `NativeConstruct` and `NativeDestruct`
as repeatable Slate attachment hooks. Pooled or re-added widgets can enter and leave the hierarchy
more than once, so subscriptions, timers, animations, and cleanup must be idempotent.

Create player-facing screens with an explicit owning LocalPlayer/PlayerController. Prefer one
player-owned root/layer manager over unrelated systems adding competing viewport roots. Use
`AddToPlayerScreen` for per-player UI when split-screen or local multiplayer is possible.

## Update from events, not every frame

- Publish an immutable UI view model or bounded change set when a committed simulation snapshot
  changes.
- Coalesce many changes from one simulation tick into one UI update.
- Avoid widget Tick, raw UMG property bindings, and polling. Update only affected controls.
- Use invalidation for mostly static hierarchies after measuring. A Retainer Panel adds repaint and
  render-target memory cost; it is not the first optimization.
- Use Widget Reflector for hierarchy, focus, hit testing, clipping, and invalidation. Use Slate
  Insights only when approved and when a measured UI CPU problem needs it.
- Prefer layout panels that express flow. Use Canvas and Overlay only where overlap or anchored
  positioning is actually required; extra layers and deep hierarchies increase layout and draw cost.
- Use render transforms for transient visual effects, not permanent layout. Animate opacity or
  render transforms before properties that force layout, and honor the interface's reduced-motion policy.

Read [performance and testing](references/performance-and-testing.md) before changing invalidation,
volatility, Retainer Panels, pooling, animation strategy, or UI performance instrumentation.

## Make input and presentation resilient

- Choose Game Only, Game and UI, or UI Only for each interface state; preserve the camera's cursor
  and capture contract.
- Apply input mode, cursor visibility, mouse capture, movement/look suppression, mapping contexts,
  focus target, and pause state as one reversible transition. Closing a screen restores the prior
  valid state even after rejection, travel, controller loss, or forced teardown.
- Keep gameplay and UI mapping contexts distinct and prioritized. Define keyboard, pointer, and
  gamepad navigation, initial focus, focus restoration, device switching, and Back/Escape.
- Use `FText` for user-facing text. Test long and localized text, DPI curves, anchors, clipping,
  safe zones, narrow/wide aspect ratios, and UI scale.
- Format numbers, dates, times, plurals, and currencies through culture-aware `FText` APIs. Do not
  concatenate sentence fragments or convert display text through `FString` and lose text history.
- Critical meaning cannot rely on color, hover, sound, or animation alone. Keep focus visible and
  navigation complete without a mouse.
- Screen-reader support is experimental and platform-limited in Epic's 5.8 documentation; implement
  useful labels where supported and still test focus, text scale, contrast, and redundant cues.

Read [layout, input, and accessibility](references/layout-input-and-accessibility.md) for anchors,
DPI, safe zones, text, fonts, navigation, focus, input modes, and device coverage. Read
[CommonUI](references/commonui.md) only when CommonUI is already selected or its adoption is in scope.
Read [world-space and specialized UI](references/world-space-and-specialized-ui.md) for Widget
Components, interaction components, drag-and-drop, or large sets of world indicators.

## Prove behavior and hand off visuals

1. Test state-to-view translation and semantic-action-to-result routing without pixels.
2. Add focused state/input tests for open, close, modal, focus, Back/Escape, rejected action, and
   device changes when those behaviors exist.
3. Run the repository's required build and focused test commands; confirm non-zero discovery and
   execution.
4. Use the UI-specific rendered screenshot path for screenshot comparison. The ordinary
   `TakeAutomationScreenshot` path excludes UI; NullRHI cannot prove pixels, clipping, contrast,
   animation, or focus visibility.
5. Inspect Widget Reflector focus, hit-test, clipping, and hierarchy evidence for interaction defects.
   Use Slate Insights for measured invalidation, tick, timer, or repaint problems.
6. Complete the repository's visual handoff at named resolutions, aspect ratios, cultures, UI scales,
   safe zones, and input devices.

Read [the UE 5.8 source map](references/sources.md) when choosing CommonUI, MVVM, input routing,
invalidation, localization, scaling, accessibility, or UI profiling behavior. Confirm version-sensitive
claims against the engine version declared by the host repository and its installed headers.
