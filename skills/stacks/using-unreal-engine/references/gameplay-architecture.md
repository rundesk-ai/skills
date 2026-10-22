# Gameplay architecture and lifetimes

Use this reference when selecting an Unreal gameplay owner, composing Actors, introducing a service,
choosing tick or timers, or designing a C++/Blueprint boundary.

## Select by lifetime, authority, and representation

| Type | Lifetime and reach | Use it for | Avoid |
|---|---|---|---|
| `UGameInstance` | Process game session; survives map travel | Small coordination state that truly crosses worlds | A universal service locator or replicated state |
| `UWorldSubsystem` | One `UWorld` | World-scoped services and orchestration | Data that must survive world replacement |
| `UGameInstanceSubsystem` | One GameInstance | Cross-world runtime services | Per-player state or server-to-client state |
| `ULocalPlayerSubsystem` | One local player | Local input, viewport, preferences, player-facing services | Remote player or authoritative match state |
| `UEngineSubsystem` | Engine lifetime | Rare engine-wide integration | Ordinary game services |
| `UEditorSubsystem` | Editor lifetime | Editor workflows and tools | Runtime behavior |
| `AGameModeBase` | One world/match; server only | Rules, joining, spawning, win/loss flow | Client-readable match state |
| `AGameStateBase` | One world/match; replicated | Match state all clients need | Secret server rules or one player's private state |
| `APlayerState` | Participant; replicated broadly | Per-participant public match state | Local input/UI state |
| `APlayerController` | Server plus owning client | Possession, local input bridge, camera/HUD coordination | State every client must observe |
| `APawn` | Spawned physical agent | Possessable world representation | Persistent account/player identity |
| `UActorComponent` | Owning Actor | Reusable cohesive behavior | Unrelated global orchestration |
| Plain C++ value/service | Explicit owner | Deterministic rules and data with no engine facility need | Reflection, GC, Blueprint, editor, or replication needs |

Use the narrowest lifetime. Record how the owner is obtained and how tests replace or isolate it.
Do not cache a `UWorld*` or framework Actor across travel unless the documented lifetime proves it.

## Compose Actors deliberately

- Use `UActorComponent` for non-spatial behavior, `USceneComponent` when a transform is required, and
  `UPrimitiveComponent` only when rendering, collision, or another geometric primitive contract is needed.
- Create required default components in the Actor constructor with `CreateDefaultSubobject`. Create
  optional runtime components with an explicit outer, registration, attachment, ownership, and teardown plan.
- Avoid inheritance that exists only to share incidental implementation. Prefer a component when the
  behavior has a coherent Actor-owned lifecycle and more than one owner type needs it.
- Avoid an Actor when the concept has no world presence, transform, replication, ticking, or level lifetime.

## Keep the C++ and Blueprint seam semantic

- Put invariants, algorithms, authoritative mutations, and performance-sensitive loops in C++.
- Let Blueprint assemble components, choose assets, tune defaults, and express bounded content behavior.
- Expose actions such as `RequestPlacement` or `CanInteract`, not writable internals and long object chains.
- Use `BlueprintImplementableEvent` only for a required Blueprint-owned presentation hook. Use
  `BlueprintNativeEvent` when C++ supplies a valid default. Keep native implementation callable and tested.
- Prefer read-only exposure. If a value must change, route it through a function that validates the request.
- Give every exposed symbol a stable name, category, useful tooltip, and intentional edit/call scope.

## Schedule only necessary work

1. Prefer a direct call when one owner already controls order.
2. Prefer an event or delegate when another owner reacts to a state transition.
3. Prefer a timer for bounded delayed or periodic work.
4. Use tick only for genuinely per-frame work; disable it while idle.
5. If tick ordering matters, declare the tick group or prerequisite. Do not rely on incidental Actor order.

Delegates do not define authoritative multicast order. Check single-cast delegates before execution.
Store and remove handles when a longer-lived publisher can outlive the subscriber.

## Use Unreal text and assertions by contract

- Use `FName` for immutable names that are frequently compared, `FString` for mutable text processing,
  and `FText` for player-facing localized text. Never use display text as stable identity.
- Use `check` for impossible programmer errors when the expression has no required side effect. Use
  `verify` when the expression must still execute in builds where checks compile out. Use `ensure` for
  recoverable unexpected states that need diagnostics. Return normal errors for expected failure.
- Reflection metadata exists for editor tooling; runtime gameplay must not depend on reading metadata.
