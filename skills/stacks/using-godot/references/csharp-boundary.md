# The C# boundary

Godot is a C++ engine with a C# layer over it. Read this in any project with a `.csproj`: most of the
surprising behaviour in a Godot C# project happens at that seam. Figures are from Godot 4.7.2 (mono).

## Setting up and building

A project runs from four files; no editor session, solution or import is needed to run it:

```ini
; project.godot
config_version=5

[application]
config/name="Colony"
run/main_scene="res://main.tscn"
config/features=PackedStringArray("4.7", "C#", "Forward Plus")

[dotnet]
project/assembly_name="Colony"
```

```xml
<!-- Colony.csproj: the name matches assembly_name -->
<Project Sdk="Godot.NET.Sdk/4.7.2">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <EnableDynamicLoading>true</EnableDynamicLoading>
  </PropertyGroup>
</Project>
```

plus `main.tscn` and a `Main.cs` holding `public partial class Main : Node`.

```sh
dotnet build                                               # prints compiler errors; use this
"$GODOT" --headless --path . --quit-after 100
```

- **Build with `dotnet build`, and read its output.** `--headless --build-solutions --quit` exits 1 on a
  compile error but prints only "build callback failed"; the errors are in `msbuild_issues.csv` under
  the user data directory's `mono/build_logs/`. With no `.csproj` it builds nothing and exits 0.
- **The engine runs the last built assembly** (`.godot/mono/temp/bin/Debug/<assembly_name>.dll`), never
  your source, and only the `Debug` output: `dotnet build -c Release` is ignored. Check the `.dll`'s
  mtime postdates the edit.
- `Sdk="Godot.NET.Sdk/<version>"` must match the engine exactly. From 4.4 the packages target `net8.0`
  (earlier 4.x: `net6.0`); `TargetFramework` is mandatory. Do not raise it without a reason: Android
  needs .NET 9, and C# projects cannot export to the web.
- A script class is named exactly like its file, case included. The compiler does not check it; the
  first instantiation fails. A `snake_case.cs` file name is exactly this failure.
- **Exporting** needs the .NET export templates for the exact engine version **and a solution file**
  (`dotnet new sln -n Colony && dotnet sln add Colony.csproj`; `.slnx` works). Without the solution the
  export exits 0 and ships a game with no C# assembly.

### "Cannot instantiate C# script because the associated class could not be found"

One message, four causes, and the process exits 0 for each. Check in this order: `dotnet build`
succeeded; the `.dll` exists at `.godot/mono/temp/bin/Debug/<assembly_name>.dll` (with no `[dotnet]`
section the engine looks for `config/name`, spaces included); the class name matches the file name
exactly, case included. A namespace is fine.

## An exception in an engine callback is swallowed

When `_Ready`, `_Process` or a signal handler throws, the runtime logs the exception and the engine
carries on to the next frame. **The process does not stop and the exit code stays 0.** The symptom is
never a crash; it is a feature that silently does nothing, with the cause in the log above whatever you
were looking at.

```sh
grep -n -e 'ERROR' -e 'Exception' -e '   at ' run.log | head -40
```

- **A partially constructed scene is normal after a throw.** If `_Ready` threw halfway, everything
  before the throw exists and everything after does not.
- A `TargetInvocationException` or `TypeInitializationException` names only the call that failed; its
  inner exception is the finding.
- An `async void` handler's exception is logged the same way. A fire-and-forget `Task` that throws logs
  **nothing**; await every task, or route its failure to `GD.PushError`.

## Wrapper and native object

A `Node` in C# is a wrapper around a native object, and they die at different times: the native one on
`Free`/`QueueFree`, the wrapper when the garbage collector gets to it. So a reference to a freed node is
not null, and touching it throws `ObjectDisposedException`. `GodotObject.IsInstanceValid(node)` asks
whether the native object is still reachable; set your own field to `null` when you free what you own.

- **The garbage collector never frees a `Node`.** A thousand unreferenced `new Node()` stayed alive as
  orphans and were reported leaked at exit. Every node is freed explicitly or lives under one that is;
  a node taken out with `RemoveChild` or held in a pool leaks unless freed. `RefCounted` objects are
  collected once no C# field holds them.
- **`Dispose()` is not `Free()`.** It drops the wrapper; the node stays in the tree, still drawing, and
  `IsInstanceValid` turns false. Never `using` or `Dispose` a node you meant to destroy.
- **A script class needs a parameterless constructor.** Without one, instantiating its scene logs
  `MissingMemberException` and returns a plain `Node` with no script. Pass data through a setup method.
- `new Agent()` gives the script's code defaults and no children; the scene's saved values and children
  come from `GD.Load<PackedScene>(...).Instantiate<Agent>()`. `GD.Load` returns one cached instance.

## Signals and events

- **Engine signals** (`timer.Timeout += OnTimeout`) and connections made with `Connect(SignalName.X,
  Callable.From(...))` are removed when the receiving node is freed.
- **A custom `[Signal]` subscribed with `+=` is not.** It keeps calling the method on the freed receiver,
  which throws `ObjectDisposedException`. Subscribe in `_EnterTree` and `-=` in `_ExitTree`, or use
  `Connect`.
- **A plain C# `event` is a hundred times cheaper** than a signal — 0.6 ns against about 80 ns per
  emission in an export — but the engine cannot see it: no editor wiring, no `ToSignal`, no
  auto-disconnect. Use C# events or a dirty list for simulation output, signals for engine and editor
  wiring.
