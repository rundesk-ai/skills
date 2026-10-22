# The C# boundary

Godot is a C++ engine with a C# layer over it. Read this in any project with a `.csproj`: most of the
surprising behaviour in a Godot C# project happens at that seam.

## Building

```sh
grep -E "Sdk=|TargetFramework" *.csproj
"$GODOT" --headless --path . --build-solutions --quit      # exits 1 when the build fails
dotnet build                                               # the same output, without the engine
```

- **The engine runs the last built assembly** (`.godot/mono/temp/bin/<Config>/<Assembly>.dll`), never
  your source. A run without a build shows yesterday's behaviour while you read today's code; check the
  `.dll`'s mtime postdates the edit.
- `Sdk="Godot.NET.Sdk/<version>"` must match the engine version exactly. From 4.4 the packages
  target `net8.0` (earlier 4.x: `net6.0`), so that is the floor; a newer SDK can build it. Do not raise `TargetFramework` without a
  reason: Android needs a newer one, and C# projects cannot export to the web.
- Exporting a C# project needs the .NET export templates for that exact engine version.

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
- Read the exception whole: type, message, **every** `InnerException`, and the stack. A
  `TargetInvocationException` or `TypeInitializationException` names only the call that failed; its
  inner exception is the finding.

## Wrapper and native object

A `Node` in C# is a wrapper around a native object, and they die at different times: the native one on
`Free`/`QueueFree`, the wrapper when the garbage collector gets to it. So a reference to a freed node is
not null, and touching it throws `ObjectDisposedException`. `GodotObject.IsInstanceValid(node)` asks
whether the native object still exists; set your own field to `null` when you free what you own.

A lambda subscribed to a signal (`button.Pressed += () => ...`) is not disconnected when the nodes it
captured are freed, and throws `ObjectDisposedException` on the next emission. Subscribe a method, or
unsubscribe with `-=` where you subscribed.

## Names the engine looks up by string

String-based engine calls take the engine's **snake_case** name, not the C# one:
`CallDeferred("AddChild", n)` fails, `CallDeferred(Node.MethodName.AddChild, n)` works, and
`Callable.From(() => AddChild(n)).CallDeferred()` avoids the string entirely. The generated
`MethodName`, `PropertyName` and `SignalName` constants are also pre-built `StringName`s, so use them in
anything that runs per frame. Node paths are `NodePath`, a different type.

## Assembly reload

Reload happens **only in the editor**, when you rebuild while it is open — so it affects `[Tool]` scripts,
editor plugins, and the game running from the editor, never an exported or command-line run.

- `static` mutable state resets. Never keep game state there.
- Signal delegates are serialized and restored where the engine can: methods, and lambdas whose
  captures are engine types. Any it cannot serialize are dropped, and the message appears only with
  `--verbose`. A handler that stops running after a rebuild in the editor is this.
- Cached objects other than exported values are not restored.

## Marshalling cost

Typed engine method calls go through a direct pointer call; conversion to `Variant` happens on calls
into scripts, on signals, and on the dynamic `Call`/`Get`/`Set`/`Emit` path. Each crossing still costs
something: one call is negligible, a hundred thousand in a frame is the frame.

- **Do the arithmetic on the C# side.** `Vector3`, `Transform3D` and the other math types are C#
  structs, free until you hand one over.
- **Batch.** Read an engine property once, not in a loop. For a MultiMesh, build a `float[]` and hand it
  over with `Buffer` in one call instead of one `SetInstanceTransform` per instance.
- Avoid `Call("method")` and string-named signals in hot code.

## What does not belong on this side

A project that declares an engine-free layer means it. Nothing in that layer may reference `Godot`, hold
a `Node`, or use `Vector3` — not because those are bad, but because the moment the simulation depends on
the engine it can only be tested by starting one, and a suite that starts an engine is a suite nobody
runs on every change.
