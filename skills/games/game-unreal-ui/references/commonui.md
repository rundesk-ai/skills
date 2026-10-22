# CommonUI

Load this reference only when CommonUI is already selected or its adoption is explicitly in scope.
CommonUI is useful for complex layered, cross-platform interfaces; it is not the default for every HUD.
Epic marks core CommonUI production-ready in UE 5.8. That does not remove its architectural adoption cost,
and the separate CommonUI/Enhanced Input integration remains documented as Experimental.

## Decide whether CommonUI earns its cost

Use it when several of these are required:

- keyboard, mouse, gamepad, and platform-specific input glyphs;
- layered screens with consistent activation/deactivation and Back handling;
- screen stacks or queues with focus restoration;
- platform-aware input routing and controller data; or
- a large interface needing reusable common buttons, tabs, and action presentation.

Prefer ordinary UMG plus one small player-owned coordinator for a passive HUD or a shallow, single-platform
menu. Do not use CommonUI for Widget Components placed in the world.

## Establish one routing authority

CommonUI routes input through the viewport and the active activatable-widget tree. Adopting it changes the
Game Viewport Client and input policy, so treat adoption as architecture and configuration work.

- Define one primary layout for each local player and a small fixed set of named layers.
- Make a widget activatable only when activation must affect input routing, focus, Back, or layer participation.
  Tooltips, decorative controls, and ordinary child widgets are not activatable screens.
- Give each activatable screen a desired focus target and complete input config.
- Push screens through their owning stack. Do not also add them directly to the viewport.
- Let the top screen deactivate/pop and reactivate the previous screen. Do not duplicate stack history elsewhere.
- If every screen deactivates, ensure the last transition restores a valid gameplay input config.

## Do not mix input-config owners

CommonUI input configs may set move/look suppression, mouse capture, cursor behavior, and overall input mode.
Avoid separate widgets or controllers calling the same standard setters while CommonUI owns them; the last call
wins and teardown can restore stale state.

Test mouse, keyboard-as-navigation, gamepad, device switching, initial focus, nested modal Back, closing the
last screen, and controller reconnect. CommonUI intentionally maintains one focus path; do not show pointer
hover and keyboard/gamepad focus as two simultaneous selections.

## Treat Enhanced Input integration as version-sensitive

CommonUI's Enhanced Input page carries older experimental cautions even in current documentation. Confirm the
installed version and sample behavior. Keep generic UI actions separate from gameplay actions, and add/remove
mapping contexts at the top-level policy rather than in many leaf widgets.

## Learn from Lyra without copying it whole

Lyra demonstrates a policy object, one layout per local player, named layer stacks, a passive gameplay HUD
layer, menu layers, and a modal layer. Reuse the structural lesson, not its full experience, game-feature,
messaging, online, or settings stack unless those systems are independently required.
