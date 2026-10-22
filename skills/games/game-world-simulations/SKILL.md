---
name: game-world-simulations
description: Use when designing, implementing, reviewing, or debugging an engine-agnostic world simulation for a city builder, colony sim, management game, factory game, ecosystem, or other systemic world, including semantic state layers, fields, networks, stocks, agents, simulation fidelity, system cadences, deterministic phase order, local invalidation, snapshots, causal traces, or full-versus-incremental correctness. It supplies authority, phase, cadence, fidelity, and invalidation contracts inside the simulation tick, with full-versus-incremental proof. Do not use it for what a management game should simulate, tile storage and map edits, the host runtime loop or replay harness, pathfinding, rendering, engine APIs, or profiling methodology alone.
---

# Engineer world simulations

Model a world as authoritative semantic state plus explicit transformations. Make causes reproducible,
derived state rebuildable, and presentation an observer of committed facts.

## Establish the simulation contract

Record before selecting containers or systems:

- the player-visible questions the simulation must answer and deliberately omitted fidelity;
- the authoritative entities, stable identities, units, coordinate systems, clocks, and boundaries;
- every state layer, its owner, invariants, consumers, persistence, and whether it is primary or
  derived;
- the dependency graph, phase order, update cadence, mutation point, and randomness contract;
- the declared reproducibility envelope: same run, build, platform, worker count, or cross-platform;
- save, replay, migration, inspection, and explanation requirements; and
- maximum supported world shape, active populations, change patterns, and time speeds as workloads,
  leaving benchmark method and budget proof to performance work.

Treat unknown fidelity and cadence choices as hypotheses. Do not simulate a detail because it exists
in the real world; keep it when its state can change a supported decision, consequence, explanation,
or future system.

## Separate world concerns without disconnecting them

Use a small set of semantic categories to expose ownership and coupling. A world may need only some:

| Category | Meaning | Typical state |
|---|---|---|
| Substrate | Persistent spatial conditions | terrain, elevation, water, soil |
| Fields | Values distributed over space | pollution, heat, value, coverage |
| Objects | Stable placed or owned things | buildings, parcels, machines |
| Networks | Connectivity and flow topology | roads, pipes, power, relationships |
| Stocks | Conserved or capacity-bound quantities | money, food, energy, inventory |
| Agents | Individually identifiable actors | residents, vehicles, crews, animals |
| Rules and events | Policies and committed facts | taxes, schedules, incidents, completions |

This is a decomposition aid, not a required class hierarchy. Store one fact in one authoritative
home and make every other representation derived. Declare units, sign conventions, capacity,
conservation, and legal ranges at that home. A sprite, scene node, cached route, connection mask,
dashboard total, or animation state cannot become a second owner.

```text
Good: stock ledger commits delivery -> building inventory changes -> snapshot exposes the fact.
Bad:  truck arrival animation increments inventory while a logistics system also transfers it.
```

Draw a causal dependency graph before coding. Reject cycles that rely on accidental system order;
resolve intentional feedback with a previous/current buffer, a staged solver, or an explicit
within-tick iteration and convergence policy.

## Choose fidelity from observable consequences

Choose independently for each concern:

- **Aggregate:** retain counts, rates, distributions, or cohorts when individual history and
  position cannot affect supported decisions.
- **Agent:** retain identity, state, location, memory, and commitments when the player or another
  system must follow an individual consequence.
- **Hybrid:** keep authoritative aggregates plus a bounded set of materialized individuals, or
  aggregate inactive regions while preserving declared transition invariants.

Do not tie semantic fidelity to camera visibility. Moving the camera must not create money, erase
people, reroll outcomes, or change a reachable result. If fidelity changes by distance, activity, or
importance, define promotion and demotion explicitly: what history is retained, how identities are
assigned, which conserved totals remain equal, and which approximation error is accepted.

```text
Good: a distant cohort preserves population, needs distribution, commitments, and seeded promotion.
Bad:  off-screen citizens stop consuming resources, then respawn from current averages when viewed.
```

## Schedule world systems explicitly

