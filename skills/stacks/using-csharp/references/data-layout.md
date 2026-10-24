# Data layout at simulation scale

Measured on .NET 10 (Arm64, Release, Stopwatch best of 7 after warm-up). The ratios are what to trust;
take your own number before acting on one.

## Agents: structs, objects, and columns

| 100,000 agents | Time per 100 ticks | Memory |
|---|---|---|
| `class[]`, allocated in order | 8.0 ms | 8.8 MB |
| `class[]`, references shuffled (a heap after churn) | 12.5 ms | 8.8 MB |
| `struct[]`, updated with `ref var` | 7.7 ms | 2.0 MB |
| one `int` of a 64-byte struct: array of structs vs a separate `int[]` | 6.6 ms vs 3.4 ms | — |

- A `struct[]` is a quarter of the memory and immune to heap order. Update it in place with
  `ref var a = ref agents[i];` — `var a = agents[i]` copies.
- Split a field into its own array (struct of arrays) when systems touch it alone — hunger, position.
  Two passes over two arrays measured slower than one pass over structs, so split by access, not by habit.
- A dense integer id indexes an array. A `Dictionary<int, Agent>` for ids `0..n` pays a hash for nothing
  and brings back the enumeration-order problem.

## Grids and keys

| 1M lookups, 90,000 cells | Time |
|---|---|
| flat `int[]`, `y * width + x` | 1.0 ms |
| `Dictionary<RKey, int>`, `readonly record struct RKey(int X, int Y)` | 2.5 ms |
| `Dictionary<(int, int), int>` | 5.6 ms |
| `Dictionary<long, int>`, key `((long)x << 32) \| (uint)y` | **516 ms** |

The packed `long` collides because `long.GetHashCode()` folds the halves together with XOR: 90,000 keys
landed on 512 hash codes. An unbounded map uses a record struct key or a comparer that mixes bits.

## Sets of dense ids

`bool[]` or a `ulong[]` bitset beats `HashSet<int>` about threefold for membership, and
`BitOperations.PopCount` over `ulong[]` counts ten times faster than a `bool[]` loop at an eighth of the
memory.

## Lookups and updates

- **One hash lookup, not two.** Counting into a dictionary: `ContainsKey` then get then set 9.4 ms,
  `TryGetValue` then set 4.2 ms, `CollectionsMarshal.GetValueRefOrAddDefault(d, key, out _)++` 1.9 ms.
  The returned `ref` is invalid after any other add or remove on that dictionary.
- Presize what you know the size of: a million `Dictionary` adds allocated 54 MB without capacity, 23 MB
  with it.

## Removal

A swap with the last element and `RemoveAt(Count - 1)` removes in constant time, and it changes order:
in an agent list whose order is part of the rules, that is a determinism decision, not an optimization.
`RemoveAt(0)` drains a list 570 times slower than a `Queue<T>`.

## Iterating a list

`CollectionsMarshal.AsSpan(list)` is the fastest walk over a `List<T>` and allows `ref` access to its
elements. The span still points at the old array after an `Add` that grows the list, and a write
through it is lost without an error: never add or remove while it is live.

## Large and infinite worlds

A world too big to hold is a sparse map of fixed-size chunks, loaded near the player and dropped far
away. What C# decides is what each load and unload costs the collector:

| 20,000 chunk loads, 200 kept live | Bytes per chunk | Gen 0 | Gen 2 |
|---|---|---|---|
| 64×64 `ushort[]`, `new` each time | 8,192 | 19 | 0 |
| 256×256 `ushort[]`, `new` each time | 131,072 | 90 | **90** |
| 256×256 `ushort[]`, from `ArrayPool<ushort>.Shared` | 131,072 | 2 | 2 |

- **An array of 85,000 bytes or more goes on the large object heap**, which is collected only with
  generation 2 — a full collection, the pause a player sees. Keep a chunk's arrays under the threshold,
  or rent them from a pool and return them on unload.
- Key chunks by a `readonly record struct ChunkKey(int X, int Y)`, computed with floor division, and
  keep the cell data in flat arrays inside the chunk rather than an object per cell.
- Generate or load a chunk off the main thread as plain arrays, then hand the finished chunk to the
  main thread in one step; never let two threads touch one chunk's arrays.
- A `float` position loses millimetres tens of kilometres from the origin. Keep simulation positions as
  an integer chunk plus a local offset, or `double`, and convert at the view.
- Watch the result over a long session, not a short one: `GC.CollectionCount(2)` and
  `GC.GetGCMemoryInfo()` before and after an hour of streaming say whether unloaded chunks really left.
