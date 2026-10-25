# Game traffic source map

Use this file to audit a rule, not as more procedure. Every source below was opened on 2026-10-25.
Source trees were read for their behaviour, not copied. OpenTTD is GPLv2, Citybound AGPLv3, A/B Street
Apache-2.0 and TM:PE MIT; the traffic-simulation.de licence was not checked. The pseudocode is written
fresh.

## Representation and the lane graph

- SimCity 4 Network Addon Mod, [automata documentation](https://www.sc4nam.com/docs/feature-guides/automata-plugins/).
  SimCity 4 is not agent-based. Its cars are a visual approximation with a loose correlation to the
  statistics, and changing them does not change capacity or commutes.
- [Game Design Deep Dive: Traffic systems in Cities: Skylines](https://www.gamedeveloper.com/design/game-design-deep-dive-traffic-systems-in-i-cities-skylines-i-)
  (Game Developer, 2015, by the developers).
  - Segments with bezier lanes, and vehicles following target points along them.
  - Lanes are chosen early and kept, and freer lane changing produced "total traffic chaos".
  - At junctions, a first-come first-served check over projected segments.
  - Car movement runs about four times per second, and rendering interpolates.
  - Stuck vehicles are teleported back to their origin.
- SUMO, [road networks](https://sumo.dlr.de/docs/Networks/SUMO_Road_Networks.html),
  [intersections](https://sumo.dlr.de/docs/Simulation/Intersections.html) and
  [traffic lights](https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html).
  - Connections from an incoming lane to an outgoing lane, with an internal `via` lane; lane 0 is
    rightmost.
  - Per-connection `foes` and `response` bitsets.
  - Junctions kept clear by default; turn speed limited to `sqrt(radius × 5.5)`.
  - One phase character per link, with lower-case `g` meaning green that yields; a 90 s default cycle.
- [Traffic](https://github.com/krzychu124/Traffic), a lane-connection mod for Cities: Skylines II. Its
  known issues: connections are removed when a road is replaced or reversed, and none are generated
  for newly added roads.
- OpenTTD [yapf_road.cpp](https://github.com/OpenTTD/OpenTTD/blob/master/src/pathfinder/yapf/yapf_road.cpp)
  and [roadveh_cmd.cpp](https://github.com/OpenTTD/OpenTTD/blob/master/src/roadveh_cmd.cpp):
  - path nodes keyed by tile and track direction, with a route cache of 8 decisions;
  - the blocking vehicle found among nearby same-direction vehicles, ties broken by vehicle id;
  - after 1,480 ticks blocked, the vehicle drives through its blocker;
  - extra frames in curves.
  Studied, not copied.

## Vehicle stepping and car-following

- Martin Treiber, [IDM reference page](https://traffic-simulation.de/info/info_IDM.html) and the
  [Intelligent driver model](https://en.wikipedia.org/wiki/Intelligent_driver_model) article, which
  copies the formulas the page shows as images.
  - The parameter table: a = 0.3 m/s² is "very low" to enhance stop-and-go, and realistic values are
    0.8–2.5 m/s²; b around 2 m/s²; T 0.8–2 s; s0 2 m.
  - The ballistic update with an exact stop.
  - Update steps below 0.5 s give essentially the same result.
- [traffic-simulation.de source](https://github.com/movsim/traffic-simulation-de) (`js/models.js`,
  `js/road.js`).
  - The gap clamped at s0, a braking floor, and a linear free term above v0.
  - Two-phase updates; per-road sorting with a virtual far leader.
  - A recorded bug of stale neighbours after merges, fixed by re-sorting after every transfer.
  - A recorded bug of a lane-change flag leaking between candidates.
  - Junction conflict checks by time to collision.
- [Citybound microtraffic](https://github.com/citybound/citybound/blob/master/cb_simulation/src/transport/microtraffic/mod.rs)
  (an inactive project).
  - Per-lane sorted cars, with the next lane's first car projected back as an obstacle.
  - A red light as a stationary obstacle; each car takes the minimum of the IDM terms.
  - Logic and route searches every 10th tick, staggered by id.
- SUMO, [car-following models](https://sumo.dlr.de/docs/Car-Following-Models/index.html) and
  [vehicle types](https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html).
  - The Krauss safe-speed default at a 1 s step, with an action step length for less frequent
    decisions.
  - A minor-link time gap of 1 s by default.
- [Nagel–Schreckenberg model](https://en.wikipedia.org/wiki/Nagel%E2%80%93Schreckenberg_model) and
  [Gipps' model](https://en.wikipedia.org/wiki/Gipps%27_model). Secondary summaries of the original
  papers, which were not opened.
- A/B Street, [discrete-event traffic](https://a-b-street.github.io/docs/tech/trafficsim/discrete_event/index.html).
  - Smooth acceleration added little when only arrival times matter.
  - A lot of processing goes into agents retrying to start a turn as jams form.
  - The documented numbers are out of date.
- Glenn Fiedler, [Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/). A fixed step
  with an accumulator, the spiral of death, and interpolation.
- Liikennematto, [dev blog one](https://matiasklemola.com/liikennematto-dev-blog-one) (2020). Moving
  every car at once caused collisions, which giving cars individual turns fixed. A hobby prototype.

## Lanes and lane changes

- Treiber, [MOBIL reference page](https://traffic-simulation.de/info/info_MOBIL.html). The incentive and
  safety criteria with both followers; p 0–0.5, b_safe 4 m/s², threshold 0.2 m/s², bias 0.2 m/s²; even
  selfish drivers obey the safety criterion. The paper is Kesting, Treiber and Helbing,
  [TRR 1999](https://journals.sagepub.com/doi/abs/10.3141/1999-10) (2007); only its abstract record was
  opened.
- TM:PE, [Highway junction rules](https://github.com/CitiesSkylinesMods/TMPE/wiki/Highway-Junction-Rules),
  [Traffic on highways not behaving properly](https://github.com/CitiesSkylinesMods/TMPE/wiki/Traffic-on-highways-not-behaving-properly)
  and [Nodes, segments, lanes](https://github.com/CitiesSkylinesMods/TMPE/wiki/Nodes,-Segments,-Lanes).
  - On highways: one lane at a time, stay in lane on entry and exit, and lane parity.
  - Merging at the last node before a junction causes jams.
  - Dynamic lane selection jams the middle lane above 50%, with 30–40% working well.
  - In the base game, lanes change only at nodes.
- TM:PE [VehicleBehaviorManager](https://github.com/CitiesSkylinesMods/TMPE/blob/master/TLM/TLM/Manager/Impl/VehicleBehaviorManager.cs).
  Chooses the best lane over four future path positions, gives each vehicle a static random value for its
  lane-selection share, and filters debug logs by vehicle and node.
- A/B Street [router.rs](https://github.com/a-b-street/abstreet/blob/main/sim/src/router.rs). Lane
  penalties are compared in order, and queued vehicles are combined with lane changes, so a car does not
  switch lanes just to pass one car.
- Cities: Skylines II, [Morning Dew patch notes](https://www.paradoxinteractive.com/games/cities-skylines-ii/news/morning-dew)
  (2026). Vehicles switched lanes too late, causing jams; a legal U-turn had cost 0 and was raised.

## Junctions and gridlock

- A/B Street [intersection.rs](https://github.com/a-b-street/abstreet/blob/main/sim/src/mechanics/intersection.rs)
  and [queue.rs](https://github.com/a-b-street/abstreet/blob/main/sim/src/mechanics/queue.rs).
  - The entry check order: conflicting accepted turn, then signal or stop policy, then exit
    reservation.
  - The reserved-length rule, with an assertion that reserved length stays non-negative.
  - Blocked-by tracking and cycle detection; urgent priority for overflowing queues.
  - Two-road junctions may block the box.
  - Ordered waiting containers, wake-ups and retry counters.
  The [gridlock page](https://a-b-street.github.io/docs/tech/trafficsim/gridlock.html) lists
  block-the-box and cycle detection as remedies.
- Dresner and Stone,
  [A Multiagent Approach to Autonomous Intersection Management](https://www.cs.utexas.edu/~pstone/Papers/bib2html-links/JAIR08-dresner.pdf)
  (JAIR 2008).
  - Reservation tiles in an n × n grid, tested by internal simulation of the crossing.
  - The reservation-distance gate that protects the front car, retry timeouts and safety buffers.
  - Delay cut by two orders of magnitude against signals.
  - The exact timeout formula did not extract cleanly and is not used.
- SUMO, [Why vehicles are teleporting](https://sumo.dlr.de/docs/Simulation/Why_Vehicles_are_teleporting.html).
  - After 300 s, the lane head below 0.1 m/s is moved to the next free edge or removed, with a warning
    and a teleport count.
  - The advice is to fix priorities, signal timings or demand.
- TM:PE, [Toggle despawn](https://github.com/CitiesSkylinesMods/TMPE/wiki/Toggle-Despawn),
  [Enter blocked junctions](https://github.com/CitiesSkylinesMods/TMPE/wiki/Enter-Blocked-Junctions) and
  [Bulldozing road causes vehicles to despawn](https://github.com/CitiesSkylinesMods/TMPE/wiki/Bulldozing-road-causes-vehicles-to-despawn-nearby).
  - Despawning keeps flow but hides bottlenecks.
  - Blocked-junction entry exists for micro-roundabouts.
  - Vehicles despawned instead of rerouting after edits.
- TM:PE [car step patch](https://github.com/CitiesSkylinesMods/TMPE/blob/aadca33ece4b60e1bfc9a6ca8aec573ae8a04898/TLM/TLM/Patch/_VehicleAI/_CarAI/SimulationStepPatch.cs).
  It reproduces the base game's distance detail levels at about 500 m and 1,100 m, and its block-counter
  release. The skill states only that behaviour.
- [Cities: Skylines Wiki, Traffic](https://skylines.paradoxwikis.com/Traffic). A community source:
  heavy traffic in red is not necessarily a problem area, and wider spacing between junctions reduces
  gridlock.
- Paradox Interactive, [Cities: Skylines II traffic AI](https://www.paradoxinteractive.com/games/cities-skylines-ii/features/traffic-ai).
  Lane balancing, and roundabout entry yielding to circulating traffic. A feature page without numbers.

## Routing under congestion

- TM:PE [CustomPathFind.cs](https://github.com/CitiesSkylinesMods/TMPE/blob/master/TLM/TLM/Custom/PathFinding/CustomPathFind.cs),
  [TrafficMeasurementManager.cs](https://github.com/CitiesSkylinesMods/TMPE/blob/master/TLM/TLM/Manager/Impl/TrafficMeasurementManager.cs)
  and [AdvancedVehicleAI.cs](https://github.com/CitiesSkylinesMods/TMPE/blob/master/TLM/TLM/State/ConfigData/AdvancedVehicleAI.cs).
  - The base game's seeded per-query, per-segment cost factor from 0.9 to 1 + density/100, as the mod
    reproduces it.
  - The mod's congestion term: 1 + 4 × congestion, from per-lane relative mean speed on a 10,000 scale,
    with a ±10% random term and a rescaled sample buffer.
- SUMO, [automatic routing](https://sumo.dlr.de/docs/Demand/Automatic_Routing.html). Rerouting is off
  until a period is set; edge speeds are averaged over 180 steps; a random factor on weights creates route
  variety; there is an option for routing threads.
- [Bureau of Public Roads function](https://arxiv.org/pdf/2005.01610). α = 0.15 and β = 4 as the
  standard choice. A transport-planning curve, not a game measurement.
- [All-or-nothing assignment](https://www.civil.iitb.ac.in/tvm/1100_LnTse/136_lntse/plain/plain.html)
  (course notes). It loads one path and ignores congestion.
- SimCity (2013): [Maxis begins improving the simulation](https://www.gamewatcher.com/2013-15-03-maxis-begins-turning-attention-to-improving-the-simulation-in-simcity)
  (press, 2013) and [Wikipedia](https://en.wikipedia.org/wiki/SimCity_(2013_video_game)) for the launch
  routing that took the shortest rather than the least congested route. Then
  [Update 7](https://www.gamewatcher.com/2013-21-08-simcity-traffic-tuning-update-7-0-releases-august-22nd)
  for agents swarming one business until each was guaranteed an open slot before leaving. Both are
  press accounts of Maxis posts.
- [GDC 2012: Breaking down SimCity's GlassBox engine](https://gamedeveloper.com/design/gdc-2012-breaking-down-em-simcity-em-s-glassbox-engine).
  A target of 10,000+ agents.

## Scale

- SUMO, [mesoscopic model](https://sumo.dlr.de/docs/Simulation/Meso.html). Queues on 100 m segments, up
  to 100× faster, with junction control off by default.
- The order to buy scale, the fixed-time-first signal default, and the defaults table in
  [scale and tuning](scale-and-tuning.md) are conclusions drawn from the sources above. Signal timing
  optimisation was not researched.

## Not relied on

Not opened or not verified:

- the Cities: Skylines vehicle caps, which are community-reported;
- the SimCity (2013) capacity-weighting percentages and engine slides;
- the internals of Cities: Skylines II, Transport Fever and Mini Motorways;
- the original Gipps and Nagel–Schreckenberg papers;
- the reroute-oscillation research.

No source gives a formal no-gridlock guarantee for a general network, so block-the-box, cycle breaking
and counted timeouts are defences, not proofs.

Last checked 2026-10-25.
