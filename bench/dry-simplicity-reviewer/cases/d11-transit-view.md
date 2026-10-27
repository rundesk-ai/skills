+++
subject = "dry-simplicity-reviewer"
kind = "quality"
difficulty = "medium"
fixture = "transit"
expect_clean = false
cases_version = 1
key = """
Scoped to one component, the way a review round per area runs: the brief names game/ only. The measure is whether a rule restated in the scope is caught when its home, and its drifted value, sit outside the scope.
must:
  M1 game/CrossingView.cs Reach re-derives Crossing.SquareReach from src/Transit.Sim/Crossing.cs instead of calling it, and its copy already disagrees: a skew floor of 0.25 against Crossing.MinSine 0.2. Hit only when the review names the sim's SquareReach (or MinSine) as the home and the disagreement, or the fix is to call crossing.SquareReach.
  M2 RoadView.EdgeLine's `lift` parameter is passed 0f by both callers.
  M3 RoadView.Draw's `height` parameter is passed 0f by its only caller, GameLoop.Frame.
decoys (reporting any as dead or as duplication to merge is a false positive):
  D1 GameLoop's public methods with no caller in the repository (SaveRoute, LoadRoute, DepotAt, CarArrives, AddRoad, AddGate, PlaceDepot, LayTrack) are the host engine's entry points, as the class says.
  D2 Canvas's lists are read by the host engine.
  D3 The repeated string.Create(CultureInfo.CurrentCulture, ...) calls in Hud are plain formatting.
taste:
  T1 culture choices in labels; T2 naming.
extras (real but not core; neither hit nor false positive):
  X1 any finding outside game/ reported as a note, such as SegmentMarkings.StopLines that RoadView never draws.
  X2 GameLoop.SelectedRoute defaults to -1 and indexes a route list.
"""
+++
Look for duplication, redundancy and dead code in `game/`, the view layer, and tell me what is worth consolidating or removing there.
