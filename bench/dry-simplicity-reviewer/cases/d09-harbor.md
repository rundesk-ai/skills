+++
subject = "dry-simplicity-reviewer"
kind = "quality"
difficulty = "complex"
fixture = "harbor"
expect_clean = false
cases_version = 1
key = """
Held out: written after d08-transit was measured and the agent revised, from shapes a later round of the source project found, so the agent was never tuned on it. The measure is how much one round finds, especially dead code that only a member-by-member reader check reveals.
must:
  M1 BerthPlan.Warnings is built and never read (game/QuayView.cs reads only Slots). Hit only when the finding also removes what that leaves unused: the warnings list and the Check call in Planner.Plan, Planner.Check (its only other caller is a test), the private Overhang, the Warning record, the WarningKind enum, and the test AShipThatFitsNowhereIsWarnedAboutTheFirstBerth. Partial when Warnings is reported but any of those is missing.
  M2 ITide.HighWaterAt is called by nothing; Tide and the test stub FlatTide implement it only because the interface demands it.
  M3 CraneSystem.Idle is raised but nothing subscribes to it (ShipArrived, by contrast, has a subscriber in GameLoop).
  M4 CraneSystem.SpeedFactor's setter is never called, so it is always 1 and the divisions by it do nothing.
  M5 CraneSystem.PickOverride is never set, so its branch in Step never runs.
  M6 ShipState.Anchored is never produced, so its case in Fleet.Step never runs.
  M7 Planner.Free's margin default of 0 and its `margin == 0f` branch are never reached: the one caller passes BerthSpec.EndMargin.
  M8 Arc (src/Harbor.Sim/Arc.cs) has no production reader; only the test AnArcsPointsLieOnItsCircle uses it. Both go.
  M9 assets/icons/crane-idle.svg is referenced by nothing (ship.svg is referenced in QuayView; storm.svg and calm.svg by name from data/events.json).
  M10 The comment in Planner.Plan cites docs/design/berthing.md and task BP-12; the repository has no docs folder.
  M11 The crane move time, (distance / TrolleySpeed + 2 * LockSeconds) / SpeedFactor, with its distance, is written in both CraneSystem.Step and EstimateFinish; one private helper.
  M12 Fleet.UnloadFore and UnloadAft are the same pop on a different list; one Unload(List<int>) or a parameter.
  M13 game/QuayView.cs re-derives the clearance Planner.Clearance owns, and its copy already disagrees: it leaves out BerthSpec.KeelMargin, so the quay shows green where the planner refuses the berth. Hit only when the disagreement is named or the fix is to call Planner.Clearance.
decoys (reporting any as dead or as duplication to merge is a false positive):
  D1 WeatherHandlers.OnStorm and OnCalm have no C# caller outside one test, but data/events.json names them and Weather.Fire calls them by reflection.
  D2 assets/icons/storm.svg and calm.svg have no literal path in code; data/events.json names them by stem and GameLoop builds the path.
  D3 Port.SetTickForTests is a documented test seam.
  D4 BerthSpec.KeelMargin and CraneSpec.LockSeconds are both 0.5f with different meanings.
  D5 Fleet.ShipArrived has a subscriber; ITide.LevelAt is called in production, so FlatTide's LevelAt is a legitimate stub.
  D6 GameLoop.AddShip, AddBerth, AddCrane and Frame are the host engine's entry points, documented on the class.
taste:
  T1 culture in labels; T2 LINQ in Plan; T3 naming.
extras (real but not core; neither hit nor false positive):
  X1 Planner.Check calls Clearance and Overhang twice each.
  X2 Planner.Plan warns about berths[0] rather than the berth the ship came closest to.
  X3 EstimateFinish assumes even cranes work fore, as Step does.
"""
+++
Look for duplication, redundancy and dead code across this repository, and tell me what is worth consolidating or removing.
