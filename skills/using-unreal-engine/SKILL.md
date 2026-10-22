---
name: using-unreal-engine
description: Use when writing, reviewing, debugging, building, testing, profiling, or packaging Unreal Engine code or tooling, including C++, gameplay framework ownership, modules and plugins, UBT/UHT, reflection, UObject and Actor lifetime, Blueprint APIs, assets and mesh import from Blender, glTF or FBX, configuration, saves, replication, editor tooling, and Automation tests. It supplies version-aware engine boundaries while preserving any declared engine-free domain layer. Do not use for plain C++ with no Unreal boundary.
---

# Use Unreal Engine

Respect the host project's architecture. Keep engine objects out of any declared engine-free domain
layer, and make presentation, input, editor tooling, and persistence boundaries explicit.

## Ground the change

Before choosing an Unreal type or API:

1. Read the repository rules, architecture, build instructions, terminology, and owning requirement.
2. Confirm the declared and installed engine version. Inspect the affected `.uproject`, `.uplugin`,
   `.Target.cs`, `.Build.cs`, module, nearby tests, configuration, and enabled plugin state.
   UnrealBuildTool is the build graph; generated IDE files are not.
3. State the behavior, module boundary, runtime authority, lifetime owner, thread, data or asset
   compatibility impact, and proof before editing.

Never enable a plugin, add a dependency, or change the engine version without the approval required
by the host repository.

## Put work in the owning layer

| Concern | Owner | Boundary |
|---|---|---|
| Declared engine-free domain rules | Project domain/simulation module | Plain deterministic C++; permitted base modules only |
| Snapshot presentation and input commands | Runtime game module | Unreal-facing adapter |
| Import, generation, validation, commandlets | Editor module | Editor target only |
| Engine-free proof | Domain/simulation tests | No Actor or UObject needed |
| Presentation proof | Runtime adapter tests | Exercise the adapter, not domain rules through an Actor |

Do not scaffold a future module or engine abstraction. Add the smallest owner needed by the current
accepted behavior.

## Choose the narrowest correct engine owner

Do not use an Actor, global singleton, or GameInstance merely because it is easy to reach.

| Need | Default owner |
|---|---|
| Rules for a running match | `AGameModeBase`; server only in network play |
| Replicated match-wide state | `AGameStateBase` |
| Per-participant replicated state | `APlayerState` |
| Human input, possession, camera, local viewport | `APlayerController` or `ULocalPlayerSubsystem` |
| Physical controllable presence | `APawn`, or `ACharacter` only when its movement stack fits |
| Reusable behavior owned by one Actor | `UActorComponent`; add a transform only when spatial behavior needs one |
| Service with an engine-managed lifetime | The narrowest matching World, GameInstance, LocalPlayer, Engine, or Editor subsystem |
| Designer-authored definitions | `UDataAsset`; use primary assets only when identity, discovery, bundles, or explicit load control are needed |
| Cross-session player data | A versioned `USaveGame` schema, not a live Actor graph |

Read [gameplay architecture and lifetimes](references/gameplay-architecture.md) before adding a
framework class, subsystem, component, tick, timer, or Blueprint seam.

## Keep the module graph honest

- Prefer private dependencies. Make a dependency public only when a public header exposes its type.
- Keep editor-only modules, headers, and code out of the Game target.
- Follow include-what-you-use: each header includes what it needs, the matching header is first in a
  `.cpp`, and monolithic engine headers do not hide dependencies.
- Treat the repository's normal full build as the UBT/UHT/compile/link proof. A successful IDE parse
  or Live Coding patch is not that proof.
- Keep reflected API narrow. Add `UCLASS`, `USTRUCT`, `UFUNCTION`, or `UPROPERTY` only for a named
  reflection, GC, serialization, editor, or Blueprint need. Put `.generated.h` last.
- Use C++ for stable systems, complex logic, hot paths, and invariants; use Blueprint for composition,
  tuning, content-specific behavior, and fast iteration. Expose small semantic functions instead of
  internal storage or chains of engine objects.
- Prefer `BlueprintReadOnly`, `EditDefaultsOnly`, narrow categories, tooltips, and validated setters.
  Mutating authoritative state remains an explicit command. Do not expose a property as writable
  merely to make a graph compile.
- Treat public reflected names as serialized API. Renaming a reflected class, struct, enum, function,
  property, package, or asset may require a Core Redirect and a resave/validation pass.

## Make engine lifetime explicit

Choose standard C++ values for plain data. Use a UObject only when an engine facility requires it.

| Need | Default |
|---|---|
| Reflected strong UObject member | `UPROPERTY()` with `TObjectPtr<T>` |
| Optional non-owning live UObject | `TWeakObjectPtr<T>` |
| Unloadable asset reference | `TSoftObjectPtr<T>` or a soft object path |
| Shared ownership of plain non-UObject data | `TSharedPtr` only when lifetime is genuinely shared |

Never allocate a UObject with `new`, and never manage one with Unreal shared pointers. Use
`CreateDefaultSubobject` during construction or `NewObject` at runtime. Constructors set defaults and
create default subobjects; bind runtime state at the appropriate lifecycle hook. Make delegate
binding and cleanup idempotent, and release it in `EndPlay`, `Deinitialize`, or the matching owner
hook. Streaming unload and reconstruction are ordinary lifecycle paths.

Do not use multicast delegate order for simulation-affecting sequencing; its order is undefined.
Put authoritative phase order in the simulation contract.

## Prefer events and bounded work

