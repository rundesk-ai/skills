# Duplication and dead code

Each pattern below was written in good faith, one reasonable edit at a time, and each took a later
review round to find. Every bad version compiles, passes its tests and reads fine in its own file; the
cost shows up when the rule changes and only one copy is updated.

## One formula, written where its inputs live

```csharp
// Bad: the same physics typed again wherever it was needed, each copy a place the next fix misses.
var ahead = (Spec.MaxSpeed * Spec.MaxSpeed / (2f * Spec.Braking)) + CurveStep;     // Trucks.cs
if (pos[other] + (speed * speed / (2f * braking[type[other]])) + MinGap > from)    // Parking.cs
var stopping = (v.Speed[car] * v.Speed[car] / (2f * _braking[v.Type[car]])) + 1f;  // Bays.cs
_retry[t] = 5f;                                                                    // three call sites

// Good: one home on the type that owns the inputs, and every caller reads it.
public static class Spec
{
    public const float BrakingDistance = MaxSpeed * MaxSpeed / (2f * Braking);
    public const float RetrySeconds = 5f;
}

private float StopDistance(int car) => Speed[car] * Speed[car] / (2f * _braking[Type[car]]);
```

Search by the inputs (`Braking`, `Speed\[.*\] \*`), not by a name you would give the result: a copy
written by someone else has another name or none.

## A lookup copied with its tolerance changed

```csharp
// Bad: three "find the lane at this point" loops, one with a different tolerance. Depot siting
// accepted a point 0.8 m off the lane that the planner then could not find.
private (int, float) LaneAt(Vector2 p) { /* QueryNear(p, 1f) ... distance < 0.5f */ }   // Planner
private int AnchorLane(Vector2 p)       { /* the same loop, inline, distance < 0.5f */ } // Planner
internal static (int, float)? LaneUnder(Network n, Vector2 p) { /* ... distance < 1f */ } // Siting

// Good: one query on the type that owns the data, its tolerance a parameter with one default.
public (int Lane, float S)? LaneAt(Vector2 point, float tolerance = 0.5f) { ... }
```

When the copies already disagree, merging them is a behaviour change: decide which value is right,
prove it with a test that fails first, and say so in the change.

## A method copied to change one end

```csharp
// Bad: the same splice twice, mirror images. A fix to one end's bookkeeping misses the other.
public void Enqueue(int car, int lane)      { /* ahead = tail, behind = none, update tail ... */ }
public void EnqueueFront(int car, int lane) { /* ahead = none, behind = head, update head ... */ }

// Good: the difference is a parameter; the public names stay because callers read better.
public void Enqueue(int car, int lane) => Link(car, lane, ahead: Tail[lane], behind: None);
public void EnqueueFront(int car, int lane) => Link(car, lane, ahead: None, behind: Head[lane]);
```

The same holds for two draws that differ only in which entries are allowed: one
`Draw(ReadOnlySpan<bool> allowed, ...)`, two one-line callers.

## The view re-derives the model's rule

```csharp
// Bad: the game layer recomputes a sim rule from raw fields. When the sim's skew floor changes,
// the painted gap no longer matches where cars stop.
var sine = MathF.Max(0.2f, MathF.Abs(Cross(c.Along, c.Across)));
var reach = c.Reach + (halfWidth * MathF.Abs(Dot(c.Along, c.Across)) / sine) + margin;

// Good: the model exposes the rule, and every view, preview and tool calls it.
var reach = crossing.ClearReach(halfWidth, margin);
```

A preview or ghost is the sharpest case: build it by calling the same steps the real edit takes, or it
shows a result the edit does not produce.

## A list of cases where a predicate owns the set

```csharp
// Bad: the set restated as cases. Bike was added to the kerb rule later; this copy never learned of
// it, and bike couriers stopped being offered kerbside drops, with no error anywhere.
if (vehicle.Class is VehicleClass.Van or VehicleClass.Truck && bay.Length >= vehicle.Length) ...

// Good: the predicate that owns the set, so the next class added updates every caller.
if (VehicleClasses.MayUseKerb(vehicle.Class) && bay.Length >= vehicle.Length) ...
```

Search for the enum's cases (`VehicleClass.Van or`), not for the predicate's name. An exhaustive
`switch` that maps every case to a value (a width, a colour) is a mapping, not a copy of a predicate.

## One classification, worked out once

```csharp
// Bad: the map colour and the tooltip classify the same ratio on their own, and already disagree:
// a shelf the map draws red reads "Low" in its tooltip.
var shade = ratio >= Stock.FullAbove ? 0f : ratio >= Stock.LowAbove ? 0.5f : 1f;   // MapLayer
var word = ratio >= Stock.FullAbove ? "Full" : ratio >= 0.1f ? "Low" : "Empty";    // Tooltip

// Good: classify once into an enum; each output maps the enum.
public static StockBand Band(float ratio) => ratio >= FullAbove ? StockBand.Full : ratio >= LowAbove ? StockBand.Low : StockBand.Empty;
```

## A component's own copy of another's state

