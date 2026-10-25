# Traps

Read this when a pathfinding symptom has no obvious cause. Each entry gives the symptom, its cause,
the replacement, and the proof that it is fixed.

| Symptom | Cause | Replacement | Proof |
|---|---|---|---|
| One request makes a frame several times longer | Unreachable goal: A* expands the whole component | Reachability labels checked before queueing; node budget | Unreachable fixture returns with 0 expansions |
| Agents keep retrying an unreachable item or job | Failure not remembered | Job selection consults reachability; mark the target unavailable for a while | Failed searches per minute stay flat while an island of items exists |
| Fast search, wrong or longer paths | Overestimating heuristic: squared distance, Manhattan on 8-connected, wrong units, a hazard baked into the abstraction | Heuristic matching the movement, in cost units, from base costs only | Cost equals Dijkstra oracle; heuristic set to zero changes nothing |
| Assert or bad path when a closed node is reached more cheaply | Inconsistent heuristic with a closed set that never reopens | Consistent heuristic, or allow reopening | Debug assert that no closed node improves |
| Shortest path missed on some maps | Neighbour updated only "if not visited" | Update when the new g is lower | Fixture where the cheaper route is found second |
| Staircase paths, many expansions on open ground | Equal-f ties broken arbitrarily | Comparator: f, larger g, stable index; then smoothing | Expansions on an empty map ≈ path length |
| Search time scales with map size even for short trips | Allocating or clearing N-sized arrays per search | Preallocated pools with generation stamps | Zero allocations in the loop; short-search time independent of map size |
| Agents cut diagonally through wall corners | Diagonal allowed past a blocked flank | Require both flanking cells open | Benchmark scenario costs match |
| Thousands repath on the tick after one wall | Global invalidation, inline pathing | Dirty regions, only crossing agents, hash-staggered, through the queue | "One wall in a crowd" replay stays within the repath budget |
| Repath storm in narrow corridors | Other agents priced heavily into path cost | Small or no agent cost outside combat; local wait or sidestep; two-wide routes | Repaths per agent meeting ≈ 0 |
| Crowd flips between two routes or two goal slots | Everyone reacts to the same congestion snapshot in the same tick | Commit to a route for N ticks; staggered re-evaluation; switching margin; explicit slots or queues | Route switches per agent per minute bounded |
| Navmesh agents hug corners, clip walls, fit through gaps they cannot | Unshrunk mesh, polygon centres | Mesh eroded by radius per size class, then funnel | Narrow-gap fixture: no overlap, wide unit rejected |
| Avoidance pushes agents off the mesh; dense crowds deadlock | Velocity avoidance ignores boundaries; ORCA infeasible when packed | Clamp to boundary segments; stuck timer escalates | Dense doorway clears within a bound, nobody off-mesh |
| Replays diverge only under load | Budgets in milliseconds | Budgets in iterations; results on fixed ticks | Same trace on a throttled CPU, identical checksum |
| Desync with no load difference | Ties by insertion order or address, hash-order neighbours, float costs, random draws in cost sampling | Integer costs, total order, fixed neighbour order, hashed coordinates instead of random draws | Identical path hashes across builds and platforms |
| Different results with more threads | Results applied in completion order | Fixed-tick delivery in request order; discard stale revisions | 1-thread and N-thread checksums equal |
| Time-slicing many searches is slower than serial | One open list per live request thrashes the cache | Small fixed number of live searches, or two lanes | Paths per second under the burst trace improves |
| Path cache barely hits and serves stale paths | Exact start-to-goal paths rarely repeat | Cache labels, segment costs, flow tiles per portal, popular goal nodes | Measured hit rate and saved expansions exceed invalidation cost |
| Jump point search gives wrong paths or no speedup | Weighted or mutating map; large open areas | Use it only on uniform-cost static regions | Oracle equality on weighted fixtures; measured speedup |
| Hierarchical search slow for short trips, kinks at cluster borders | Inserting start and goal dominates; abstract paths unsmoothed | Plain A* under a distance threshold; smooth; refine lazily | Timing per distance bucket shows the crossover |
| Bidirectional search to "handle islands" doubles the work | Both frontiers stall behind the barrier | Reachability labels answer islands at once | Barrier fixture expansions |
| Weighted A* takes absurd detours | Path must first head away from the goal (one bridge, one staircase) | Lower weight, or topology-aware heuristic | Cost ratio on the connector fixture |
| Agent walks into a new wall, or stands forever | Path never revalidated; failed repath has no fallback | Lookahead validity check; partial path plus retry; cancel the task when unreachable | Wall-on-path fixture reroutes within k ticks |
| Flow field rebuilt every tick | Field used for a moving or unique goal | Fields for shared goals only; rebuild only the goal tile | Field builds per tick ≤ distinct shared goals |
| Group squeezes through a gap a member cannot, or blocks a corridor | Group routed as one disc, or every member routed separately | One shared route for a virtual leader, member steering, slowest speed | Narrow-gap group fixture |