- Emit with the generated `EmitSignalTicked(i)`, which allocates nothing; `EmitSignal(SignalName.Ticked,
  i)` allocates a params array, and `EmitSignal("Ticked", i)` also converts the string.

## Names the engine looks up by string

**Engine members are registered under their snake_case name; members you declare in C# under their C#
name, exactly.** `CallDeferred("AddChild", n)` fails while `CallDeferred(Node.MethodName.AddChild, n)`
works — and `call_group("guards", "enter_alert_mode")` silently skips a C# `EnterAlertMode()`, as do
`has_method`, `has_signal` and `get` from GDScript with the snake_case name. Use the generated
`MethodName`, `PropertyName` and `SignalName`, or `Callable.From(() => AddChild(n)).CallDeferred()`, which
avoids the string entirely.

**A `string` where the engine takes a `StringName` is converted on every call, in every build:**
`Input.IsActionPressed("select")` costs 365 ns and 96 bytes; with a cached `static readonly StringName
Select = "select";` it costs 10 ns and nothing. The same applies to `IsInGroup`, `GetNode<T>("Path")`
(about 600 ns), `Get("position")` and `node.Name == "x"` (a new wrapper and a conversion, 760 ns). Use
the generated `MethodName`, `PropertyName` and `SignalName` constants, cache the rest, and cache node
references in `_Ready`.

## Marshalling cost

Measured in an exported release build, per operation:

| Operation | Cost |
|---|---|
| `List<int>[i]` / `Godot.Collections.Array<int>[i]` | 0.3 ns / 2.3 ns |
| `Dictionary<int,int>` / Godot `Dictionary<int,int>` lookup | 1.3 ns / 28 ns |
| `node.Position` get / `child.Call(MethodName.GetPosition)` / `child.Get("position")` | 2.2 / 47 / 374 ns |
| `GetChildren()` on 1,000 children; `GetNodesInGroup` on 1,000 | 4.9 µs; 6.1 µs and 1.25 KB, per call (editor binary) |
| MultiMesh `SetInstanceTransform` / one `Buffer = float[]`, per instance | 17 ns / 3.5 ns |
| `new Node3D` + `AddChild` + `Free`; `Instantiate` of a 2-node C# scene + `AddChild` + `Free` | 0.8 µs; 4 µs |

- **Keep simulation state in `System.Collections.Generic`**, arrays and structs. Godot collections are
  for `[Export]`, signals and engine calls, and converting between the two marshals every element.
- **Keep your own registry of view nodes** keyed by entity id; do not query the tree per tick.
- `Vector3`, `Transform3D` and the other math types are C# structs, free until handed over. Do the
  arithmetic in C#; set each node's `Position` once per frame (`GlobalPosition` costs twice as much).
- Packed arrays are plain C# arrays, and hundreds of engine methods take `ReadOnlySpan<T>`; look for
  the span overload before allocating a temporary array.
- **Measure in an export, not a run of the editor binary.** Engine calls, Godot collections and signals
  were 5 to 35 times faster in an exported release, so an editor-run profile exaggerates the boundary
  and gets ratios wrong — a Godot `Array<int>` read is 8 times a `List<int>` read in the export, 40 to
  200 times from the editor binary.

## Threads and await

- **A node in the tree touched from another thread does not throw.** The write is ignored, a read
  returns a default such as `(0, 0, 0)`, and the log says `The caller thread can't call the function
  'set_position()' on this node`. Snapshot what a worker needs into plain C# data on the main thread,
  and apply results there with `Callable.From(() => ...).CallDeferred()`.
- **`await` resumes on the main thread** (the engine installs a `SynchronizationContext`), **but only once
  per frame**: ten sequential `await Task.Run(...)` took 24 frames. Never chain awaits inside a tick.
- After `ConfigureAwait(false)` the rest of the method runs on a pool thread, where every engine call
  falls under the first rule; a later `ToSignal` hung in one test project. Do not use it in node code.

## Runtime and GC

- **The editor binary runs your code on its own .NET runtime** (`rollForward: LatestMajor`): a `net8.0`
  project ran on .NET 10 from the editor and on a bundled .NET 8 in the export. Profile and soak-test
  the export.
- GC settings in the `.csproj` (`ServerGarbageCollection`, `ConcurrentGarbageCollection`) are ignored in
  editor and command-line runs and honoured in exports; test one in development with
  `DOTNET_gcServer=1` or `DOTNET_gcConcurrent=0`. Keep the default: under 4 MB of garbage a frame, server
  GC produced a 58 ms frame against about 20 ms for workstation concurrent. Cut the allocation instead.
- **The first call to a code path pays for the JIT** — 11 ms from the editor binary, 2.4 ms in the export
  for a small LINQ method. A system that first runs mid-game (the first famine, the first war) hitches;
  call it once on dummy data while loading.
- `#if TOOLS` code runs in editor and command-line runs and never in an export.
- A project that keeps an engine-free simulation layer means it: no `Godot` type, `Node` or `Vector3` on
  that side, or its tests need an engine to run.

## Assembly reload

Reload happens **only in the editor**, when you rebuild while it is open — `[Tool]` scripts, plugins, and
a game run from the editor. `static` state resets, and signal delegates the engine cannot serialize are
dropped silently (visible with `--verbose`): a handler that stops running after a rebuild is this.
