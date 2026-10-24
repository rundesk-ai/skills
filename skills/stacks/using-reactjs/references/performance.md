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
defeats it, and a defeated `memo` is slightly slower than none, since it compares and then renders
anyway. Memoizing a child usually means memoizing what the parent passes too; that chain is the
maintenance cost people underestimate.

Measured costs, to keep proposals in proportion (2,000 children, one parent update, production build in
jsdom, median of 40 updates; React work and DOM calls, not browser paint):

| Case | Time per update |
|---|---|
| plain children re-render | 0.36 ms |
| `memo` children with stable props, all skipped | 0.18 ms |
| `memo` defeated by an inline `style={{…}}` | 0.59 ms |
| rows with inputs, stable keys | 4.4 ms |
| the same rows with `key={Math.random()}`, remounting every row | 28.5 ms, and every input loses its state |

A re-render of a cheap component is about a tenth of a microsecond here; the cost that hurts is an
expensive component re-rendering, or a whole subtree remounting.

## The React Compiler

Where the React Compiler is enabled it memoizes components and hooks automatically, but only the ones
that follow the Rules of React, and it skips the rest silently:

- A component that reads a ref during render, mutates a prop, sets state during render, or writes a
  module variable is left uncompiled, and the build still passes. Compile with the plugin's `logger`
  option, or once with `panicThreshold: 'all_errors'`, to list every skipped component with its reason.
- A library hook that returns the same object every render and mutates it in place (some table and form
  libraries) renders stale UI once the compiler memoizes on that object's identity. The lint rule
  `incompatible-library` warns about known cases; put `'use no memo'` in the affected component, and test
  the interaction with the compiler on.
- Configuration moves between tool versions, so check the build rather than the config: a compiled
  component's output contains `react.memo_cache_sentinel` comparisons and imports `react/compiler-runtime`.
- Leave existing `useMemo` and `useCallback` in place when turning the compiler on; removing them can
  change compilation output and the stability of effect dependencies. In new code, keep them as an
  escape hatch, for example for a value used as an effect dependency.

## Prove the improvement

Re-measure the same interaction the same way and report both numbers. Confirm the behavior did not
change: a memoized component with a stale dependency renders old data, which is a correctness
regression bought with a performance win. Keep the profile or timing output as the evidence.
