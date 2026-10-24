# GDScript at simulation scale

Read this before writing a grid, an agent list, a tick loop, or a chunked world. Measured on Godot 4.7.2,
headless, one Apple Silicon machine: debug is the editor binary, release the export template. Debug
times run 1.2–1.7 times release; the ratios between rows hold in both, and they are what to trust.

## The numbers that decide the design

| 65,536 elements (a 256×256 grid) | Release ms |
|---|---:|
| grid read+write: `PackedInt32Array` / `PackedByteArray` | 0.99 / 0.95 |
| grid read+write: `Array[int]` / untyped `Array` | 1.70 / 2.19 |
| grid read+write: `Dictionary[Vector2i, int]` | 8.33 |
| 4-neighbour sum: flat `PackedInt32Array` / `Dictionary[Vector2i, int]` | 2.20 / 15.72 |
| update two fields: parallel `PackedFloat32Array`s / `RefCounted` per agent / `Dictionary` per agent | 1.19 / 4.57 / 5.83 |
| `s += i + 1` inline / through a method call / through `Callable.call` | 0.53 / 2.63 / 3.15 |
| one signal emit per agent / one signal carrying all the ids | 6.08 / 0.73 |
| `Array[int].sort()` / `.sort_custom(lambda)` / `PackedInt32Array.sort()` | 7.62 / 38.2 / 2.81 |
| `Array[Agent].sort_custom` by a field / the same order from a packed-key sort | 141 / 4.8 (debug) |
| `String +=` 16,384 parts / `PackedStringArray` + `join` | 34.1 / 0.64 |

| Memory per instance (debug) | Bytes |
|---|---:|
| one cell in `PackedByteArray` / `PackedInt32Array` / `Array[int]` / `Dictionary` | 1 / 4 / 24 / 82 |
| three floats per agent in shared `PackedFloat32Array`s | 12 |
| a `Dictionary` `{x, y, hunger}` | 596 |
| a script `RefCounted` with three members | 1,020 |
| `Node2D.new()`, not in the tree | 1,901 |

## Grids and agents

- **A grid is one flat packed array indexed `y * width + x`**, never a Dictionary keyed by cell. Choose
  the narrowest type: `PackedByteArray` for under 256 kinds, `PackedInt32Array` above.
- **Thousands of agents are columns**: one packed array per field, one index per agent, a free list of
  indices (`PackedInt32Array`) instead of erasing, which shifts every later index. Keep objects for the
  hundreds that need identity and behaviour.
- **A Dictionary is for sparse data** — under about 5–10% of cells occupied, such as ore or items on belts.
- Packed arrays hold 32-bit ints, bytes or 32-bit floats while GDScript `int` and `float` are 64-bit:
  a `PackedInt32Array` counter wraps at 2,147,483,647 and a byte grid turns 256 into 0, silently. Money,
  population and timestamps go in `PackedInt64Array` or `PackedFloat64Array`.

## Hot loops

- **Inline the per-element work in the loop the profiler names.** Every GDScript call costs 40–60 ns,
  and a lambda, a `Callable` or a call by name costs the same.
- `for i in n` or `for i: int in range(n)` (which allocates nothing) beats `while`, about twofold.
- `filter`, `map` and `reduce` with lambdas are twice the loop they replace; keep them off the hot path.
- Iterate `dict.values()` rather than `for k in dict: dict[k]`, which hashes every key again.
- Build long strings with `PackedStringArray` and `"".join()`; `+=` is quadratic.
- `get_tree().get_nodes_in_group()` builds a new array on every call; keep your own index of what a
  tick visits.
- **Batch signals per tick**: collect ids into a `PackedInt32Array` and emit once.
- **`sort_custom` calls GDScript for every comparison.** Sort numbers natively, and to order objects
  pack a non-negative key and the index into one int:

```gdscript
var keys := PackedInt64Array()
keys.resize(n)
for i: int in n:
	keys[i] = (int(priority[i] * 1000000.0) << 17) | i   # key >= 0, i < 131072
keys.sort()
for k: int in n:
	var agent: int = keys[k] & 0x1FFFF
```

  The index in the low bits also breaks ties, and `sort` and `sort_custom` are not stable.
