---
name: game-pathfinding
description: Use when designing, implementing, tuning, reviewing, or debugging pathfinding or agent movement in a game or simulation, including grids, waypoint or road graphs, navmeshes, flow fields, A* and its heuristics, jump point search, hierarchical search, reachability, path repair after map edits, path request budgets, path following, local avoidance and crowds, or agents that get stuck, take strange routes, or stall the frame when many repath at once. It supplies search-space choice, a bounded A* proved against an oracle, request scheduling, edit repair, and determinism rules for thousands of agents. Do not use it for lane-level road traffic or for deciding where an agent wants to go.
---

# Engineer game pathfinding

Most pathfinding cost is not the algorithm. It is searches that should never have run, searches that
run all at once, and graphs with more nodes than the legal moves need. Fix those first; tune A* last.

## Write the workload down first

Before choosing an algorithm, record: map size; whether edits change **topology** (a wall) or only
**cost** (mud), and how often; agent count; how many distinct goals are live at once; tile-stepped or
continuous movement; and whether the simulation must replay or run in lockstep. Capture a trace of
real requests (start, goal, tick) from play and keep it as the benchmark input. Implementations of the
same algorithm have been measured 100× apart, so every later choice is judged against that trace, not
against intuition.

## Choose the smallest search space that expresses the legal moves

Search time is proportional to nodes expanded, and the representation decides the node count.

| World | Default | Deviate when |
|---|---|---|
| Tile sim whose tiles change often | Cell-as-node grid, neighbours by index offset, integer costs 10/14, no corner cutting | Long choice-free corridors: collapse them into segment edges between junctions |
| Road or rail network | Node = junction, edge = segment; search state = (node, entry direction) | Turn restrictions require the entry direction in the key |
| Continuous 3D surfaces | Navmesh polygons, A* over the corridor, funnel string-pulling | Routes are authored, not arbitrary: use authored lanes |
| Many agents, few shared goals | Flow field (Dijkstra map) per goal, tiled into sectors | Goals differ per agent: A* with a reachability check |
| Very large, mostly static map | Two-level hierarchy (clusters or sectors with portals) | The map mutates constantly: keep only reachability labels |
| Several floors | One graph; stairs and ramps are edges; lifts are queued edges | — |

Keep one graph or cost field per movement class (walker, swimmer, wide unit). A path that is valid for
a narrow agent is wrong for a wide one.

## Answer "can I get there?" before searching

A* proves that no path exists only by expanding everything reachable from the start. One unreachable
goal can therefore cost a whole-map flood, and a crowd retrying it every tick makes the frame several
times slower. Shipped colony and fortress sims all added the same fix:

- Keep a connected-component label per walkable cell for each movement class. Reject a request at once
  when `label[start] != label[goal]`.
- When re-flooding the whole map on each edit becomes measurable, switch to region-local labels
  (fixed squares such as 16×16) that are marked dirty on edit and recomputed when next read. Mark the
  neighbouring region dirty too when the edited tile lies on a region border.
- Let job and target selection consult reachability, and remember failures for a while. Otherwise every
  agent re-proves the same failure.

## Write one exact, bounded A* and its oracle

Default implementation:

- A consistent heuristic in the same units as the step cost: Manhattan for 4-connected grids, octile
  for 8-connected (`10*(dx+dy) - 6*min(dx,dy)` with costs 10/14), hex distance for hex grids. A
  squared distance, Manhattan on an 8-connected grid, or a heuristic in other units overestimates.
  A* then returns wrong paths that look fast.
- Integer costs, preallocated per-node storage, and a **generation stamp** per node instead of clearing
  arrays or allocating maps per search. Allocation inside the search costs an order of magnitude.
- A binary heap with a **total-order comparator**: f, then larger g, then a stable node index. Equal-f
  ties left to chance produce staircase paths, extra expansions, and replay divergence.
- Update a node when the new g is lower, not merely when it is unvisited. Test for the goal when a node
  is **popped**, not when it is pushed.
- A hard node budget that returns the best partial node, with a status of found, partial, unreachable
  or exhausted. A caller cannot react to a failure it cannot see.

Build a plain Dijkstra over the same graph beside it. Assert equal cost and legal steps on fixtures and
on seeded random pairs. With the heuristic set to zero the result must not change; if it does, the
heuristic overestimates. Read [search patterns](references/search-patterns.md) for the code: A*,
labels, flow fields, time-sliced search and funnel string-pulling, each with the bad version agents
usually write.