Give every system a phase contract:

```text
SystemContract {
  reads, writes, cadence, ordering dependencies
  structural requests, random stream, emitted facts
  invalidation inputs, invariants, reference implementation
}
```

Default to reading a coherent committed state, writing private next-state or result buffers, and
installing changes at a named boundary. Order phases from causes to effects. Queue creation,
destruction, topology changes, and ownership transfers for a structural commit unless immediate
visibility is part of the declared phase contract.

Assign randomness by stable semantic stream or keyed decision, not one global consumption sequence.
Define stable iteration and tie rules. For parallel work, partition from committed inputs, write
worker-local results, and reduce or install them in a canonical order. A mutex can prevent a data
race without making arrival order reproducible.

Cadence is semantics, not only optimization. Declare whether a slower system samples, accumulates,
integrates, or consumes queued changes; define its first-fire phase and overload behavior. Never let
systems silently infer elapsed time from how often a callback happened.

```text
Good: each field pass reads generation N, writes N+1, then swaps once after all cells finish.
Bad:  cells read neighbors that may already contain this pass's result, so traversal order changes it.
```

## Make derived work local and auditable

For every mutation, classify each dependent result:

- same-location local;
- fixed-radius or declared read-set closure;
- connected-component or route-dependent;
- globally coupled; or
- periodic/background with a coherent publish boundary.

Emit one semantic change set at commit. Expand it through registered dependency footprints, union
duplicate work, compute from one coherent revision, and publish only a complete derived generation.
Keep a simple full recomputation path as the correctness oracle whenever an incremental path exists.
Switching between them may be a measured policy; their supported semantic result must agree.

Do not label an operation global merely because its first implementation scans the map. Conversely,
do not call a cache local when a network split, capacity change, or policy update can alter a remote
result. Record revision, source change, affected domain, rebuild mode, and fallback use so a stale
result can be traced.

## Expose meaning without leaking ownership

Publish coherent semantic snapshots at a committed boundary. Include stable identity and generation,
meaningful state, previous/current values needed by presentation, and explicit unknown or stale
status. Exclude mutable engine objects, texture or clip handles, transient pointers, and caches that
presentation could mistake for truth.

Maintain bounded causal traces for important outcomes:

```text
outcome -> committed rule/effect -> relevant inputs -> originating command or prior fact
```

Use stable reason codes plus contextual values; do not preserve every internal read as an unbounded
event log. The same semantic fact should feed UI, debug overlays, animation, telemetry, and player
explanation rather than each adapter guessing why it happened.

## Prove the model before scaling it

Build tiny deterministic fixtures that cross system boundaries, then add representative worlds:

- assert conservation, capacity, ranges, ownership uniqueness, topology, and lifecycle invariants at
  every commit where practical;
- replay the same seed and commands while varying render rate, worker count, partition order, and
  unrelated system presence inside the promised envelope; compare per-phase semantic hashes to find
  the first divergence;
- compare incremental, component-local, and full recomputation after sparse edits, batches, network
  splits/merges, border changes, and policy changes;
- run field passes in reversed traversal order and detect unintended in-place dependencies;
- promote and demote hybrid-fidelity regions repeatedly and verify conservation, identity policy,
  commitments, and accepted approximation bounds;
- follow representative agents or vehicles from intent through reservation, movement, interruption,
  completion, and committed effects; entity counts alone cannot prove causal behavior;
- save and reload at every structural phase boundary, then continue commands and compare state;
- inspect snapshots and causal traces for normal, delayed, rejected, starved, unreachable, and stale
  outcomes; and
- exercise minimum, typical, dense, adversarial, long-running, and maximum time-speed workloads,
  reporting counters while leaving performance conclusions to a profiling method of their own.

Deliver the semantic layer inventory, authority map, dependency graph, phase/cadence table, fidelity
policy, randomness and reproducibility envelope, invalidation footprints, snapshot and explanation
schemas, invariants, reference-versus-incremental evidence, and unresolved limits. Read
[the source map](references/sources.md) when auditing or changing these rules.
