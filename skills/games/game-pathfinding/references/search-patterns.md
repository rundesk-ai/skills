# Search patterns

Read this before writing or reviewing a search: A*, reachability labels, a flow field, a time-sliced
query, or string-pulling. Each pattern is language-neutral pseudocode. Port it to the stack's own
containers, and keep the properties the comments name.

## A* with preallocated nodes, generation stamps and total-order ties

The version agents usually write allocates a priority queue and hash maps on every call, iterates
neighbours from an unordered container, uses float costs, skips a node once it has been seen even when a
cheaper route arrives later, uses squared distance as the heuristic, and floods the whole component
before returning nothing. Every one of those is a measured failure.

```text
# Allocated once per map (or once per worker thread). N = cell count.
struct Node { g: int32; f: int32; parent: int32; openStamp: uint16; closedStamp: uint16 }
nodes: Node[N]
openGen, closedGen: uint16 = 1, 2
heap: IntHeap(capacity)                       # holds cell indices; preallocated

function beginSearch():
    openGen += 2; closedGen += 2               # a new generation, no clearing
    if closedGen >= STAMP_MAX - 2:             # wraparound is the only full clear
        for i in 0..N-1: nodes[i].openStamp = 0; nodes[i].closedStamp = 0
        openGen, closedGen = 1, 2
    heap.clear()

function less(a, b):                           # a total order: no tie left to chance
    if nodes[a].f != nodes[b].f: return nodes[a].f < nodes[b].f
    if nodes[a].g != nodes[b].g: return nodes[a].g > nodes[b].g   # deeper first
    return a < b                                                  # stable index

function astar(start, goal, budget):
    if label[start] != label[goal]: return (UNREACHABLE, [])
    beginSearch(); open(start, g = 0, parent = NONE)
    best = start; expanded = 0
    while not heap.empty():
        cur = heap.popMin(less)
        if nodes[cur].closedStamp == closedGen: continue           # stale duplicate
        nodes[cur].closedStamp = closedGen
        if cur == goal: return (FOUND, reconstruct(cur))           # test on pop
        if h(cur) < h(best): best = cur
        expanded += 1
        if expanded >= budget: return (PARTIAL, reconstruct(best))
        for dir in FIXED_DIR_ORDER:                                # never a hash-set order
            n = cur + offset[dir]
            if not passable(n) or cutsCorner(cur, dir): continue
            g = nodes[cur].g + stepCost(cur, dir)                  # integers: 10 / 14
            if nodes[n].openStamp == openGen and g >= nodes[n].g: continue   # better-cost test
            nodes[n].openStamp = openGen; nodes[n].closedStamp = 0
            nodes[n].g = g; nodes[n].f = g + h(n); nodes[n].parent = cur
            heap.push(n, less)                                     # duplicates skipped on pop
    return (EXHAUSTED, reconstruct(best))

function h(n):                                 # octile, integer, the same units as stepCost
    dx = abs(x(n) - x(goal)); dy = abs(y(n) - y(goal))
    return 10 * (dx + dy) - 6 * min(dx, dy)
```

- **Duplicates or decrease-key.** Pushing duplicates and skipping stale entries on pop is usually
  cheaper than decrease-key. Looking the node up in an open hash and re-inserting it is also correct.
  Choose one deliberately.
- **Closed sets need a consistent heuristic.** With a weighted or inconsistent heuristic, a closed node
  can later be reached more cheaply. Either allow reopening or accept bounded suboptimality, and in debug
  builds assert that no closed node improves.
- **Corner cutting.** Allow a diagonal step only when both flanking orthogonal cells are open. Public
  grid benchmarks assume this when they list optimal lengths.
- **The open list.** Under about 10–30 open nodes, an unordered array can beat a heap. With integer
  costs in a narrow range, a bucket queue can beat both. Measure on the request trace.
- **Do not step back to the parent.** It saves roughly one neighbour in eight on a grid.

## Reachability labels

```text
label: int32[N]                         # 0 = not walkable for this movement class
function relabelAll():
    fill(label, 0); next = 1
    for c in 0..N-1 in index order:     # fixed order -> the same label numbers every run
        if walkable(c) and label[c] == 0: floodFill(c, next); next += 1   # iterative, preallocated queue
function reachable(a, b): return label[a] != 0 and label[a] == label[b]
```

A full relabel was measured at about 5.5 ms on a 200×200 map on 2013 hardware: fine on an edit, too
slow every frame. When it shows up in a profile, switch to region-local labels:

