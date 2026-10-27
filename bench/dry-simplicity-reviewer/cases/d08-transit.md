+++
subject = "dry-simplicity-reviewer"
kind = "quality"
difficulty = "complex"
fixture = "transit"
expect_clean = false
cases_version = 1
key = """
A C# simulation and its game layer, seeded with the duplication and dead code a real multi-agent project took several review rounds to find. The measure is how much one round finds, and whether each dead-code removal comes with everything it leaves unused.
must:
  M1 Van braking distance from top speed, MaxSpeed*MaxSpeed/(2*Braking), is written inline twice in src/Transit.Sim/Vans.cs (PassReach and Limit's `ahead`); one named home such as VanSpec.BrakingDistance.
  M2 The van retry wait `5f` is a bare literal in three places in Vans.cs (Spawn, Step's blocked branch, Reroute); one named constant.
  M3 A car's stopping distance, speed*speed/(2*braking[type]), is written inline three times in src/Transit.Sim/Parking.cs (CanClaim, CanPullOut, BrakeFrom); one private helper.
  M4 "The track at a point" is written three times: Planner.TrackAt and the inline loop in Planner.Resolve (both 0.5 m) and Siting.TrackUnder (1 m). Hit only when the review says the copies already disagree on the tolerance; the fix is one query on Network.
  M5 VanSystem.DwellAt and DwellOf state the dwell rule twice and disagree: DwellOf (used by RoundTripSeconds) counts a dwell at freight-only depots a parcel route's vans pass without stopping, and ignores its `stop` parameter, so round trips are overstated. Hit only when the disagreement is named.
  M6 LaneQueue.Join and JoinAtHead are the same linked-list splice mirrored; one Link(car, lane, ahead, behind) behind both.
  M7 TripPicker.Origin and Exit are the same weighted draw over a different allowed set; one Draw(allowed, gates).
  M8 game/CrossingView.cs re-derives Crossing.SquareReach instead of calling it, and its copy already disagrees (skew floor 0.25 against Crossing.MinSine 0.2), so the paint gap does not match where cars stop. Hit only when the disagreement is named, or the fix is to call crossing.SquareReach.
  M9 Stop lines are built and never drawn: SegmentMarkings.StopLines and the StopLine record have no reader (game/RoadView.cs draws only Lines). Hit only when the finding also removes what that leaves unused: Markings.GivesWay (whose only other caller is a test), the private Cut and YieldsOnly, and the GivesWay test in tests/MarkingsTests.cs. Partial when the stop lines are reported but any of those is missing.
  M10 SimSnapshot.QueuedCars and TripsPerMinute are published and never read (game/Hud.cs reads Tick, VanCount and ParkedCars). Hit only when the finding also removes what computes them: QueuedCount, and the _tripsThisMinute/_tripsPerMinute counting in Step (and the TripsAreCountedOverAMinute test). Partial when only the snapshot fields are reported.
  M11 RoadView.EdgeLine's `lift` parameter is passed 0f by every caller.
  M12 VanSystem.LastFailure is written in three places and read nowhere.
  M13 VanSystem.DriveOff is an alias of Retire with no caller.
  M14 The second link of M9's chain: once GivesWay goes, nothing reads the junction control and incident bookkeeping. Junctions.ControlOf, SetControl, the _control map and the Control enum (with GameLoop.AddRoad's control argument), Junctions.Connect, Incident, IsJunction and the _incident map, and Segment.Rank are written and never read. Hit when the review names most of this as going with the stop lines; partial when it names some of it.
decoys (proposing to change or remove any of these is a false positive):
  D1 Handlers.OnRushHour and OnQuietNight have no caller in C#, but data/events.json names them and Events.Fire calls them by reflection. Reporting them as dead is the failure this decoy measures.
  D2 VanSystem.CurveStep is 5f like the retry wait in M2 but means a distance step, not seconds; folding it into the retry constant is wrong.
  D3 RouteSave.Format and Parse mirror each other by necessity.
  D4 Simulation.SetTickForTests is a documented test seam used only by tests.
  D5 The repeated setup in tests/SimulationTests.cs keeps each test readable alone.
taste:
  T1 culture or formatting in the HUD; T2 Dictionary versus SortedDictionary choices; T3 naming.
extras (real but not core; neither hit nor false positive):
  X1 the tick conversion (long)(seconds * Clock.TicksPerSecond) repeated in Parking.GivesUpClaim and GivesUpPullOut.
  X2 Planner.Resolve's 1 m query radius against its 0.5 m tolerance, or the Network bounds query, as a performance note.
  X3 any real behaviour bug in the toy kerb logic (KerbDriver claims before checking GivesUpClaim order, and the like).
"""
+++
Look for duplication, redundancy and dead code across this repository, and tell me what is worth consolidating or removing.
