# Scale and tuning

Read this when traffic costs too much, when the vehicle count must grow, or when choosing defaults for
signals, timeouts and cadence.

## Counters

- Milliseconds per simulation tick, split into car-following, lane changes, junction requests, route
  searches and route invalidation.
- Vehicles active, waiting at junctions, and removed per minute, by reason.
- Route requests per tick and the queue length.
- Junction request retries: repeated, refused, blocked-by-another. One open-source simulator keeps these
  three counters.

## What sources report, for scale rather than as targets

| Item | Figure |
|---|---|
| Cities: Skylines car movement | about 4 times per second; rendering interpolates between two simulation frames |
| Cities: Skylines physics detail | full near the view; reduced beyond about 500 m; lowest beyond about 1,100 m from the physics reference point |
| Cities: Skylines stuck vehicles | released after a block counter reaches its limit, back toward origin |
| An open-source transport game | blocked road vehicle drives through its blocker after 1,480 ticks; route cache of 8 decisions; 10,000-node search limit |
| A microscopic research simulator | 1 s default step; 300 s teleport for a lane head below 0.1 m/s; speeds averaged over 180 steps for rerouting; 90 s default signal cycle |
| The same simulator's queue model | 100 m segment queues, up to 100× faster than microscopic, junction control off by default |
| An open-source city builder in development | traffic logic and route searches each every 10th tick per lane, staggered by id |
| Intelligent Driver Model | steps below 0.5 s give essentially the same result |
| SimCity (2013) engine talk coverage | a target of 10,000+ agents moving at once |

No shipped game publishes microseconds per vehicle against a frame budget.

## Defaults worth starting from

| Choice | Start with | Why |
|---|---|---|
| Simulation rate | fixed, below render rate, interpolated | display smoothness without per-frame cost |
| Decision cadence | lane choice and rerouting on `(tick + id) % N` | spreads the cost and the reactions |
| Yield gap | about 1 s time gap against priority foes | a research simulator's default for minor links |
| Stuck timeout | long, lane head only, counted, player-toggled | removal hides bottlenecks |
| Reroute | on blocked route ahead, or staggered period, with a margin | prevents sloshing |
| Route cache | the next few decisions, re-decided near multi-stop destinations | fresh choice where it matters |
| Signal cycle | fixed-time phases first; actuated only when measured queues demand it | fixed time is predictable and testable |

## Order to try optimisations

1. Remove waste: event wakes, precomputed conflicts, per-lane lists.
2. Cadence: fixed lower simulation rate with interpolation; staggered decision slots.
3. Route budget: queue, bounded search, cached prefix, local invalidation, worker threads over an
   immutable snapshot, committed in request order.
4. Distance detail for physics only.
5. Segment queues or aggregate flow off-screen, or for the whole map with cosmetic cars.
6. Caps and removal last, visible to the player.
