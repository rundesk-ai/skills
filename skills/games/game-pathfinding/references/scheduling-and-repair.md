# Scheduling, repair and tuning

Read this when building the path request queue, handling map edits, moving searches to worker threads,
or tuning pathfinding cost at scale.

## Request queue

```text
MAX_LIVE = 8           # one shipped navigation library's queue size; tune by measurement
ITER_BUDGET = 100      # node expansions per tick across all live searches; tune by measurement
queue ordered by (enqueueTick, requestId)          # ids assigned in a stable sweep over agents

function request(agent, start, goal, mode):
    if not reachable(start, goal, mode): agent.onPathFailed(UNREACHABLE); return
    key = (patchOf(start), goal, mode)
    if pending[key]: pending[key].waiters.add(agent); return          # merge duplicates
    agent.path = quickPartial(start, goal, maxIter = 20)             # move now, refine later
    enqueue(Request(key, start, goal, mode, tick, nextId++))

function tick():
    budget = ITER_BUDGET
    for req in the first MAX_LIVE requests, in queue order:
        if req.status == NONE: init(req)
        budget -= update(req, budget)
        if budget <= 0: break
    for req finished this tick, in queue order:
        for agent in req.waiters sorted by id: agent.setPath(finish(req))
        remove(req)
    drop results nobody has collected after a couple of ticks
```

- Serve the request that has waited longest first. Under load, a queue ordered by distance or priority
  alone starves somebody.
- When one long search blocks many short ones, split the queue into two lanes: at most one live search
  for requests whose start–goal distance predicts a short search, and one for long ones.
- A failed request reports its cause (unreachable, or budget exhausted) so that job selection can stop
  offering the target for a while.

## Worker threads without divergence

1. Give the worker an immutable snapshot of the map, or a revision number that it checks.
2. Make results available at a fixed tick, such as the enqueue tick plus k, never when the job happens
   to finish.
3. Apply results in request-id order.
4. Discard a result whose map revision is older than the last topology edit on its route, and requeue
   the request.
5. Treat a thread that dies as a fatal error. One shipped colony sim had a pathfinding thread that
   crashed silently; afterwards agents could only reach areas they could reach before the crash.

## Repair after an edit

```text
function onTopologyEdit(cells):
    dirty = regionsTouching(cells) ∪ borderNeighbours(cells)
    for r in dirty: regionValid[r] = false; abstractEdgesDirty[r] = true
    reachCache.clear()                                  # small; cheaper than tracking dependencies
    for agent in agentsWhoseRouteCrosses(dirty) sorted by id:     # a region -> agents index
        agent.needsRepath = true
        agent.repathTick = now + hash(agent.id) % STAGGER         # spread the burst deterministically

function onCostOnlyEdit(cells):
    updateCostField(cells)                              # future searches see it; current paths continue

function follow(agent):
    if not routeValid(agent, lookahead = 10): agent.needsRepath = true
    if agent.needsRepath and now >= agent.repathTick: request(agent, ...)
    if noProgress(agent, STUCK_TICKS): escalate(agent)  # wait -> repath -> yield -> give up the task
```

- Treat "the incremental cache equals a full rebuild" as a test that runs after every random edit
  sequence. A route-segment cache in a long-lived open-source transport game has had stale-cache bugs
  reported against it.
- A wall placed on an agent's path must reroute it within a few ticks. If the target becomes
  unreachable, cancel the task rather than leaving the agent standing.

## Counters to keep in the build

- Nodes expanded per search, as a histogram by start–goal distance bucket.
- Searches per tick by outcome: found, partial, unreachable rejected before search, budget exhausted.
- Iterations used per tick against the budget; queue length; queue age at delivery, in ticks.
- Milliseconds per tick for search, field integration, region repair and avoidance, measured
  separately. Measure request bursts and edit bursts separately, because they stall for different
  reasons.
- Repaths per agent per minute, by trigger: invalidated, stuck, goal moved.
- The hit rate of every cache, and path cost against the oracle on a sample.

## What sources report, for scale rather than as targets

| Figure | Context |
|---|---|
| ~200 µs / ~2,500 µs / >20,000 µs | fastest, average and slowest A* written for one assignment, on one map |
| ≥10× slower | A* that allocates during the search |
| 10,000 nodes (range 500–1,000,000) | default search-node limit in an open-source transport game |
| 8 searches, 100 iterations per update, 4,096 nodes, 20-iteration quick search, 10-polygon lookahead, 1 s replan delay | one navigation library's crowd defaults |
| 15,000 grid nodes → 100 nodes and 400 edges | a tower sim's floors-and-connectors graph, plus a limited job queue, holding 60 FPS |
| up to 10× faster than A*, within 1% of optimal after smoothing | HPA* on 2004 hardware |
| an order of magnitude and more | jump point search over A*, uniform-cost grids |
| up to 100× over A* | JPS+ with precomputation, static maps only |
| ~8× | goal bounding, static maps only |
| 5,000 agents in 8–16 ms on 8 cores | ORCA avoidance benchmark |
| ~20× | a city builder's shipped A* over its first version, about 350 lines with the flood fill |

## Order to try optimisations

Measure each step against the request trace before taking the next:

1. Reachability check, which removes the worst searches.
2. Node budget, request queue with an iteration budget, and merged duplicates, which remove the spikes.
3. Fewer nodes: segments, navmesh or waypoints instead of cells, where that fits.
4. Zero allocation, generation stamps, cached neighbour lists.
5. A matching heuristic, then the tie-break.
6. The open-list structure: heap, then a bucket queue.
7. A better heuristic (landmark distances, or portal-graph distance from the goal), then a small weight.
8. Jump point search on uniform-cost regions; a hierarchy for large maps; flow fields for shared goals.
9. Static precomputation, only for topology that never changes at runtime.
10. Threads last, with fixed-tick delivery.
