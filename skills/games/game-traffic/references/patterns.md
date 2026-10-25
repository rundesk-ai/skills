# Traffic patterns

Read this before writing or reviewing the lane graph, vehicle stepping, junction control, gridlock
handling, congestion-aware routing or lane choice. The pseudocode is language-neutral and written fresh
from the behaviour of the sources; port it to the stack's own containers.

## Lane graph

```text
LaneId, ConnId, SegmentId, NodeId: dense integer ids indexing arrays

Segment    { id, nodeA, nodeB, lanes: [LaneId] (index 0 = rightmost), speedLimit }
Lane       { id, segment, index, length, curve (arc-length parametrised), speedLimit, allowedClasses,
             outConns: [ConnId], left: LaneId?, right: LaneId?,
             vehicles: [VehId] ordered by s descending (front first),
             reservedLength }                                   # block-the-box accounting
Connection { id, node, fromLane, toLane, via (path across the junction), length,
             dir: STRAIGHT | LEFT | RIGHT | UTURN,             # restriction = connection absent
             foes: BitSet over node.conns,                     # geometric conflict
             yieldsTo: BitSet over node.conns,                 # foes with priority over this one
             signalIndex }
Node       { id, conns, kind: PRIORITY | ALLWAY_STOP | SIGNAL | ROUNDABOUT, signal? }
Signal     { phases: [{ duration, state: one char per signalIndex: 'G' green, 'g' green-yield, 'y', 'r' }] }
```

Build `foes` and `yieldsTo` once per junction edit, by intersecting the `via` paths.

## Leader lookup

```text
leaderOf(lane, i, me):
    if i > 0:
        lead = lane.vehicles[i-1]
        return (lead, lead.s - lead.length - me.s)
    next = nextLaneOrConnection(me.route)
    if next.vehicles not empty:
        last = next.vehicles.back
        return (last, (lane.length - me.s) + last.s - last.length)
    if stopRequiredAt(lane.end, me):                       # red, yield, stop line
        return (VIRTUAL_STOPPED, lane.length - me.s - stopOffset)
    return (none, +inf)
```

```text
BAD   scan every vehicle for the nearest one ahead               # O(n²)
BAD   stop the lookup at the lane end                            # the car accelerates into a stopped queue
BAD   keep neighbour indices across a lane transfer              # stale leaders after merges
GOOD  sorted per-lane list, one look across into the next route lane, re-sort after every transfer
```

## Two-phase IDM step

```text
# Phase 1: every acceleration from the state at time t; no writes to positions
for lane in lanes in id order:
    for i, veh in enumerate(lane.vehicles):                  # front to back
        (lead, gap) = leaderOf(lane, i, veh)
        v0 = min(veh.desired, lane.speedLimit, curveSpeed(lane, veh.s), nextCurveSpeedBraking(veh))
        free = veh.v < v0 ? a * (1 - (veh.v / v0)^4) : a * (1 - veh.v / v0)
        inter = 0
        if lead:
            sstar = s0 + max(0, veh.v * T + veh.v * (veh.v - lead.v) / (2 * sqrt(a * b)))
            inter = -a * (sstar / max(gap, s0))^2
        veh.acc = max(-B_MAX, free + inter)

# Phase 2: integrate, then transfer and re-sort
for veh:
    if veh.v + veh.acc * dt < 0: ds = -veh.v * veh.v / (2 * veh.acc); veh.v = 0   # stop, never reverse
    else: ds = veh.v * dt + 0.5 * veh.acc * dt * dt; veh.v += veh.acc * dt
    veh.s += ds
transferVehiclesPastLaneEnds(); resortLanes()
```

| Parameter | Use | Reference value and its remark |
|---|---|---|
| a | 0.8–2.5 m/s² | 0.3 in the reference table, deliberately low to provoke stop-and-go |
| b | about 2 m/s² | 3 for cars, 2 for trucks in the table |
| T | 1.0–1.5 s | 1.5 s car, 1.7 s truck; realistic 0.8–2 s |
| s0 | 2 m | kept at standstill, including at red lights |
| δ | 4 | |
| dt | ≤ 0.5 s | steps below 0.5 s give essentially the same result |

```text
BAD   dt = baseDt * gameSpeed                       # overlaps and tunnelling at 4×
GOOD  fixed dt; more steps per frame at higher speed, with a cap per frame

BAD   (s*/s) with s near zero or negative          # infinity or NaN
GOOD  max(gap, s0) and a braking floor; a NaN check in debug builds
```

## Junction entry

```text
tryStart(veh, conn):
    node = conn.node
    if any accepted c in node with conn.foes[c]: return WAIT
    if node.kind == SIGNAL:
        st = node.signal.stateFor(conn.signalIndex, tick)
        if st == 'r' or (st == 'y' and not canClearBeforeRed(veh)): return WAIT
        if st == 'g' and not gapOk(veh, conn): return WAIT
    else if node.kind in (PRIORITY, ROUNDABOUT) and not gapOk(veh, conn): return WAIT
    out = conn.toLane; need = veh.length + FOLLOW_GAP
    if out.reservedLength > 0 and out.reservedLength + need >= out.length
       and not (node.allowsBlockBox or inDetectedCycle(veh)): return WAIT
    out.reservedLength += need                 # released when the vehicle's rear leaves `out`
    node.accept(veh, conn)
    return GO

gapOk(veh, conn):
    tMe = timeToConflict(veh, conn)
    for foe approaching on conn.yieldsTo: if abs(timeToConflict(foe, conn) - tMe) < GAP_MINOR: return false
    return true                                 # GAP_MINOR about 1 s
```

