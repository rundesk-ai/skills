# Numbers

Every entry here fails silently: no exception, a plausible wrong value. Each was reproduced on .NET 10.

## Rounding

`Math.Round` rounds a midpoint to the even neighbour unless told otherwise: `Math.Round(2.5)` is `2`,
`Math.Round(3.5)` is `4`, and `Convert.ToInt32(2.5)` is `2`. A cast truncates toward zero:
`(int)-2.7` is `-2`.

```csharp
// Bad: a tax of 2.5 becomes 2, and totals drift low.
long tax = (long)Math.Round(revenue * rate);

// Better: the rule is written down.
long tax = (long)Math.Round(revenue * rate, MidpointRounding.AwayFromZero);

// Best: no floating step. Rate in basis points, half up, for non-negative revenue held as long.
long tax = (revenue * rateBasisPoints + 5_000) / 10_000;
```

`0.1` has no exact `double`, so `revenue * 0.1` can land a hair either side of a midpoint. When a
result must be exact, keep the rate as an integer and round once, at the end, with a named rule.

## Overflow

Integer arithmetic is unchecked by default: `int.MaxValue + 1` is `-2147483648`. A tycoon balance, a
population total or a tick counter wraps and keeps going.

- **Money is `long` minor units** (cents), or `decimal` where the design needs base-10 fractions;
  `decimal` always throws on overflow.
- **Multiply before dividing, and hand out the remainder.** `amount / 100 * percent` loses the fraction
  before it multiplies; `amount * percent / 100` does not. Splitting 100 cents three ways as `100 / 3`
  each loses a cent: give the remainder to the first shares, in a fixed order.
- **`checked(a + b)` where a total can grow without bound**, or `<CheckForOverflowUnderflow>true</...>` in
  Debug and test builds so the suite finds the wrap.
- **LINQ `Sum()` over `int` or `long` is checked, a hand loop is not.** Replacing one with the other
  changes behaviour: one throws, the other wraps. Sum into a `long` deliberately.
- `Math.Abs(int.MinValue)` throws, and negating `int.MinValue` at runtime gives `int.MinValue`.

## Negative coordinates

`/` and `%` truncate toward zero: `-1 / 16` is `0` and `-1 % 10` is `-1`, so a unit one step west of the
origin lands in chunk 0 and the wrong cell.

```csharp
static int FloorDiv(int a, int b) => a / b - ((a % b != 0) && ((a ^ b) < 0) ? 1 : 0);
static int Mod(int a, int n) => ((a % n) + n) % n;
// For a power-of-two size: chunk = x >> 4; local = x & 15;   (-1 >> 4 is -1)
```

## NaN and infinity

Integer division by zero throws; floating division does not: `1.0 / 0` is infinity, `0.0 / 0` is NaN,
and every value computed from them is poisoned. `NaN == NaN` is false, `NaN.Equals(NaN)` is true.

- Assert `double.IsFinite(x)` at the tick boundary, or in a state validator a test runs every tick.
- System.Text.Json refuses NaN by default, so the save is where a NaN produced hours earlier surfaces.

## Comparers

A comparer must be a total order, or sorting is silently wrong:

- `(a, b) => a - b` overflows for large or negative values and returns the wrong sign.
- `a < b ? -1 : a > b ? 1 : 0` treats NaN as equal to everything; 20 NaNs in 1,000 values left 15
  inversions among the rest, with no exception.
- Use `a.CompareTo(b)`, which orders NaN first consistently, and end with a unique tie-break so the
  order is also deterministic (see [Determinism](determinism.md)).

## Float to int

Since .NET 9 an out-of-range or NaN float-to-int conversion saturates on every platform
(`(int)3e10` is `int.MaxValue`, `(int)double.NaN` is `0`); before .NET 9 it differed between x64 and
Arm64. Clamp and reject NaN before converting simulation values, or use `checked((int)x)` to throw.
