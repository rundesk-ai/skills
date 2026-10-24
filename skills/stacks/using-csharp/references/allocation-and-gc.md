# Allocation and collection in a game loop

The garbage collector is not slow; allocation is what makes it run. A loop that allocates nothing gives
it nothing to do.

## Where garbage comes from

| Source | Why it allocates | Instead |
|---|---|---|
| LINQ in a hot path | An enumerator, a closure, and usually an array; four to five times a loop | A `for` loop; LINQ in load, save and UI refresh |
| A lambda that captures a local, or only `this` | A closure or delegate per call (64 bytes for `this` alone) | A `static` lambda with state passed as an argument, or a delegate cached in a field |
| Text rebuilt every frame | A new string each time | Rebuild when the value changes; format into a reused `StringBuilder` or `TryFormat` into a span |
| `Enum.ToString()`, `Enum.GetValues<T>()` | A string or array every call | A cached `string[]` indexed by value; a static field |
| A struct passed as an interface or `object` | A 24-byte box per call | A generic method constrained to the interface |
| `params T[]` | An array per call | `params ReadOnlySpan<T>` (C# 13), which allocates nothing |
| `foreach` over an interface, `IEnumerable<T>` returns | A class enumerator; deferred machinery | The concrete type, whose enumerator is a struct; fill a caller-supplied collection |

## Pools and stack buffers

`ArrayPool<T>.Shared` rents an array and gives it back. It is worth it for large, short-lived buffers,
and it is a liability for small ones: a rented array you forget to return is a leak, and one you return
twice is a corruption. `Rent(100)` returns at least 100 elements — 128 here — still holding the
previous renter's data, so slice to the length you asked for and clear what you read before writing.

`stackalloc` only a small, fixed bound, and never inside a loop: each iteration grows the frame until
the stack overflows, which cannot be caught. `Span<int> buf = n <= 256 ? stackalloc int[256] : rented;`
is the pattern.

## Prove a tick allocates nothing

`GC.GetAllocatedBytesForCurrentThread()` is exact to the object — one `new object()` reads 24 bytes —
so a test can hold the line once the hot path is clean:

```csharp
[Fact]
public void TickDoesNotAllocate()
{
    var sim = Sim.Build(seed: 1, businesses: 10_000);
    sim.Tick(); sim.Tick();                                // warm up: JIT, static constructors, lazy caches
    var before = GC.GetAllocatedBytesForCurrentThread();
    for (var i = 0; i < 100; i++) sim.Tick();
    Assert.Equal(0, GC.GetAllocatedBytesForCurrentThread() - before);
}
```

It counts the current thread only; work on other threads needs `GC.GetTotalAllocatedBytes(precise: true)`.
Measure a Release build outside the debugger: Debug and tier-0 JIT code allocate and run differently.

## Measure before you change anything

**An allocation you removed because it looked expensive is not a result.** Take a number first:

```sh
dotnet-counters monitor --process-id <pid> --counters System.Runtime
#   gen-0-gc-count        collections per interval
#   time-in-gc            per cent of time collecting
```

A frame hitch with a flat allocation rate is not a GC problem, and the time spent chasing it is the real
cost of guessing.

## Collector settings

The default — workstation, concurrent — is right for a game client; server GC trades pause shape for
throughput. `GCLatencyMode.SustainedLowLatency` during play avoids blocking full collections at the cost
of a larger heap; `GC.TryStartNoGCRegion` covers a load screen, not a session. Large chunk arrays and the
large object heap are in [Data layout](data-layout.md). All of this, and the allocation counter above,
is CoreCLR: a host on Mono or an ahead-of-time runtime has its own collector and ignores these settings.

## Hidden struct copies

A large struct is copied when passed by value to a call that is not inlined, or through a hidden
defensive copy — a non-`readonly` member called through an `in` parameter or a `readonly` field. Mark the
struct or the member `readonly`. A plain read-only `foreach` over a struct array measured no slower than
`ref readonly`: the JIT removes that copy, so do not rewrite loops for it.
