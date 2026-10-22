# Allocation and collection in a game loop

The garbage collector is not slow; allocation is what makes it run. A loop that allocates nothing gives
it nothing to do.

## Where garbage comes from

| Source | Why it allocates | Instead |
|---|---|---|
| `new List<T>()` per frame | A fresh array every time | Reuse a field, and `Clear()` it |
| LINQ in a hot path | An enumerator, a closure, and usually an array | A `for` loop |
| A lambda that captures a local | A closure object per call | A static lambda, or pass state as an argument |
| String concatenation or interpolation | A new string each time | Build once when the text changes, not every frame |
| Boxing a struct | A heap object wrapping the value | A generic method constrained to the struct type, instead of an interface or `object` parameter |
| `params` arrays | An array per call | An overload with fixed arguments |
| `foreach` over an interface | `IEnumerator<T>` is a class | `foreach` over the concrete type, whose enumerator is a struct |
| `IEnumerable<T>` returns | Deferred execution allocates machinery | Fill a caller-supplied collection |

```csharp
// Bad: three allocations per frame, every frame.
public void Draw()
{
    var open = _grid.Cells.Where(c => c == CellState.Open).ToList();
    _label.Text = $"open {open.Count}";
}

// Good: no allocation while nothing changes.
private readonly List<int> _open = new();

public void Draw()
{
    _open.Clear();
    var cells = _grid.Cells;
    for (var i = 0; i < cells.Length; i++)
        if (cells[i] == CellState.Open) _open.Add(i);

    if (_open.Count != _shownCount)
    {
        _shownCount = _open.Count;
        _label.Text = "open " + _shownCount;
    }
}
```

## Span and pooling

`Span<T>` and `ReadOnlySpan<T>` give a view over memory without copying it, and `stackalloc` gives a
short buffer with no heap at all. They are the right tool for reading a grid, slicing a buffer, or
parsing — and they cannot be stored in a field on a class, which is the compiler enforcing that they do
not outlive the memory they point at.

`ArrayPool<T>.Shared` rents an array and gives it back. It is worth it for large, short-lived buffers,
and it is a liability for small ones: a rented array you forget to return is a leak, and one you return
twice is a corruption.

## Measure before you change anything

**An allocation you removed because it looked expensive is not a result.** Take a number first:

```sh
dotnet-counters monitor --process-id <pid> --counters System.Runtime
#   gen-0-gc-count        collections per interval
#   time-in-gc            per cent of time collecting
```

A frame hitch with a flat allocation rate is not a GC problem, and the time spent chasing it is the real
cost of guessing.

## Structs, and when they help

A `struct` in an array is stored inline, so a grid of a million cells is one allocation and one
cache-friendly walk. That is the single biggest structural win available to a simulation, and it is why
a cell is a byte-sized enum rather than an object.

The counter-rules: a struct larger than a few words is copied on every pass, a mutable struct is a source
of "I changed it and nothing happened", and a struct used through an interface is boxed — which returns
every saving to the heap.