- Start with events, delegates, timers, or explicit orchestration. Enable Actor or Component tick only
  for work that truly varies every frame; disable it when idle and select tick group/prerequisites
  intentionally when order matters.
- Store delegate handles when removal is required. Match binding style to lifetime: UObject-aware
  bindings for UObjects; raw bindings only when external lifetime is proved.
- Use subsystems for services whose required lifetime exactly matches the subsystem. A subsystem is
  not a license for hidden global state or a dependency locator.
- Use components for cohesive behavior owned by an Actor. Do not split every method into a component,
  and do not let a component silently become the authority for unrelated systems.
- Keep construction idempotent. Expect Blueprint recompilation, construction-script reruns, PIE
  teardown, seamless travel, streaming unload, and editor transactions to exercise paths that a
  one-shot standalone run does not.

## Cross threads and assets deliberately

- Worker tasks consume immutable or copied plain data and return plain results.
- Touch Actor, UObject, UI, and ordinary engine state on the game thread unless the specific API
  explicitly documents another contract.
- Every async completion has cancellation and an owner-lifetime check. Completion order cannot
  change deterministic simulation results.
- Prefer soft references when eager loading is not required. Retain the streamable handle or another
  strong reference for assets that must remain loaded.
- Treat Live Coding object reinstancing as invalidation: rebuild cached object pointers and verify a
  full build before completion.

## Treat assets, settings, and saves as contracts

- Prefer stable identifiers and soft references across persistence, streaming, and optional content
  boundaries. Avoid synchronous loads hidden in constructors, getters, UI paint, or per-frame paths.
- Use the Asset Manager when content needs explicit identity, discovery, auditing, bundles, cook
  rules, or load/unload control. Do not introduce a custom Asset Manager for ordinary references.
- Put checked-in defaults in the appropriate `Default*.ini`; put platform overrides in platform
  configuration. Never treat generated `Saved/Config` output as the source of truth.
- Separate authored definitions, runtime state, and saved state. Give saved data an explicit schema
  version and migration path; validate corrupted, missing, older, and newer data without partially
  mutating the live world.
- Move or rename assets through Unreal-aware tooling, fix redirectors, and validate unloaded
  referencers. Use Core Redirects for reflected code renames that existing serialized assets depend on.

Read [assets, configuration, and persistence](references/assets-config-and-persistence.md) before
changing an asset-loading policy, primary asset identity, configuration hierarchy, serialized name,
or save format. Read [Blender handoff](references/blender-handoff.md) when importing authored meshes
into Unreal, or when a mesh arrives mirrored, inside out, at the wrong scale or facing the wrong way.

## Preserve authority in networked code

If networking is in scope, define who owns the Actor, which machine may initiate the action, which
machine validates it, and which state must converge before writing code.

- The server owns authoritative gameplay state. A client request is untrusted input, including when
  it arrives through a Server RPC.
- Replicate durable state with properties; use RepNotify for client reactions. Use RPCs for bounded
  events, not as a replacement for state synchronization or a return-value call.
- Check Actor ownership and owning connection before selecting an RPC direction. Keep reliable RPCs
  infrequent and necessary; a reliable stream can delay later traffic.
- Test dedicated server, listen server, owning client, simulated proxy, late join, disconnect, and
  packet impairment paths that the behavior can reach. A single-process PIE result is not sufficient
  network proof.
- Do not opt into Iris, Replication Graph, or another replication architecture incidentally. Verify
  the installed engine's maturity and migration contract, then obtain the approval required by the
  repository.

Read [networking, diagnostics, and delivery](references/networking-diagnostics-and-delivery.md) for
replication, logs, Insights, build configurations, cooking, packaging, and session tests.

## Choose Unreal evidence

- Use a dedicated log category with intentional verbosity and stable identity in each line.
- Use Visual Logger for spatial gameplay history and Unreal Insights for traced timing, memory and
  loading.
- Measure performance on a non-Debug, cooked build: editor overhead, uncooked assets and warm caches
  invalidate a conclusion drawn in the editor.

## Prove the boundary

Use the repository's own build and test commands when it has them. Otherwise, from the engine root:

```sh
# Build (Build.bat on Windows; the Linux script lives under BatchFiles/Linux)
Engine/Build/BatchFiles/Mac/Build.sh <Project>Editor Mac Development -Project="$PWD/<Project>.uproject" -WaitMutex

# Run one Automation filter headless and quit
UnrealEditor-Cmd "$PWD/<Project>.uproject" -ExecCmds="Automation RunTests <Filter>;Quit" \
  -unattended -nopause -nullrhi -nosplash -log
```

1. Run the smallest affected Automation filter and confirm in the log that it discovered and ran at
   least one test; a filter that matches nothing still exits cleanly.
2. Run the repository's required build and test commands.
3. For an engine-free module, search its dependency and include surface for prohibited engine,
   UObject, Actor, Component, and asset types; expect none.
4. Inspect the Game and Editor target/module direction after every dependency change.
5. When assets, loading, configuration, networking, or platform behavior changed, run the applicable
   cook/package or target session. An Editor build proves neither cooked discovery nor Shipping behavior.
6. Validate serialized references and migrations after reflected or asset renames.
7. Remove temporary logs and instrumentation. Report any editor-only, device, network, or visual
   check honestly.

Read [the UE 5.8 source map](references/sources.md) when choosing or auditing an engine API. Prefer
the installed engine headers and release notes when an example or page conflicts with the pinned API.
