+++
subject = "dry-simplicity-reviewer"
kind = "quality"
difficulty = "complex"
fixture = "grid"
expect_clean = false
cases_version = 1
key = """
Held out: built from four shapes a later review round of the source project found after earlier rounds had passed them, none of which the agent's examples named when the case was written. Each must item already causes a visible wrong result.
must:
  M1 Entrances.Connect (src/Grid.Sim/Buildings.cs) tests `Class is RoadClass.Street or RoadClass.Avenue` instead of calling RoadKinds.MayFront, and the copy is missing Local, so a building fronting only a Local road never gets an entrance. Hit only when the review names MayFront as the owner and the missing Local.
  M2 RoadCard.Text classifies the speed ratio separately from TrafficLayer.States, and the two disagree: the card's last cut is a literal 0.15 where the layer uses Congestion.HeavyAbove (0.4), so a road the map draws as jammed reads "Heavy" on its card. One classification (a band) both read is the fix. Hit only when the disagreement is named.
  M3 Hud keeps its own copy of the road tool's class, level and shape and restates the tool's level clamp, and the copy drifts: after the lane button the tool's level is 0 but the HUD still shows the old one, and level_up raises the HUD's level while the tool holds a lane at 0. RoadTool.Shape is written and never read because the HUD shows its own. The HUD should read the tool's state. Hit when the copied state and a drift are named.
  M4 RoadBridges.PierClearance and RailBridges.PierClearance are one rule, height minus deck depth minus the 0.5 m footing margin, written twice with the margin as a literal in each; one rule taking the deck depth.
decoys (reporting any as duplication to merge or as dead is a false positive):
  D1 RoadKinds.Width and Surfaces.ColourOf switch over every class: per-class mappings, not copies of MayFront.
  D2 SimSnapshot copies the speed ratios on purpose, so the game thread never reads arrays the simulation is stepping (documented).
  D3 TrafficLayer's shader states (0, 0.25, 0.5, 0.75) and RoadCard's words are two encodings of one band, not copies of each other; the duplication is the classification, not the encodings.
  D4 GameLoop's methods, RoadTool.Build, Hud.Press and Hud.Lines are the host's entry points, as their summaries say.
  D5 RoadBridges.DeckDepth and RailBridges.DeckDepth differ on purpose.
taste:
  T1 Hud's one case per class button; T2 Shape as a string; T3 naming.
extras (real but not core; neither hit nor false positive):
  X1 Network.Remove leaves the removed road's id in the no-left bans.
  X2 Entrances.Connect accepts only ground-level roads.
  X3 Simulation.Step's placeholder ratio formula.
"""
+++
Look for duplication, redundancy and dead code across this repository, and tell me what is worth consolidating or removing.
