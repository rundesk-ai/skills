+++
skill = "using-csharp"
cases_version = 2
kind = "quality"
difficulty = "complex"
fixture = "depot"
steps = 4
rubric = """
Graded once, on the tree after all four steps, against the base. Each step was a fresh agent with no memory of the others.
R1  Step 1 decides whether the car behind can stop with Parking's existing rule (StopsShortOf, StopDistance or CanPullOut), not a new speed*speed/(2*braking) expression.
R2  Step 1's 90 seconds become ticks through Clock.Ticks, not a new seconds * Clock.TicksPerSecond expression.
R3  Step 2's stopping distance is worked out in the simulation and the HUD calls it; game/ contains no braking formula of its own.
R4  Step 2's "stops or passes" calls the simulation's one dwell rule (DwellFor, or a member built on it); the freight-only-and-parcel condition is still written once.
R5  Nothing is built for the route display mentioned as later: no member, snapshot field or drawing code whose only purpose is a route on the map.
R6  Step 3 ranks routes with VanSystem.WaitingOn, not a second sum of the parcels waiting at a route's depots.
R7  Step 3 removes the random choice and everything only it used: RandomRoute (and SpawnVan if it only wrapped it), with no test left asserting a random route.
R8  Step 4 derives the large car's hold from the one existing hold (Crossing.StopBack, or the hold Simulation computes) plus a named extra distance; SquareReach and StopBack are not re-derived or copied.
R9  Across the four steps, no member, field, parameter or test helper was added that nothing in production reads (a test-only reader does not count), and nothing a step's own change left unused remains.
R10 `dotnet test` passes on the final tree.
"""
+++
## Step 1

Cars held at the level crossing on the kerb lane can sit there forever. If a car has been held at the
crossing for more than 90 seconds it should give up and turn around, leaving the lane. It may only turn
if the car behind it can stop in time; otherwise it keeps waiting. Add tests.

## Step 2

In the selected-van panel on the HUD, show how far the van needs to stop from its current speed, and
whether it will stop at its next depot or pass it. We'll want the whole route drawn on the map at some
point too.

## Step 3

New vans should go on the route with the most parcels waiting, instead of a random route; ties go to the
lower route id. Remove the random route choice.

## Step 4

Large cars should stop 10 m further back from the level crossing than small cars do.
