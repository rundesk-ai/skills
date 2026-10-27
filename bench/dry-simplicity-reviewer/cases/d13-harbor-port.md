+++
subject = "dry-simplicity-reviewer"
kind = "quality"
difficulty = "easy"
fixture = "harbor"
expect_clean = true
cases_version = 1
key = """
Scoped to one file whose members are read only from outside it. Nothing in the file is worth changing; the measure is whether searching beyond the scope keeps live code from being called dead.
must: none.
decoys (reporting any as dead or as something to change is a false positive):
  D1 Port.Plan and Port.Tide have no reader in Port.cs; game/QuayView.cs reads both.
  D2 WeatherHandlers.OnStorm and OnCalm are called by name from data/events.json through Weather.Fire.
  D3 Port.SetTickForTests is a documented test seam.
  D4 Port.Wind's public setter is set only by the weather handlers.
  D5 Weather.Load and Fire have no caller in Port.cs; GameLoop calls both.
taste:
  T1 a property with a public setter; T2 the reflection lookup's style.
extras (real but not core; neither hit nor false positive):
  X1 findings outside Port.cs reported as notes.
  X2 Weather.Fire throws on an unknown handler name at the tick it fires rather than when the file loads.
"""
+++
Review `src/Harbor.Sim/Port.cs` for duplication, redundancy and dead code, and tell me what is worth consolidating or removing in it.
