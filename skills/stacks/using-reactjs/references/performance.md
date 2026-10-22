# React performance

Read this when an interaction is measurably slow. Do not read it to add memoization
pre-emptively.

## Measure before changing anything

Name the slow interaction, reproduce it, and record a baseline with the React Profiler or the
browser's performance timeline. Profile a production-mode build for realistic numbers: development
builds carry extra work, and Strict Mode's double rendering makes every component look twice as
expensive as it is.

State which number you are moving — commit duration, interaction latency, a specific component's
render time — before you change code. "Feels faster" is not evidence, and neither is a smaller
render count that no one can perceive.

## Fix the structural cause before memoizing

Most React slowness is one of these, and memoization addresses none of them:

| Cause | Fix |
|---|---|
| Rendering thousands of rows | Virtualize or paginate |
| State held too high, so a keystroke re-renders a page | Move state down to the component that uses it |
| A provider value recreated every render | Memoize the value, or split the context |
| Expensive derivation repeated per item | Compute once above the list |
| A large synchronous update blocking input | `useTransition` or `useDeferredValue` |
| Oversized bundle delaying first interaction | Code-split at route or feature boundaries |

Moving state down is the highest-value fix and costs nothing at runtime.

## Understand what memoization actually buys

`useMemo` caches a computed value, `useCallback` caches a function identity, and `React.memo` skips a
re-render when props are shallow-equal. Each has a real cost: the comparison itself, the retained
memory, and the maintenance burden of a dependency array that can go stale.

```jsx
// Pointless: the comparison costs more than the addition.
const total = useMemo(() => a + b, [a, b]);

// Pointless: memo cannot help while a new object arrives every render.
const Row = React.memo(RowImpl);
<Row style={{ padding: 8 }} item={item} />
```

`React.memo` only works when every prop is stable. One inline object, array, or arrow function
defeats it entirely, which is why memoizing a child usually means memoizing what the parent passes
too. That chain is the maintenance cost people underestimate.

Where the React Compiler is enabled, it applies this class of memoization automatically from the
Rules of React; hand-written `useMemo` and `useCallback` become redundant, and impure components
are precisely what stop it from working. Check whether the project has it enabled before adding
memoization by hand.

## Prove the improvement

Re-measure the same interaction the same way and report both numbers. Confirm the behavior did not
change: a memoized component with a stale dependency renders old data, which is a correctness
regression bought with a performance win. Keep the profile or timing output as the evidence.
