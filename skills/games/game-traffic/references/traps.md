# Traps

Read this when a traffic symptom has no obvious cause. Each entry gives the symptom, its cause, the
replacement, and the proof that it is fixed.

| Symptom | Cause | Replacement | Proof |
|---|---|---|---|
| Every car stacks in one lane of a wide road | Lane chosen once for the final turn and kept | Per-segment choice with a 2–4 step lookahead and a queue term | Three-lane straight, even demand: occupancies within 20% |
| Lane changes at the last metre block the junction or exit | Strategic changes considered only on the final segment | Choose the target lane at segment entry; mandatory-change bias | No vehicle stopped in a through lane waiting to change |
| Cars overlap or tunnel at high game speed | dt scaled with game speed | Fixed dt ≤ 0.5 s, more steps per frame, a step cap, clamped gap | 1×, 4×, 16× give matching trajectories, gaps ≥ 0 |
| Two cars take one cell or junction slot in a tick | Discrete moves checked against old state, applied without arbitration | Arbitrate in stable order, or reserve before moving | Conflicting approaches to an empty junction: one accepted |
| Junction locks; a car sits inside it | Entry checked against the junction only | Reserve exit-lane length before entry | Saturated grid: nobody stopped inside while a cross stream waits |
| Roundabout or ring of close junctions gridlocks | Circular wait; strict block-the-box makes everyone wait | Blocked-by cycle detection, one member proceeds; urgent overflow; wider spacing | Scripted four-arm deadlock resolves with no removal |
| Vehicles vanish; city statistics drift | Timeout despawn without accounting | Removals counted by reason, trip settled, logged | `spawned == active + arrived + removed` every tick of a soak |
| Players cannot find the bottleneck | Removal too eager, cannot be disabled | Long head-only timeout, a toggle, a removal heatmap | With removal off, the jam stays visible at the faulty junction |
| One road carries everything; its parallel stays empty | All-or-nothing routing without congestion | Congestion factor plus seeded per-query perturbation | Equal parallel routes carry 40–60% each |
| Traffic sloshes between two routes each cycle | Everyone reroutes on the same fresh snapshot | Smoothed speeds, staggered cohorts, hysteresis | Route split converges instead of alternating |
| Route recompute storm after an edit or a jam | Every affected vehicle searches in the same tick, unbounded | Local invalidation, queued requests with a budget, bounded search, cached prefix | Path requests per tick stay under budget when a main road is bulldozed |
| Vehicles despawn when a road ahead is bulldozed | Invalid route triggers removal | Reroute from the current lane; remove only when no route exists | Zero removals while an alternative exists |
| Replays or multiplayer diverge | Hash-map iteration, float ties, unseeded random numbers, writes in thread order | Id order, ordered containers, ties by vehicle id, seeded perturbation, integer costs | Same save, same hash at tick N |
| Leaders wrong after merges | Lane list not re-sorted after inserting a vehicle | Re-sort and re-resolve after every transfer | Assert lanes sorted after every phase |
| Unsafe lane changes appear depending on history | Decision flag reused across candidates | Fresh decision state per candidate | A candidate that fails MOBIL after one that passes is refused |
| Lanes lose connections after a road edit | Overrides tied to lane indices that change on replace or reverse | Regenerate defaults; re-apply by lane meaning; flag dead-end lanes | After replace and reverse, validation finds no dead-end lane |
| Stop-and-go waves everywhere; sluggish cars | Reference IDM parameters copied, a = 0.3 m/s² | a = 0.8–2.5, b ≈ 2, T = 1.0–1.5, v0 from the limit | A queue leaving a red light reaches the limit within the expected distance |
| Cars take turns at highway speed | v0 capped by the speed limit only | Curve-speed cap with look-ahead braking | Speed traces slow before every tight turn |
| Overlay is red on busy roads that flow | Coloured by count or volume | Colour by mean speed relative to the limit; volume as a separate view | A flowing road at capacity reads green to yellow |
| A front car waits forever at a reservation junction | Followers win reservations first | Reservation-distance gate plus retry timeouts | Front-car wait bounded under saturated demand |
| CPU spent on waiting cars during jams | Every waiting car retries every tick | Wake on release events, or back off | Junction checks scale with state changes, not with waiting cars |
| Vehicles swarm one destination, then circle | Destination chosen without a slot | Claim the destination or parking slot before departure | Vehicles circling for parking stay under a bound |
