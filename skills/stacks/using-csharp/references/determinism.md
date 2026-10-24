# Determinism in C#

Same starting state, same inputs, same state: every run, every machine. Each convenience below is
documented as unspecified, and each one passes the tests you write today.

## Iteration order

**`Dictionary<TKey,TValue>` and `HashSet<T>` do not specify an enumeration order**, and in practice it
depends on hashes, bucket count and the history of insertions **and removals**: two dictionaries holding
the same pairs can enumerate differently, and one can change order after an unrelated removal. It is
stable enough to pass every test until the first resident is removed.

Step simulation objects from a `List<T>` or an array, in an order you chose. Where a map is genuinely
wanted, keep a sorted list of its ids alongside it, updated on add and remove — sorting a snapshot of the
keys every tick works, and allocates every tick. `SortedDictionary` specifies order at a cost per
operation; a flat array indexed by a dense id is cheaper than both.

## Sorting and queues

**`Array.Sort`, `List<T>.Sort` and `MemoryExtensions.Sort` are unstable.** Up to 16 items they use an
insertion sort, which keeps equal keys in order, so every small test passes; past 16 the order of equal
keys depends on the order they arrived in. Fifty items keyed `i % 3` came back `0, 45, 42, 39…` for key 0.
Feed the same sort a list built in a different order — after a load, after a removal — and "who acts
first" changes.

```csharp
// Bad: equal priorities come out in an order nobody chose.
jobs.Sort((a, b) => b.Priority.CompareTo(a.Priority));

// Good: a total order, ending in a unique key.
jobs.Sort(static (a, b) => a.Priority != b.Priority ? b.Priority.CompareTo(a.Priority) : a.Id.CompareTo(b.Id));
```

`Enumerable.OrderBy` is stable; it allocates, so it belongs outside the tick.

**`PriorityQueue<TElement,TPriority>` does not keep equal priorities first-in, first-out** — ten jobs at
one priority came out `0, 9, 8, …, 1`. Make the priority `(int priority, long sequence)` with the
sequence counter saved in the simulation state.

A comparer must also be a total order; see [Numbers](numbers.md) for NaN and subtraction.

## Hash codes and digests

`string.GetHashCode()`, `HashCode.Combine` and `ValueTuple.GetHashCode()` are randomized per process —
`HashCode.Combine(1, 2)` differed between two launches — and so is anything that hashes through them: a
record or anonymous type holding a string, and a record class (its hash includes its type's identity
hash). Integer and double hash codes happen to be stable, and nothing promises it.

So a hash code is never persisted, compared across runs, or used to order what the simulation reads. A
state digest is an algorithm you wrote — FNV-1a, xxHash, a CRC — over **every byte** of the state, in an
order you chose:

```csharp
static ulong Mix(ulong hash, ulong value)
{
    for (var b = 0; b < 8; b++)                // FNV-1a over all eight bytes, not the low one
    {
        hash ^= (byte)(value >> (8 * b));
        hash *= 1099511628211UL;
    }
    return hash;
}

var hash = 14695981039346656037UL;
foreach (var c in cells) hash = Mix(hash, (ulong)c.Kind);
foreach (var a in agents) hash = Mix(Mix(hash, (ulong)a.Id), (ulong)BitConverter.DoubleToInt64Bits(a.Hunger));
```

Hash a float by its bits, never its `ToString()`, which rounds.

**A digest only proves what it covers, in the order it walks.** Reversing the loop over a palindromic
array produces the identical bytes and the identical digest. Pin a digest over deliberately asymmetric
state, or the test is decorative.

## Floating point

One operation is exactly specified; **the order of operations is not**, because addition is not
associative, and the low bits compound over thousands of ticks.

- An accumulator fed different frame deltas reaches a different value for the same elapsed time.
  Accumulate elapsed time in integer microseconds and convert once, at the boundary.
- `Math` functions beyond the four operations and `sqrt` are not specified bit for bit across platforms,
  `MathF` and `Math` results differ between runtimes, and an ahead-of-time compiler may contract `a * b + c`
  into one fused operation. Keep them out of state that must match across machines.
- `Vector<T>` has a width chosen by the CPU — four floats on one machine, eight on another — so a SIMD
  float reduction groups additions differently per machine. A million floats gave three different sums
  from a scalar loop, `Vector<float>` and LINQ `Sum`. Use SIMD on integer state, or fixed-width
  `Vector128<T>` with a fixed reduction order.

Where bits must match, use integers or fixed point.

## Randomness

`System.Random` cannot be saved — its state is private — and its documentation warns that a seeded
sequence may differ between .NET versions, so a seed in a save file is a promise the runtime does not
make. Own a small generator whose state is plain fields:

```csharp
public sealed class SplitMix64        // a class: a struct copy would fork the sequence silently
{
    public ulong State;
    public SplitMix64(ulong seed) => State = seed;
    public ulong Next()
    {
        var z = State += 0x9E3779B97F4A7C15UL;
        z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9UL;
        z = (z ^ (z >> 27)) * 0x94D049BB133111EBUL;
        return z ^ (z >> 31);
    }
}
```

Save `State` with the simulation, and never draw from it in presentation code: a view that pulls a random
flicker from the simulation's generator changes the simulation.

## Parallel work that still replays

`Parallel.For` with thread-local sums gave 16 different totals in 20 runs over the same doubles. Split the
work into a **constant** number of chunks — not `Environment.ProcessorCount` — write each chunk's result
to its own slot, and combine the slots in index order: one total across 20 runs.

```csharp
var part = new double[Chunks];
Parallel.For(0, Chunks, c =>
{
    double s = 0;
    for (int i = c * size; i < Math.Min(n, (c + 1) * size); i++) s += v[i];
    part[c] = s;
});
double total = 0;
for (int c = 0; c < Chunks; c++) total += part[c];
```

Each chunk reads only state no other chunk writes during the step.

## Proving it

- Two instances, same construction, same steps, same digest; and a run that saves mid-game, loads, and
  keeps stepping both copies (see [Saves and serialization](saves-and-serialization.md)).
- A digest value pinned in a test, so a change to state layout or walk order fails.
- **Break it on purpose** — reverse the walk, swap a `List` for a `Dictionary` — and watch the test go red.
  A determinism test that has never been seen to fail is a test of nothing.
