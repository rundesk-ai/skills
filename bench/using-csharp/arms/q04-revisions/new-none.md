# AGENTS

Rules for every agent working in this repository. Transit is a delivery simulation: vans run routes
between depots over track, and cars park at the kerb and cross the track at level crossings. The
simulation must replay exactly from a save, and the game layer must show what the simulation does.
Where this file conflicts with your general habits, this file wins.

## Before you work

Load light; pull depth only when the task needs it.

1. **Load every skill the work calls for — all of them, in one pass, before anything else.** An
   agent that has started editing has stopped loading. After a compaction, load them again.

   No skills are installed in this repository yet.
2. **Read the code map below**, then the files the task enters.
3. **Read a file before editing it; search before writing new logic** — reuse or extend what is
   already here rather than duplicating it. Scratch files stay outside the repository.
4. **Make the smallest complete change.** First list every place it must reach: callers, tests,
   the game layer, the snapshot. Then take the first option that fully works: does it need to exist;
   is it already here; does .NET do it; otherwise the least new code that reads at a glance. Add no
   abstraction, wrapper, option, config or "for later" code nobody asked for; keep the structure the
   code already has, and prefer deleting to adding. Touch nothing the task did not send you to —
   improvements are mentioned, not made. Be lazy about the solution, never about the change: finish
   every caller, test and doc it breaks, and delete the code, tests, assets and config it leaves
   unused; list anything already unused for the owner, since it may be kept on purpose. Never cut
   the determinism rules or a save's contents — and code you move or merge keeps its own.
5. **Do not contradict the owner without evidence.** Investigate, then answer with what you found.

## Hard rules

The first three need explicit approval. The rest are not negotiable.

- **Dependencies — ask first.** Adding, removing, or version-bumping a NuGet package.
- **Deletions — ask first.** Any file outside the task's immediate scope.
- **Commits — ask first.** Never commit or push unless told to.
- **Never break determinism.** A replay that drifts cannot be debugged. No wall clock, no unseeded
  random numbers, no enumeration order you did not choose.
- **Never put a simulation rule in `game/`.** The view then shows what the simulation does not do.
  The game calls the simulation's public API.

## Stack & architecture

| Layer | Owns | May depend on | Must not |
|---|---|---|---|
| `src/Transit.Sim` | every rule: driving, parking, vans, routes, trips | .NET only | reference `game/` or an engine |
| `game/` | drawing and tool input | `Transit.Sim` | compute a rule the simulation owns |
| `tests/Transit.Sim.Tests` | the simulation's behaviour | `Transit.Sim` | — |

## Build, test & run

```sh
dotnet build   # must pass with no warnings: warnings are errors
dotnet test    # the suite
```

**Who runs the app:** build to prove it compiles, then hand off — the owner runs the game and judges
it.

## Definition of done

Re-read this file and check each item below before calling the work done.

1. `dotnet test` passes — observed, not inferred.
2. Every rule here held.
3. New guaranteed behaviour is proven by a test seen failing without it.
4. The hand-off names what changed, what was deliberately left, and anything unused you noticed.
