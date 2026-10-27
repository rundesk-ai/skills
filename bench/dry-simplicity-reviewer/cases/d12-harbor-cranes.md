+++
subject = "dry-simplicity-reviewer"
kind = "quality"
difficulty = "medium"
fixture = "harbor"
expect_clean = false
cases_version = 1
key = """
Scoped to one file. Three of the findings can only be proved by searching outside it, and the decoys are public members whose only callers are outside it.
must:
  M1 The crane move time, (distance / TrolleySpeed + 2 * LockSeconds) / SpeedFactor with its distance, is written in both CraneSystem.Step and EstimateFinish; one private helper.
  M2 CraneSystem.Idle is raised but nothing in the repository subscribes to it (GameLoop subscribes only to Fleet.ShipArrived).
  M3 CraneSystem.SpeedFactor's setter is never called anywhere, so it is always 1 and the divisions by it do nothing.
  M4 CraneSystem.PickOverride is never set anywhere, so its branch in Step never runs.
decoys (reporting any as dead is a false positive):
  D1 CraneSystem.Add, Assign, BusyUntil, EstimateFinish and Count have no caller inside Cranes.cs; GameLoop and Port call them.
  D2 CraneSpec.LockSeconds and BerthSpec.KeelMargin are both 0.5f with different meanings.
taste:
  T1 parallel lists instead of a struct; T2 naming.
extras (real but not core; neither hit nor false positive):
  X1 assets/icons/crane-idle.svg is referenced by nothing, which goes with Idle.
  X2 Fleet.UnloadFore and UnloadAft, outside the scope, are one pop on a different list.
  X3 EstimateFinish assumes even cranes work fore, as Step does.
"""
+++
Review `src/Harbor.Sim/Cranes.cs` for duplication, redundancy and dead code, and tell me what is worth consolidating or removing in it.
