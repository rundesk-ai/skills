# Engineering world simulations source map

Use this file to audit a rule, not as more procedure. The rules rest on public game-engine accounts,
maintainer implementation records, engine documentation, and scoped research.

## World decomposition and causal state

- Electronic Arts, [Insider's Look at SimCity's New Simulation Engine](https://www.ea.com/en-ca/news/insiders-look-at-simcity-new-simulation-engine)
  (2012), introduces GlassBox in terms of resources, units, maps, agents, and economic, water, and
  fire scenarios under its “what you see is what we sim” framing. This is a first-party preview of
  one game, not evidence that every visible thing needs an individual agent.
- Guillaume Pierre,
  [We Built This City on Bits 'n Maps](https://gdcvault.com/play/1034401/We-Built-This-City-on)
  (GDC 2024), is a named-practitioner account of maps, networks and globals, agents, and
  building-to-building connections used for city systems including water, crime, fire, work shifts,
  and parking. It
  supports separating spatial fields, network/global concerns, and actors while making their
  connections explicit; its particular implementations are not a universal city-sim architecture.

The substrate/fields/objects/networks/stocks/agents table is an integration vocabulary.
The two sources establish that useful world simulations combine several representations; they do not
define this exact taxonomy or require a class hierarchy.

## Determinism, phases, and replay

- Erin Catto, Box2D,
  [Determinism](https://box2d.org/posts/2024/08/determinism/) (2024), demonstrates that worker
  completion order can change result order even without a data race, describes worker-local bitsets
  merged into a deterministic sequence, distinguishes algorithmic, multithreaded, cross-platform,
  and rollback claims, and continuously tests state hashes. This supports canonical reduction,
  bounded reproducibility claims, and per-phase hash proof. It documents Box2D v3 techniques, not a
  guarantee for other engines or arbitrary floating-point simulations.
- Catto, [Replay](https://box2d.org/posts/2026/06/replay/) (2026), records an initial snapshot plus
  mutating operations and step arguments, validates transform/velocity hashes, and warns that engine
  determinism does not make application code deterministic. This supports recording authoritative
  inputs and finding the first divergent state; its snapshot format and handle implementation are
  Box2D-specific.
- Rseding, Factorio,
  [Friday Facts 415: Fix, Improve, Optimize](https://www.factorio.com/blog/post/fff-415) (2024),
  traces a map-generation desync to worker-count-dependent chunk results and separately describes
  pacing a potentially expensive task search across updates. This is shipped-system failure evidence
  for controlling partition-dependent results and declaring bounded work cadence, not a prescription
  for one tick budget or scheduler.
- Robert Nystrom, [Dirty Flag](https://gameprogrammingpatterns.com/dirty-flag.html), distinguishes
  primary from derived data and defers recomputation until a controlled point. It is
  practitioner explanation, not an engine contract. The rules combine it with explicit system
  dependencies and generation publication so readers cannot observe half-updated derived state.

The keyed-random-stream, read-current/write-next, canonical-install, and structural-commit rules are
conservative conclusions from these ordering failures. No source claims that one storage,
floating-point, thread, or RNG design satisfies every reproducibility envelope.

## Fidelity and bounded simulation

- Brogan and Hodgins,
  [Simulation Level of Detail for Multiagent Control](https://publications.ri.cmu.edu/simulation-level-of-detail-for-multiagent-control)
  (AAMAS 2002), evaluates simplified dynamic character models as an interface for navigation control
  across physically simulated agents. It establishes simulation fidelity as a selectable contract,
  but its bicyclist path-following and herding experiments do not establish aggregate population
  models or the hybrid promotion policy in this skill.
- Factorio,
  [Friday Facts 374: Smarter robots](https://www.factorio.com/blog/post/fff-374) (2023), is a
  maintainer account of changing robot task assignment from repeated nearest-idle selection to queued
  work and estimated completion time. It supports treating identity, commitments, task queues, and
  approximations as explicit semantic choices. It does not show that individual robots or its
  heuristic are right for another game.

Aggregate, agent, and hybrid fidelity are alternatives, not a quality ranking. The
requirements to preserve conserved totals, history policy, commitments, and seeded identity across
promotion are safeguards; empirical player value still belongs to game design and playtest.

## Invalidation, snapshots, and proof

- Godot stable,
  [TileMapLayer](https://docs.godotengine.org/en/stable/classes/class_tilemaplayer.html), documents
  batched internal updates, modified-cell update sets, and costly runtime tile updates. Unity 6's
  [Tilemap Collider 2D reference](https://docs.unity3d.com/6000.0/Documentation/Manual/tilemaps/work-with-tilemaps/tilemap-collider-2d-reference.html)
  documents a threshold that changes from accumulated incremental collision updates to a full
  regeneration. These concrete engine contracts support keeping both local and full paths and
  measuring their crossover; the same evidence rule applies to semantic world data.
- Factorio,
  [Friday Facts 150: New Terrain Experiments](https://www.factorio.com/blog/post/fff-150) (2016),
  describes a synchronized prepare stage that collects draw-ready data before rendering proceeds in
  parallel with later game update. It corroborates publishing a coherent presentation generation,
  but its renderer synchronization and stored data are Factorio-specific.

Full-versus-incremental equality, revisioned publish boundaries, semantic snapshots, causal reason
codes, and the final proof matrix are conclusions that integrate these sources with the gameplay
runtime's loop, replay, and save contracts. Valid benchmark and optimization claims need a performance
method of their own.

## Good/bad pair mapping

- **One stock owner:** EA's resources/units framing and Pierre's connected simulation techniques
  establish semantic simulation state; Catto's replay account shows why mutating operations need a
  recordable authoritative boundary. The stock-ledger pair applies those contracts and rejects a
  presentation callback as a second owner.
- **Hybrid fidelity:** Brogan and Hodgins establish selectable simulation fidelity, while Factorio's
  robot account shows that individual queues and commitments can matter. Preserving totals and
  commitments across promotion is a conservative safeguard; camera-triggered creation
  or consumption would violate the declared semantic model.
- **Field generations:** Catto and Factorio establish result-order determinism failures. Reading one
  committed generation, writing the next, and swapping once is a portable way to remove
  traversal order from a field pass; engines may use another method that proves the same property.
- **End-to-end agent proof:** Factorio's robot account establishes that queues, commitments, and
  approximate assignment can change behavior. Following intent through completion is a proof rule,
  not an empirical claim that visible agents improve every simulation.
