# Widget architecture and lifecycle

Use this reference when deciding who creates a HUD or menu, how screens are layered, what belongs in
C++ versus a Widget Blueprint, or where subscriptions begin and end.

## Separate state, screen, and presentation

| Responsibility | Owner |
|---|---|
| Authoritative gameplay mutation | Gameplay/simulation command boundary |
| Player-specific UI coordination | LocalPlayer or owning PlayerController service |
| Snapshot-to-view translation | Typed C++ adapter or view model |
| Screen stack, modal policy, and focus restoration | One player-owned UI root/layer manager |
| Layout, styles, animation, and named child assembly | Widget Blueprint |
| Reusable low-level runtime control | `UUserWidget` or, only when needed, Slate widget |

Do not let a widget discover arbitrary world state, own persistent gameplay truth, or locate unrelated
singletons. Pass a bounded model or stable identifier, then emit semantic actions outward.

## Own each screen explicitly

- Create player-facing widgets with the intended owning LocalPlayer/PlayerController. Avoid an implicit
  first-player lookup; it breaks split-screen, local multiplayer, replay, and some test contexts.
- Use `AddToPlayerScreen` for UI scoped to one local player's screen. Use a full viewport root only for
  deliberate application-wide UI.
- Prefer one root per local player with named layers such as HUD, menu, modal, notification, and loading.
  A numeric Z-order scattered through callers is not a screen architecture.
- Keep non-interactive HUD elements hit-test invisible. Hidden decorative widgets must not intercept input.
- Decide whether closing means hide, deactivate, remove, or destroy. Reuse only when retained state and
  memory are intentional; otherwise recreate from authoritative view data.

## Match work to the widget lifecycle

| Hook/state | Use | Guard against |
|---|---|---|
| `NativeOnInitialized` | One-time setup for a non-template widget instance | Assuming named children exist before binding is valid |
| `NativePreConstruct` | Preview-safe cosmetic defaults | World access or gameplay side effects in designer preview |
| `NativeConstruct` | Repeatable attachment, subscriptions, and current-state refresh | Duplicate bindings when re-added |
| `NativeDestruct` | Matching unsubscription, timers, animations, and input cleanup | Assuming the UObject is being destroyed |
| Activation/deactivation | Screen participation and input routing | Treating construct/destruct as activation when widgets are retained |

Always render current state after subscribing so an update cannot be missed between model capture and
binding. Bind and unbind symmetrically; store delegate handles when the publisher outlives the widget.
Cancel async completions or validate widget/owner lifetime before applying their result.

## Model screens as explicit states

For every screen, enumerate loading, ready, empty, disabled, error, confirmation, and closed states that
can occur. Make one state transition own visibility, enabled state, focus, animation, and input policy.
Do not accumulate independent booleans that allow impossible combinations.

For lists, use stable item identity and update only changed entries. Do not key selection to array position
when sorting/filtering can move an item. If list virtualization or pooling is used, reset every visual and
interaction field on reuse.

## Keep Blueprint extension narrow

- Bind only required named children. Treat a missing required binding as an authored-content validation failure.
- Use `BindWidget` only when a named Designer child is required by the native contract. Use
  `BindWidgetOptional` only for a deliberate visual variant; native behavior must remain valid without it.
- Expose read-only data and semantic methods. Do not expose mutable internal widgets as a general API.
- Let Blueprint implement visual composition and bounded animations; keep screen policy and command dispatch
  testable in C++.
- Avoid Level Blueprint or Pawn ownership for application menus merely because a tutorial demonstrates it.
  Select the owner by lifetime and local-player scope.
