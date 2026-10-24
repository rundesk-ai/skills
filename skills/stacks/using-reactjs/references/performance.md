# React performance

Read this when an interaction is measurably slow. Do not read it to add memoization
pre-emptively.

## Measure before changing anything

Name the slow interaction and the number you are moving (commit duration, interaction latency, one
component's render time), and record a baseline with the React Profiler or the browser's performance
timeline on a production build: development builds carry extra work, and Strict Mode's double rendering
makes every component look twice as expensive. Moving state down to the component that uses it is the
highest-value fix and costs nothing at run time; a list of thousands of rows needs virtualization, not
memoization.

## What memoization costs

Measured, to keep proposals in proportion (2,000 children, one parent update, production build in jsdom,
median of 40 updates; React work and DOM calls, not browser paint):

| Case | Time per update |
|---|---|
| plain children re-render | 0.36 ms |
| `memo` children with stable props, all skipped | 0.18 ms |
| `memo` defeated by an inline `style={{…}}`, compiler off | 0.59 ms: slower than no `memo` |
| rows with inputs, stable keys | 4.4 ms |
| the same rows with `key={Math.random()}`, remounting every row | 28.5 ms, and every input loses its state |

A re-render of a cheap component is about a tenth of a microsecond here; the cost that hurts is an
expensive component re-rendering, or a whole subtree remounting. With the compiler off, `memo` works only
when every prop is stable, so memoizing a child usually means memoizing what the parent passes too; with
it on, the compiler caches those literals itself, so do not hoist objects to "fix" compiled code.

## The React Compiler

Where the React Compiler is enabled it memoizes components and hooks automatically, but only the ones
that follow the Rules of React, and it skips the rest silently:

- A component that reads a ref during render, mutates a prop, sets state during render, writes a module
  variable, or carries an `eslint-disable` for a React rule is left uncompiled, and the build still
  passes. Compile with the plugin's `logger`
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

Re-measure the same interaction the same way and report both numbers, and check that no memoized value
with a stale dependency now renders old data.
