# HUD system architecture

Use this reference when building or restructuring a complete player-facing HUD, screen hierarchy,
notification system, or the data flow connecting gameplay to UI. What the HUD should show, and how
prominently, is design work decided before this; this page is how Unreal carries it. Keep the smallest
architecture that meets the accepted behavior.

## Inventory surfaces before classes

Classify each requested element by how the player uses it:

| Surface | Purpose | Default behavior |
|---|---|---|
| Persistent HUD | Frequently needed state during play | Passive, compact, hit-test invisible |
| Contextual HUD | State relevant to the current selection, target, tool, or mode | Appears and clears with explicit context |
| Transient feedback | Acknowledgement, warning, gain/loss, damage, save, or objective change | Timed, deduplicated, priority-aware |
| World indicator | Relates screen information to a world location | Projected, clamped, pooled, occlusion-aware as required |
| Gameplay menu | Inventory, map, build, loadout, or another in-play workflow | Interactive; declares input and pause policy |
| Modal | Decision that blocks its owning layer | Top priority, one clear default/cancel path |
| Frontend/system screen | Startup, profile, settings, matchmaking, or fatal error | Own state machine independent of a world Actor |

## Use one policy per local player

A scalable pattern is one player-owned root that contains a small set of named layers. Adopt it only when
multiple independent screens need consistent ordering and Back behavior; [CommonUI](commonui.md) covers
the Lyra version of it and what not to copy.

Typical layer policy:

```text
system/fatal overlay
  modal and confirmation
    frontend or full-screen menu
      gameplay menu
        contextual UI and notifications
          passive HUD
```

- A layer owns ordering, activation, input policy, and focus restoration for its children.
- Callers request a semantic screen or message; they do not choose arbitrary Z-order values.
- Use a stack when the player drills into screens and Back returns to the previous screen.
- Use a queue for messages that must appear one at a time. Use replacement or aggregation for frequent
  status updates; a queue that grows faster than it drains is a defect.
- A modal blocks only the intended layers. Fatal/system UI has a separate escape path from ordinary menus.
- `AHUD` can coordinate UI for its local PlayerController, but UMG does not require it. A LocalPlayer-scoped
  manager is often clearer when UI must survive Pawn changes or no world exists.

## Make data flow one-way and observable

```text
authoritative application or gameplay state
  -> immutable UI snapshot or typed presentation model
  -> presenter/view-model translation
  -> widget state
  -> semantic player action
  -> validated request at the owning boundary
  -> accepted/rejected result
  -> next authoritative snapshot
```

- Keep presentation-model lifetime separate from widget lifetime. Several widgets may render one model,
  and one widget may be reused for several models.
- Translate raw gameplay values into player-facing state before the widget: label, formatted value, icon ID,
  enabled state, reason text, severity, sort key, and available actions.
- Subscribe to committed changes and apply bounded updates. After binding, immediately render the current
  model to close the subscribe-versus-snapshot race.
- Do not optimistically mutate authoritative display state unless the behavior explicitly defines prediction
  and rollback. Show pending state, then reconcile accepted or rejected results.
- Use stable semantic identifiers for selection and list items. A widget pointer or array index is not identity.
- Log or trace screen transitions and rejected actions at the coordinator boundary, not in every visual child.

## Design notifications as a bounded system

A reusable notification record usually needs: category, stable deduplication key, severity, localized text
or format data, optional icon, creation time, expiry policy, count, source/target identity, available action,
and whether acknowledgement is required.

The arbiter decides:

1. whether to suppress, merge, replace, enqueue, or interrupt;
2. which layer and region owns the message;
3. how long it remains and whether time pauses with gameplay;
4. what happens when the region is full;
5. how screen-reader/audio feedback is rate-limited; and
6. whether the event belongs in a persistent history.

Use a typed arbiter only when several producers need shared priority/deduplication policy. A single bounded
message does not justify a global message bus.

## Scale world indicators separately

Do not give every marker its own Widget Component. Read
[world-space and specialized UI](world-space-and-specialized-ui.md) for the screen-space indicator layer
and what each indicator must define.

## Make failure states first-class

Design these before the happy path is complete:

- no owning local player or controller not yet paired;
- gameplay world absent, loading, traveling, or shutting down;
- model not ready, stale, empty, or permission-restricted;
- command pending, rejected, timed out, or superseded;
- input device disconnected or active input method changed;
- focus target removed while a modal or list changes;
- network disconnect, privilege loss, or save/load failure; and
- unsupported culture glyph, missing asset, or async image load failure.

Every failure has a stable recovery: retry, cancel, go back, choose another item, reconnect, return to a safe
screen, or display a non-interactive terminal state. Never leave the player in UI Only input with no focusable
control or escape action.

## Review the system, not only individual widgets

Verify:

- one root and coherent layer order per local player;
- no competing input-config owners;
- every interactive screen has initial focus, Back, and restoration;
- every widget subscription has matching cleanup;
- authoritative data is never owned by a visual widget;
- notifications are bounded under burst load;
- world indicators remain bounded at worst-case entity counts;
- empty/loading/error/rejected states are renderable;
- all supported devices, cultures, scales, safe zones, and aspect ratios are exercised; and
- UI CPU, GPU, draw calls, texture/render-target memory, and live widget count meet a measured budget.
