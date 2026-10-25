---
name: game-traffic
description: Use when designing, implementing, tuning, reviewing, or debugging road traffic in a game or simulation such as a city builder or transport game, including lane graphs, junctions and signals, car-following, lane changes and merges, highway ramps, roundabouts, vehicle routing under congestion, parking, gridlock, despawning, traffic overlays, or how many vehicles to simulate individually rather than as flow. It supplies the lane-and-distance vehicle model, car-following and lane-change rules with game-ready parameters, junction entry checks, gridlock exits, damped congestion costs, and the order to buy scale. Do not use it for pathfinding on grids or navmeshes, or for pedestrian crowds.
---

# Engineer game traffic

Game traffic fails in the same few places: all cars in one lane, lane changes at the last metre, a
car stopped inside a junction, everyone choosing the same road, and vehicles silently deleted to hide a
jam. Build the model so that each of those is either impossible or counted.

## Decide whether vehicles are the simulation or a readout of it

Simulate individual vehicles only when the player must watch causes, such as a jam forming behind a bad
junction. Otherwise keep traffic as volume per link against capacity, and draw cosmetic cars from it.
SimCity 4 did this: its cars were only loosely correlated with the statistics that decided commutes.
Cities: Skylines made every visible car an agent. A hybrid keeps agents where the player looks and
queues or flow elsewhere. Decide this first, because it decides everything below.

## Build a lane graph separate from the road mesh

- A segment holds lanes. A junction holds **connections**, one per legal movement from an incoming lane
  to an outgoing lane, each with its own path across the junction.
- Precompute per connection, when the junction is edited: a bitset of geometrically conflicting
  connections, a bitset of those it must yield to, and its signal index. Never discover conflicts at
  runtime from bounding boxes.
- One-ways, turn restrictions and lane arrows are simply which connections exist. Limited access is the
  absence of a connection, not a cost.
- Build the road mesh from the graph, never the graph from the mesh. Regenerate connections on every
  topology edit and re-apply custom overrides by stable lane meaning, not lane index. Then flag any lane
  left without an outgoing connection: a traffic mod for a shipped city builder lists connections lost
  when a road is replaced or reversed among its known issues.
- Use dense integer ids into arrays, not pointers, so the graph saves, hashes and replays.

On a tile game with one lane per direction, the state can be the tile plus its entry direction.

## Put vehicles at (lane, distance), never in free physics

Each lane keeps its vehicles in a list ordered by distance along the lane. A vehicle stores distance,
speed and length; its world position is derived from the lane curve and only rendered. The leader is the
neighbour in the list. For the front car, look across the lane end into the next lane on its route and
treat that lane's last car as the leader, offset by the remaining length. Treat a red signal or a yield
line as a stopped leader at the lane end. Re-sort and re-resolve neighbours after every insert, removal
or transfer between lanes. One open-source traffic simulator shipped a bug from stale leader indices
after a merge.

## Choose a car-following rule

Default to the Intelligent Driver Model:

```text
a_IDM = a * (1 - (v/v0)^4 - (s*/s)^2)
s*    = s0 + max(0, v*T + v*(v - v_leader) / (2*sqrt(a*b)))
```

- Use a = 0.8–2.5 m/s², b ≈ 2 m/s², T = 1.0–1.5 s, s0 = 2 m, and v0 = min(the driver's desired speed,
  the speed limit, the curve speed). The model's reference table uses a = 0.3 m/s² on purpose, to
  provoke stop-and-go waves. Copied verbatim, it makes every road wave and every car feel sluggish.
- Step at a fixed dt of 0.5 s or less. Faster game speed means more fixed steps per frame, capped, never a
  larger dt. A larger dt overshoots the leader, and cars overlap or tunnel at 4×.
- Run two phases: compute every acceleration from the state at time t, then integrate. Updating in place
  lets followers read a half-moved world. Clamp the gap denominator at s0, floor braking at a maximum
  deceleration, and stop exactly at zero speed rather than reversing.
- Cap v0 by curvature so cars slow before a turn. One microscopic simulator limits turn speed to
  `sqrt(radius × 5.5)` m/s by default. Look ahead to the next connection's curve speed so braking
  starts in time.

Deviate to a safe-speed model at a 1 s step, or to a cellular automaton on a tile map where only queue
shape matters. Use event-driven queues when only arrival times matter; one simulator's author found
smooth acceleration added little there.

## Choose lanes early; change lanes only when it is safe and worth it

- When a vehicle enters a segment, choose the lane from the next two to four route steps and commit to
  it. Score candidate lanes lexicographically: lane type, then queued vehicles plus lane changes needed,
  so cars do not switch lanes to pass one car. Late lane changes are a jam cause that both a shipped
  city builder's patch notes and a long-lived traffic mod name. Choosing once at trip start piles every car
  into one lane.
- Discretionary changes use MOBIL. The new follower's deceleration after the change must stay under
  `b_safe` (4 m/s²), even for selfish drivers. Change only when
  `gain > p × (harm to old and new followers) + a_thr`, with p from 0 to 0.5 and `a_thr` = 0.2 m/s². Add
  a cooldown of a few seconds, and reset the decision state for each candidate lane: one implementation
  shipped a flag that leaked between candidates.