- A junction joining only two roads is an artefact of how roads are split. Let it block the box.
- Wait in an ordered queue keyed by (not urgent, wait time). Wake vehicles when an accepted turn finishes
  or exit space is released, instead of retrying every tick.
- Roundabouts: entering vehicles yield to circulating ones. Widen spacing between close junctions, and let
  micro-roundabouts block the box under the cycle rule.

Space-time reservation, for junctions without signals or for autonomous vehicles:

```text
request(veh, arrivalTick, arrivalV):
    d = arrivalV * (arrivalTick - tick)
    if d > lane.minRejectedDist: return reject(retryAfter = tick + TIMEOUT)    # the front car goes first
    cells = simulateCrossing(veh, arrivalTick, arrivalV) + safetyBuffer       # [(tile, tick)]
    if any cell held by another vehicle: lane.minRejectedDist = min(lane.minRejectedDist, d); return reject(...)
    hold(cells, veh); lane.minRejectedDist = +inf; return confirm
```

## Gridlock detection and the exit

```text
onRefused(me, targetLane):
    blockedBy.add(me -> holderOf(targetLane))          # the lane's laggy head, last car, or the turn filling it
    if findCycle(me): allowBlockBox(me)                # tier 1: break the cycle locally

findCycle(start):                                      # DFS that must return to start
    stack = [start]; seen = {}
    while stack:
        cur = stack.pop()
        if seen and cur == start: return seen
        if cur in seen: continue
        seen.add(cur)
        stack += [b for b in blockedBy[cur]]
        if cur != start and not isLaneHead(cur): stack.push(headOf(laneOf(cur)))
    return none

perTick(veh):                                          # tier 2: counted timeout
    if isLaneHead(veh) and veh.v < 0.1 and not atScheduledStop(veh): veh.stuck += dt
    else: veh.stuck = 0
    if veh.stuck > STUCK_LIMIT:
        stats.removed[reason] += 1; log(veh, lane, node, tick)
        relocateAlongRoute(veh) or removeSettlingTrip(veh)
```

```text
BAD   silent despawn                      # trip counts, deliveries and statistics drift
BAD   timeout on any slow vehicle         # deletes cars from long moving queues
BAD   despawn treated as the fix
GOOD  head-only timeout, counted by reason, trip settled, removal heatmap, player toggle
```

## Congestion cost and reroute policy

```text
onSample(lane, v): lane.accSpeed += v; lane.samples += 1
every K ticks, per lane:
    lane.meanRel = lane.samples > 0 ? min(REF, lane.accSpeed * REF / lane.samples / lane.speedLimit) : REF
    if lane.samples > MAX_BUF: lane.accSpeed = lane.accSpeed * MAX_BUF / lane.samples; lane.samples = MAX_BUF

linkCost(seg, query):
    t0 = seg.length / seg.speedLimit
    congestion = clamp(1 - seg.meanRel / REF, 0, 1)
    cost = t0 * (1 + K_CONGESTION * congestion)              # or t0 * (1 + 0.15 * (V/C)^4)
    cost *= seededRange(query.id, seg.id, 0.9, 1.0 + seg.density / 100)
    return cost + turnCost(conn) + laneChangeCost

shouldReroute(veh):
    if (tick + veh.id) % REROUTE_PERIOD != 0 and not routeAheadBlocked(veh, 3): return false
    if veh.inCommittedSection: return false                  # ramps, the last few steps
    return true
acceptRoute(new, old): return new.cost < old.cost * (1 - HYSTERESIS)
```

The integer reference scale (REF, for example 10,000) keeps the measured speeds deterministic. One mod
for a shipped city builder uses that scale, a congestion factor of 4, and a ±10% random term. The
seeded range above is how the same mod reproduces the base game's own route spread.

## Lane choice and MOBIL

```text
chooseLane(veh, segment):
    cands = [l in segment.lanes if canReach(l, veh.route.step(+2))]
    return argmin over cands of (laneTypePenalty(l), queued(l) + laneChangesNeeded(veh, l), l.index)

mobilOK(me, target):
    if me.sinceLastChange < LC_COOLDOWN (about 4 s): return false
    newFollowerAcc = idm(newFollower, leader = me)
    if newFollowerAcc < -B_SAFE (4 m/s²): return false        # safety holds even for selfish drivers
    gain = acc_after(me) - acc_now(me) + bias(direction)       # keep-right bias about 0.2 m/s²
    harm = p * ((acc_now(oldFollower) - acc_after(oldFollower)) + (acc_now(newFollower) - newFollowerAcc))
    return gain > harm + A_THR (0.2 m/s²)                       # p in 0..0.5
```

Evaluate every candidate lane with fresh decision state. On highways, change one lane at a time, and keep
lanes on entry and exit. Give on-ramp traffic a negative bias so that it merges.