```csharp
// Bad: the panel keeps the tool's mode and level and re-applies the tool's clamp. The tool resets the
// level when a mode forbids it; the panel's copy does not, so it shows a level the tool is not using.
private int _level;
case "level_up": _level = Math.Min(_level + 1, Levels.Highest); tool.SetLevel(_level); break;

// Good: the tool owns its state and rules; the panel asks and reads.
case "level_up": tool.SetLevel(tool.Level + 1); break;
label.Text = $"{tool.Mode}, level {tool.Level}";
```

A copy made on purpose to cross a boundary, such as a snapshot handed from the simulation thread to
the render thread, is not this: it is taken whole, at one moment, and never edited by its reader.

## A second subsystem copied from the first

```csharp
// Bad: the forklift was built by copying the crane, its clearance rule and margin with it.
public static float CraneClearance(float hook) => hook - CraneSpec.SpreaderDepth - 0.4f;
public static float ForkliftClearance(float mast) => mast - ForkliftSpec.CarriageDepth - 0.4f;

// Good: one rule; each subsystem passes what genuinely differs.
public static float Clearance(float top, float depth) => top - depth - Lifting.SafetyMargin;
```

## Removing something leaves its references behind

Not duplication, but found by the same review: deleting an entity from its main collection while
other structures still hold its id (a ban list, an index, a cache, a selection) leaves stale entries
that later code trusts. When you write the removal, list every structure that stores the id and
clear it there too, and add a test that removes one and uses what referred to it.

## Built ahead of its reader

```csharp
// Bad: computed every rebuild, published, tested, and read by nothing in the game.
public ImmutableArray<TourPlan> Tours { get; private set; } = [];
public sealed record LanePaint(List<PaintLine> Lines, List<HoldBar> HoldBars); // HoldBars never drawn
public readonly record struct BayLoad(Level Level, LoadCause Cause, float Wait, float Occupancy); // Cause, Occupancy unread
public string? LastFailure { get; private set; }   // written on every failure, never read

// Bad: a parameter "for the next slice" that every caller passes as 0.
private static void OutlinePoints(Network n, Arm arm, float from, float to, float offset, float lift, ...)

// Good: the field, record member, enum case or parameter arrives in the change that reads it.
public sealed record LanePaint(List<PaintLine> Lines);
```

The same holds for the shapes that look used because something implements or subscribes to them:

```csharp
// Bad: an interface member nothing calls, so every implementation and test stub must carry it.
public interface IRoutes { bool Crosses(Vector2 a, Vector2 b); IReadOnlyList<int> Stops { get; } }
// Bad: an event with no subscriber, a setter nothing calls, a probe hook nothing sets.
public event Action<int>? ZoomChanged;
public float MapRadius { get; set; }           // only ever read
internal Func<Vector2, bool>? PickOverride;    // always null, so its branch never runs
// Bad: every caller passes the same widening, so the default and its branch are dead.
public float GroundAt(Vector2 p, float widen = 0f) => widen == 0f ? Exact(p) : Widened(p, widen);
```

A test that only exercises the unread output is not a reader: it keeps the code compiling and
covered while nothing ships it, and it is deleted with the code. A snapshot or event that copies state
across a boundary is the commonest place for this: copy a field when the reader is written, not
before.

## The replaced path left behind

```csharp
// Bad: the new name arrived; the old one stayed as an alias, and its helpers stayed with it.
public void Dispatch(int truck) => SendOut(truck);
public int ClashAt(int a, int b) { ... }           // ClashOtherAt holds the same points

// Good: callers moved to SendOut and ClashOtherAt in the same change; Dispatch and ClashAt
// deleted, then every private helper only they called, until nothing new is unused.
```

Deleting one public member leaves its private helpers unused. Removing them in the same change is
what saves the next review round; with IDE0051 raised (below), the build lists them.

## The toolchain sees private code only

Verified on .NET 10 (SDK 10.0.301) with `AnalysisLevel` `latest-recommended`,
`EnforceCodeStyleInBuild` and `TreatWarningsAsErrors`:

| Code | Reported by default | With the three rules raised |
|---|---|---|
| private method with no caller | no | IDE0051 |
| private field or property written, never read | only a field assigned a constant (CS0414) | IDE0052 |
| unused parameter, any visibility | no | IDE0060 |
| event never raised | CS0067 | CS0067 |
| event raised, with no subscriber | no | no |
| `internal` or `public` member with no caller | no | no |

```ini
# .editorconfig
[*.cs]
dotnet_diagnostic.IDE0051.severity = warning
dotnet_diagnostic.IDE0052.severity = warning
dotnet_diagnostic.IDE0060.severity = warning
```

With warnings as errors, raising them fails the build until the existing hits are fixed, so propose
the change to the project's owner with its first findings rather than slipping it into unrelated
work. A record that declares its own `PrintMembers` is a known IDE0051 false positive. Nothing reports
an unused `public` or `internal` member, which is where most dead code in a multi-project solution
sits: default to `private`, and for anything wider, search every project, scene and data file for a
caller before adding or keeping it.

## What is not duplication

- Two or three plain lines repeated, a loop header, or a guard clause.
- The same number meaning two things (a lateral acceleration and a comfort limit that both happen
  to be 2): give them two names, not one.
- Copies on two sides of a boundary that change for different reasons, such as a save format's
  parser and the runtime type's constructor.
- A test spelling out its own inputs.

Merging these couples rules that were free to diverge; the first change to one of them proves it.