- On highways, move one lane at a time and keep lanes when entering or exiting. Do not let every car pick
  the emptiest lane every tick: the lanes oscillate. Randomise a share of drivers by a static per-vehicle
  seed instead.

## Let a vehicle into a junction only when it can leave

Check, in this order, before a vehicle starts a connection:

1. No accepted vehicle holds a conflicting connection.
2. The signal or priority rule allows it. A minor green means yield: accept the gap only when the time
   to the conflict point differs from every priority foe's by about 1 s or more.
3. **Block the box:** the exit lane has room for the vehicle's length plus a following gap. Reserve that
   room on entry and release it when the vehicle's rear leaves the lane. Assert that reserved length never
   goes negative.

Wake waiting vehicles when a connection or exit space is released, rather than retrying every tick. One
simulator found junction retries dominating the profile once jams formed. Serve waiting requests from an
ordered container, by urgency and then wait time. For reservation-style junctions, reserve space-time
tiles, and protect the front car from followers stealing its slot.

## Detect gridlock and give every vehicle a counted exit

- Record who blocks whom whenever entry is refused, and search that graph for a cycle. When one is found,
  let one member of the cycle block the box. Flag vehicles on overflowing queues as urgent, because they
  are most likely to be in the cycle.
- As a last resort, count a timeout only for the head vehicle of a lane that cannot enter its next step,
  below a crawl speed. Counting any slow vehicle deletes cars from long but moving queues. Shipped
  values range from 300 s (a microscopic simulator) to driving through the blocker after a long counter
  (an open-source transport game).
- Relocate or remove the vehicle with its trip settled, and **count every removal by reason**. Assert
  `spawned == active + arrived + removed` every tick. A rising removal rate is a defect signal: fix the
  junction priorities, signal timings or demand, do not tune the timeout.
- Let players turn removal off. A traffic mod's documentation notes that despawning keeps traffic flowing
  but hides the bottleneck the player needs to fix.

## Price congestion into routes, damped and spread

- Link cost is free-flow time × (1 + k × congestion), where congestion comes from measured mean speed
  relative to the limit, smoothed over a window. A volume/capacity curve such as BPR,
  `t0 × (1 + 0.15 × (V/C)^4)`, is the alternative. Add explicit turn and lane-change costs: a city
  builder patched U-turns that had cost nothing.
- Multiply by a seeded per-query, per-segment perturbation whose spread widens with density, so that
  equal routes share load. All-or-nothing shortest distance sent everyone down the same road in a
  shipped city builder's launch build.
- Reroute on staggered cohorts, `(tick + id) % period`, or when the route ahead is blocked. Never reroute
  inside a committed section such as an on-ramp. Accept a new route only if it beats the old by a margin.
  Everyone rerouting on the same snapshot makes traffic slosh between two roads.
- Cache only the next few route decisions; one transport game caches eight. On a road edit, mark only
  routes through the edited segments dirty, reroute from the current lane, and remove a vehicle only when
  no route exists.
- Claim a destination or parking slot before departure. A city builder's agents swarmed one business
  until each was guaranteed an open slot before leaving.

Read [patterns](references/patterns.md) for the code: the lane graph, leader lookup, the two-phase IDM
step, junction entry, gridlock detection, congestion cost and reroute policy, and lane choice with MOBIL.

## Buy scale in this order

1. Remove waste: event wakes at junctions, precomputed conflict bitsets, per-lane lists instead of
   global neighbour searches.
2. Cadence: a fixed simulation rate below the render rate, interpolated for display (Cities: Skylines
   moved cars about four times a second). Run lane choice, rerouting and signal checks on staggered
   slots.
3. Route budget: a request queue, bounded searches, a cached prefix, local invalidation. Run searches on
   workers against an immutable graph snapshot, and commit results in request order.
4. Distance level of detail for vehicle physics away from the camera, never for outcomes.
5. Queues per segment, or flow, for off-screen or whole-map traffic. One simulator reports its queue
   model running up to 100 times faster than its microscopic one.
6. Caps and removal last, and visible, because hitting a cap degrades the whole city.

Read [scale and tuning](references/scale-and-tuning.md) for the counters to keep and the figures sources
report.

## Prove it

- Build the tools before tuning. Use an overlay coloured by mean speed relative to the limit, not by
  vehicle count: busy roads that flow are not problems. Add follow-one-vehicle logs filtered by vehicle
  and junction id.
- Check invariants every step: lanes sorted by distance, gaps ≥ 0, reserved length ≥ 0, every spawned
  vehicle accounted for.
- At 1×, 4× and 16× game speed, trajectories match within tolerance and no gap goes negative.
- On a saturated grid, no vehicle stops inside a junction while a cross stream waits. A scripted
  four-arm deadlock resolves without a removal.
- Two equal parallel routes each carry 40–60% under load, and the split converges rather than
  alternating. On a three-lane straight with even demand, lane occupancies stay within 20%.
- A highway exit shows no vehicle stopped in a through lane waiting to change. Bulldozing a main road
  keeps path requests under budget and removes no vehicle while an alternative exists.
- Two runs from one save give the same state hash at tick N: lanes and junctions in id order, ordered
  waiting queues, ties broken by vehicle id, seeded perturbations, integer route costs.

Read [traps](references/traps.md) when a symptom matches and the cause is not obvious. Read
[the source map](references/sources.md) to audit or change these rules.
