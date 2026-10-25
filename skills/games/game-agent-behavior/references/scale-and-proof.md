# Scale and proof

Read this when agent decisions cost too much, when the population must grow, or when writing the tests
that prove behaviour holds at scale.

## Counters, per tick and per system

- Decisions made, and the backlog of dirty agents still waiting.
- Milliseconds thinking against milliseconds executing.
- Candidate targets considered per decision; reachability and path queries per decision.
- Claim queries and the size of the claim table.
- Replans per minute; job switches per agent-hour, from the trace.
- Age of the oldest open job per tier.
- Maximum decision latency for agents in a lethal band.

At 60 frames per second the whole frame is 16.7 ms, and decisions share it with everything else.

## What sources report, for scale rather than as targets

| Source | Figure |
|---|---|
| Halo 2 | AI ran at 30 Hz or more; about 115 behaviours and 30 character types; behaviour storage estimated as 100 actors × 64 bytes × 4 layers |
| Dwarf Fortress | job assignment every 100 ticks, job applications every 100 ticks staggered from it; creatures decide and advance immediate actions every tick |
| Project Highrise | 1,000 NPCs at 60 FPS on desktop; one script is about a dozen actions covering about an hour of game time |
| LOD Trader | 57 µs per frame to control 8 features for hundreds of characters; 48 bytes per entity |
| Practical goal planning | under one plan per second per NPC on average; plans of at most four actions; at most several ms |
| Dragon Age: Inquisition | 10–20 behaviour snippets per character on average, over 50 for the most complex |
| Guild Wars 2: Heart of Thorns | over 100 reusable behaviour patterns, with the expensive raycast consideration ordered last |

## Order to try optimisations

1. **Think less often.** Decide when the queue empties or an event fires, not every tick; commit to
   actions once started.
2. **Stagger and budget.** Hashed phases, decisions counted per tick, a rotating start.
3. **Sleep timers.** Move need thresholds, cooldowns and schedule changes into a min-heap of wake ticks.
   Time-slicing removes spikes but does not lower the average.
4. **Shrink candidates before scoring.** Bit-mask tag filters, per-region or spatial-index candidate
   lists instead of world scans, and reachability by component id before any path query.
5. **Early-out inside scoring.** Cheapest considerations first, veto at zero, "cannot win" bound.
6. **Share across agents.** Tree structure shared with per-agent task state; utility computed in a
   separate load-balanced pass; plans cached by world-state bit mask, since few distinct plans tend to
   occur.
7. **Data layout.** Keep hot decision inputs (needs, current job, next think tick) in dense arrays,
   apart from cold data.
8. **Budget-driven fidelity.** Choose each agent's decision frequency against a budget rather than a
   fixed distance, and never change outcomes. A distance threshold cannot respect a budget when
   crowding varies.
9. **Parallelise last.** Score over read-only inputs in parallel, then resolve claims through the
   coordinator in stable id order.

## Proof fixtures

- Write headless tests that wait until a condition holds within N ticks, and fail on timeout. Two agents
  reproduce most behaviour bugs.
- Fuzz interruptions: kill, draft or interrupt agents at random ticks and steps. Then assert that no claim
  is held by a dead agent or for a stale job, and that no agent holds an item from an aborted action.
- Run a maximum-population soak at maximum time speed. Assert no deaths beside reachable unclaimed
  sources, a bounded oldest-job age, bounded decision latency in lethal bands, and a flat
  decisions-per-tick histogram.
- For probabilistic behaviour, assert over many independent seeds rather than one. About four times as
  many runs halves a confidence interval.
- Run determinism checks with one seed while varying iteration order, camera position and thread
  count, and compare per-tick hashes of positions, job boards and claim tables.