```text
REGION = 16
function onTopologyEdit(t):
    regionValid[regionOf(t)] = false
    for side in 4 sides:                           # a border tile changes the neighbour's view too
        u = t + step(side)
        if regionOf(u) != regionOf(t): regionValid[regionOf(u)] = false
    reachCache.clear()

function patchOf(t):                               # every reader goes through this
    r = regionOf(t)
    if not regionValid[r]: labelInside(r); regionValid[r] = true
    return (r, localLabel[r][local(t)])
```

Global reachability then becomes a search over the small graph of (region, patch) nodes. Cache its
answers by (patch A, patch B, movement class), and clear the cache on any topology edit. Do not cache
answers that depend on moving obstacles.

## Flow field for a shared goal

Use a flow field only when many agents share a goal: a rally point, an exit, a dining hall. Running N A*
searches toward one point wastes work, and rebuilding a field every tick for a goal that moves wastes
more.

```text
# Per sector (a shipped RTS used 10x10 cells). Clear sectors share one static all-ones cost field.
cost:  uint8[S*S]        # 1..254 traversal cost, 255 = wall
integ: uint16[S*S]       # integrated cost to the goal
flow:  uint8[S*S]        # direction index plus flags (pathable, line of sight)

function requestPath(source, goal):
    if island[source] != island[goal]: fail
    portals = astarOverPortalGraph(source, goal)    # prefer portals other requests already use
    for sector along portals: requestFlowTile(sector, exitPortal)   # cached per (sector, exit)

function integrate(sector, front):                  # bucket-queue Dijkstra, 4-neighbour relax
    integ[*] = INF; for (cell, c0) in front: integ[cell] = c0; push(cell)
    while front not empty:
        c = popMin()
        for n in fixed 4-neighbour order:
            if cost[n] == 255: continue
            v = integ[c] + cost[n]
            if v < integ[n]: integ[n] = v; push(n)
    for c: flow[c] = hasLineOfSightToGoal(c) ? STRAIGHT : argmin over 8 neighbours of integ   # fixed tie order
```

- With several goals, seed every goal at zero. That is the same as adding a virtual goal node.
- A wavefront meeting cells already integrated must stop, unless the improvement is significant;
  otherwise fronts bounce back and forth.
- On an edit, dirty that sector's cost field and its portals, then rebuild the portal links of it and its
  neighbours. Rebuild only the field tiles whose portal windows changed.
- On uniform-cost grids, writing g straight to the closed list for cells that are not jump points
  (canonical Dijkstra) was measured 2.5–4× faster than plain Dijkstra.

## Time-sliced query

Keep the whole search state in the query object, in its own preallocated pool:

```text
struct Query { start, goal, mode, mapRevision; status: NONE|RUNNING|FOUND|PARTIAL|FAILED; search state }

function init(q):            q.mapRevision = map.revision; seed(q.start); q.status = RUNNING
function update(q, maxIter): it = 0
                             while it < maxIter and q.status == RUNNING: expandOne(q); it += 1
                             return it
function finish(q):          return reconstruct(q.found ? q.goal : q.bestSoFar)
```

A query is valid only against the map it started on. When an edit dirties a region on its frontier,
restart the query rather than continue it. Never yield on elapsed milliseconds inside a deterministic
simulation; count iterations.

## Funnel string-pulling over a navmesh corridor

Walking polygon centres or edge midpoints hugs corners and zig-zags. Erode the navmesh by the agent
radius when it is built, then pull the corridor taut:

```text
portals = [(start,start)] + corridorEdges(left,right) + [(goal,goal)]
apex = left = right = start; apexI = leftI = rightI = 0
i = 1
while i < len(portals):
    (pl, pr) = portals[i]
    if triarea2(apex, right, pr) <= 0:                         # right side can tighten
        if apex == right or triarea2(apex, left, pr) > 0: right = pr; rightI = i
        else: emit(left); apex = right = left; apexI = rightI = leftI; i = apexI + 1; continue
    if triarea2(apex, left, pl) >= 0:                          # left side can tighten
        if apex == left or triarea2(apex, right, pl) < 0: left = pl; leftI = i
        else: emit(right); apex = left = right; apexI = leftI = rightI; i = apexI + 1; continue
    i += 1
emit(goal)
```

- Polygon winding decides which shared-edge vertex is left. Test with both windings.
- A poor A* corridor produces a poor pulled path. Fix the corridor, not the funnel.
- Readers of the original description reported edge cases, such as an end point emitted twice.
  Check the output against fixtures rather than trusting a port.
- Re-optimise the corridor periodically, not every tick. One navigation library does it at most every
  0.5 s.
