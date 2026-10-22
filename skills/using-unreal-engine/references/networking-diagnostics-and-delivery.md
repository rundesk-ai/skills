# Networking, diagnostics, and delivery

Use this reference when work crosses a network boundary, needs engine-specific diagnosis or profiling,
changes a build target/configuration, or must run from cooked or packaged content.

## Design network behavior from authority

For each networked action, write down:

- the authoritative machine;
- the owning connection and which machine can initiate it;
- validation and rejection behavior;
- replicated durable state and its client reaction;
- transient cosmetic events;
- late-join reconstruction behavior;
- frequency, payload, relevance, dormancy, and failure expectations.

Prefer server-authored replicated state for facts that must converge. Use RepNotify to react on clients.
Use RPCs for directional bounded events; they have no return value and require compatible Actor ownership.
Do not send a reliable RPC every frame or for high-frequency cosmetic state. Do not trust parameters merely
because Unreal delivered them to a Server RPC.

Do not depend on ordering among RepNotify callbacks for coupled values. Group coupled state into one
replicated struct or reconcile it explicitly after updates.

The GameMode instance exists only on the server. GameState contains match-wide state clients need.
PlayerState contains per-participant state that other machines need. A PlayerController exists on the server
and its owning client, not on every client for every remote player.

## Treat replication architecture as version-sensitive

- Start with the repository's selected replication system. Do not enable Iris or Replication Graph as a
  local optimization.
- Confirm feature maturity in the installed engine's release notes and headers. Documentation pages may
  retain warnings that differ from the pinned release notes.
- Measure actor counts, connections, update frequency, bandwidth, server CPU, relevance, and dormancy before
  changing replication architecture.
- When migrating, audit custom serialization, subobjects, fast arrays, filters, prioritization, dormancy,
  replay support, and platform behavior.

## Match the diagnostic tool to the question

| Question | Evidence |
|---|---|
| What happened and in what order? | Dedicated `UE_LOG` category with intentional verbosity and stable IDs |
| Where was an Actor and what spatial state changed? | Visual Logger capture |
| Which broad subsystem is consuming a frame? | Stat commands for quick triage in a representative run |
| Which thread, scope, load, allocation, or frame consumed time? | Unreal Insights trace and a repeatable workload |
| Does a pure rule fail without engine state? | Engine-free unit test using the repository's C++ test stack |
| Does engine integration behave? | Automation test with an explicit product filter |
| Does a real session boot or survive multiple processes/devices? | Gauntlet or the repository's packaged-session harness |

Keep diagnostic output bounded. Remove temporary logs and debug drawing, but keep durable assertions,
metrics, or focused logging that are part of the accepted operability contract.

## Verify the target players will run

- Select the target type and configuration intentionally. Editor, Game, Client, Server, Program,
  Development, Test, and Shipping prove different things.
- Treat Build, Cook, Stage, Package, Deploy, and Run as distinct failure boundaries.
- Run the smallest relevant compile/test loop first, then the repository's full required gate.
- When asset discovery, configuration, platform code, loading, networking, startup, or shutdown changed,
  verify the relevant cooked or packaged target. Do not infer it from PIE.
- Exercise a clean start without warmed editor state. Preserve symbols and logs according to the build's
  diagnostic and distribution policy.
- Verify target SDK/plugin requirements before calling a packaging failure a source defect.
- Keep plugin module types and loading phases aligned with runtime/editor use.
- Convert an engine upgrade on a copy, then verify compilation, serialized assets, cooking, tests, and
  representative runtime behavior before accepting the version.