## Schedule requests; never path inline

Agent code must not call the pathfinder directly. One edit then makes every affected agent search in
the same tick. Route every request through a queue:

1. Reject unreachable requests before they are queued.
2. Merge identical requests made in the same tick into one search with several waiters.
3. Spend a fixed **iteration** budget per tick across a small fixed number of live searches, oldest
   first. Many simultaneous half-finished searches thrash the cache and finish later than serial ones.
4. Give a waiting agent a short partial search toward the goal, so it moves at once and refines later.
5. Deliver results in request order, on a fixed tick.

Count budgets in iterations or nodes, never in milliseconds, in any simulation that must replay or run
in lockstep. A slower machine then finishes paths on different ticks and diverges. The same applies to
worker threads: run the search off-thread if it helps, but deliver results on a fixed tick in request
order, never in thread-completion order, and discard results computed against a stale map revision.

## Repair edits locally

- A topology edit dirties the regions it touches and their bordering neighbours. Only agents whose
  remaining path crosses a dirty region repath, staggered over ticks by a hash of the agent id, and
  through the queue.
- A cost-only edit changes future searches and leaves existing paths alone.
- Each moving agent rechecks the next few path nodes every tick, and repaths on invalidation, on a
  stuck timer, or when its goal moves past a threshold. Repathing every tick is a storm.
- Choose the abstraction so that frequent edits do not touch it. A hierarchy built from terrain and
  ignoring buildings needs no repair when a building is placed.
- Incremental replanners (LPA*, D* Lite) suit one long-lived agent discovering small changes near
  itself. A crowd sharing a mutating map is better served by labels, regions and requeued searches.

Read [scheduling and repair](references/scheduling-and-repair.md) for the queue, the repair routine,
the counters to keep, and the order to try optimisations.

## Pick speedups only after measuring

Apply them in this order, each measured against the request trace before the next: fewer nodes;
reachability check; zero allocation; a matching heuristic and tie-break; heap tuning; a better
heuristic (landmarks, or a portal-graph distance from the goal), then a small weight of 1.1–1.5 where
paths seldom double back; jump point search where costs are uniform; a hierarchy where maps are large;
flow fields where goals are shared; static precomputation (JPS+, goal bounding, contraction
hierarchies) only when topology never changes at runtime.

Avoid the speedups that sources report backfiring: caching whole start-to-goal paths (almost no two
requests match), bidirectional A* (both frontiers stall behind the same barrier), and jump point search
on weighted or mutating maps (wrong paths, or precomputation that a single edit invalidates).

## Follow the path; avoid locally

The path is a plan. Movement is a separate layer.

- On a navmesh, eroded by the agent radius at build time, string-pull the polygon corridor into
  corners. Handling radius inside the funnel instead is far harder. On a grid, smooth with
  line-of-sight checks.
- Steering seeks the next corner. Local avoidance is separate from the plan: separation for loose
  crowds, reciprocal velocity obstacles (RVO/ORCA) for dense continuous crowds. Clamp avoidance output
  to the walkable boundary, because velocity-space avoidance knows nothing about walls.
- Tile-stepped agents need discrete claim, yield and wait arbitration, not velocity avoidance.
- Do not price other agents heavily into path cost. Every meeting in a one-wide corridor then triggers
  a fresh search. Resolve meetings locally and escalate a stuck agent: wait, then repath, then yield.
- Move a group as one virtual leader on one shared route, with members steering around it at no more
  than the slowest member's speed.

## Prove it

- A* matches the Dijkstra oracle in cost and legality, on fixtures and on public benchmark maps
  (grid maps with scenario files that list optimal lengths).
- Reachability labels agree with "Dijkstra finds a path"; after random edit sequences, incremental
  labels and caches equal a full rebuild.
- An unreachable goal returns at once with zero nodes expanded.
- Placing one wall in a crowd keeps repaths per tick within budget, with no frame spike past target.
- The same request trace, run twice, on one and on several worker threads, and on a throttled CPU,
  produces identical path hashes.
- Dense doorway and narrow-gap fixtures finish within a time bound, with no agent off the walkable area
  and no wide unit through a narrow gap.

Report nodes expanded per search by distance bucket, searches per tick by outcome, queue age at
delivery, repath rate by trigger, cache hit rates and path cost against the oracle. Read
[traps](references/traps.md) when a symptom matches and the cause is not obvious. Read
[the source map](references/sources.md) to audit or change these rules.
