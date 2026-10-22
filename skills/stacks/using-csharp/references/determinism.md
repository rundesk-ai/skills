# Determinism in C#

A simulation is deterministic when the same starting state and the same inputs produce the same state,
every run, every machine. C# will not give you that by accident: several of its most convenient
constructs are explicitly documented as having no guaranteed order.

## Iteration order

**`Dictionary<TKey,TValue>` and `HashSet<T>` do not specify an enumeration order.** The documentation
says so outright, and the order in practice depends on each key's hash, on the bucket count, and on the
history of insertions *and removals* — so two dictionaries holding identical pairs can enumerate
differently, and the same dictionary can change order after an unrelated removal.

```csharp
// Bad: the order agents are stepped in decides who reaches the exit first.
foreach (var (id, resident) in _residents)
    resident.Step();

// Good: the order is chosen and stated.
for (var i = 0; i < _residents.Count; i++)   // a List<T>, in insertion order
    _residents[i].Step();

// Also good, where a map is genuinely wanted: sort a snapshot of the keys.
var ids = _residents.Keys.ToArray();
Array.Sort(ids);
foreach (var id in ids)
    _residents[id].Step();
```

**The trap is that it usually works.** A dictionary iterated in one process, on one build, with one
insertion history, is stable enough to pass every test you write today and to diverge the first time a
resident is removed.

`SortedDictionary<K,V>` and `SortedSet<T>` do specify order, at a cost per operation. A flat array
indexed by a dense integer id is usually better and always faster.

## Hash codes

**`string.GetHashCode()` is randomized per process.** .NET seeds string hashing differently on each run
so that hash-flooding attacks do not work, which means the value differs between two runs of the same
program. The same applies to the default `object.GetHashCode()`, which is derived from an object's
identity.

So a hash code may never be persisted, compared across runs, or used to order anything the simulation
reads. A state digest must be computed by an algorithm you wrote and can read — FNV-1a, xxHash, a CRC —
over bytes in an order you chose.

```csharp
// Bad: differs every run, and would be saved into the replay.
var digest = string.Join(",", cells).GetHashCode();

// Good: an algorithm with a specified result, over a specified order.
var hash = 14695981039346656037UL;              // FNV-1a offset basis
for (var i = 0; i < cells.Length; i++)
{
    hash ^= (byte)cells[i];
    hash *= 1099511628211UL;                    // FNV prime
}
```

**A digest only proves what it covers, in the order it walks.** A digest pinned over symmetric state
proves nothing about walk order: reversing the loop over a palindromic array produces the identical
sequence of bytes and the identical digest. Pin a digest over deliberately asymmetric state, or the test
is decorative.

## Floating point

Within one process and one build, `float` and `double` arithmetic is deterministic: IEEE 754 specifies
the result of each operation. What is not deterministic is **the order you perform them in**, because
floating-point addition is not associative — `(a + b) + c` and `a + (b + c)` can differ in the last bits,
and those bits compound over thousands of ticks.

Consequences:

- An accumulator fed different frame deltas reaches a different value, even for the same elapsed time.
  Accumulate elapsed time in integer microseconds and convert once, at the boundary.
- A sum over a collection depends on that collection's order, which returns you to the section above.
- Anything parallel reduces in completion order, which is not an order at all.
- `Math` functions beyond the four operations and `sqrt` are not specified bit-for-bit across platforms;
  avoid them in state that must match across machines.

Where bits must match, prefer integers or fixed-point. An integer is exact, cheap, and has no order
problem.

## Time and randomness

**No wall clock in simulation state.** `DateTime.Now`, `Environment.TickCount` and `Stopwatch` measure
the machine, not the game. The simulation's tick is its only timebase.

**RNG state lives in the simulation state and is saved with it.** A `Random` created on demand, or a
static shared one, cannot be replayed and cannot be saved. Seed it from the simulation's own seed, store
its state, and never call it from presentation code — a view that draws a random flicker by pulling from
the simulation's RNG changes the simulation.

## Proving it

- Two instances, same construction, same number of steps, same digest.
- A digest whose value is pinned in a test, over asymmetric state, so that a change to state layout or
  walk order fails rather than passing silently.
- **Then break it on purpose.** Reverse the walk, swap a `List` for a `Dictionary`, and confirm the test
  goes red. A determinism test that has never been seen to fail is a test of nothing.