- `StringName` literals speed equality only slightly, and a `Dictionary[StringName, int]` lookup was
  slower than a `String` one. Use them for engine-facing names (actions, animations, groups), where the
  engine would otherwise convert, not for your own tables.

## Threads

```gdscript
var task := WorkerThreadPool.add_group_task(_step_chunk, chunks.size(), -1, true)   # high_priority
WorkerThreadPool.wait_for_group_task_completion(task)
```

- **Pass `high_priority = true`.** The default low priority is capped by
  `threading/worker_pool/low_priority_thread_ratio` (0.3): 1,024 chunk steps reached 3.95 times serial
  on 16 cores at low priority and 12.9 times at high.
- **Give each task a chunk, not a cell** — at least about 0.1 ms of work. 65,536 one-cell tasks were
  slower than serial.
- Workers may write distinct indices of a preallocated array; anything that resizes a container, and
  any shared counter, needs a `Mutex` (an unlocked counter lost 627 of 262,144 increments). Never
  `append` from a worker; merge results on the main thread.
- A chunk step that reads its neighbours reads last tick's copy and writes this tick's, or the result
  depends on scheduling. Each chunk task owns its own `RandomNumberGenerator`, seeded from the world seed
  and the chunk coordinate.
- **Touching the live scene tree from a worker is caught only sometimes**: `add_child` errors, but
  setting `position` passed silently. Workers compute plain data; the main thread applies it.
- Wait for every task and `Thread` (`wait_to_finish`); an unwaited `Thread` logs a warning when freed.

## Large and infinite worlds

The chunk design itself is engine-neutral; this is what it costs in GDScript. A thousand loaded 64×64
chunks is 16 MB as `PackedInt32Array`s and 4 GB as an object per cell.

- **Look chunks up in a `Dictionary[Vector2i, Chunk]`** (about 94 ns), once per chunk or row, then index
  the chunk's packed array. World to chunk for a 64-cell chunk is `wx >> 6` and `wx & 63`, correct for
  negative coordinates; `wx / 64` and `wx % 64` are not.
- **Time-slice the active chunks against a budget** with a cursor that resumes next frame; reading
  `Time.get_ticks_usec()` costs about 19 ns, cheap per chunk. A budget makes progress per frame depend
  on the machine, so advance the simulation in whole ticks and spread one tick's chunks over frames —
  never step a chunk twice before the others.

```gdscript
var _cursor := 0

func _physics_process(_delta: float) -> void:
	var deadline := Time.get_ticks_usec() + 2000
	while _cursor < _active.size() and Time.get_ticks_usec() < deadline:
		_step_chunk(_active[_cursor])
		_cursor += 1
	if _cursor >= _active.size():
		_cursor = 0                 # one whole tick done
```

- **Save a chunk as `to_byte_array()` compressed with ZSTD**: 16,384 bytes became 672 in 9 µs, and
  decompression took 5 µs. `decompress()` needs the exact original size — one byte short returned an
  empty array — and `decompress_dynamic` does not support ZSTD, so store `[raw_size, bytes]`.
- **An unloaded chunk is freed only when nothing references it**: a cache array, a bound callable or a
  lambda capture keeps it alive. Watch `Performance.get_monitor(Performance.OBJECT_COUNT)` across
  load and unload cycles.
- **A Dictionary keeps its memory after `erase` and after `clear()`**: a million-entry index still held
  18 MB of its 79 MB. Replace it (`d = {}`) after a mass unload.

## When to leave GDScript

C# was 4–25 times faster on pure loops over plain arrays in the same engine, and only 1.7 times faster
on engine property sets; reading `Godot.Collections.Array` element by element from C# was slower than
GDScript. Move a hot loop out when it is computation over plain data and the profiler names it, not
when it is mostly engine calls.

## Data definitions

Building types, recipes and similar tables are custom `Resource`s with typed exports. Text `.tres`
loaded 2,000 definitions in 66 ms against 10 ms for binary `.res`; exports convert text resources to
binary by default, so load with `load()`, never `FileAccess`, because the extension changes on export.
A loaded definition is shared: treat it as read-only and keep per-instance state in the simulation's
arrays. `const` arrays and dictionaries are read-only at runtime, which suits static tables.
