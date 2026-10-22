---
name: using-reactjs
description: Use when building, reviewing, debugging, or refactoring React components and hooks, including rendering purity, state ownership, effects and their alternatives, refs, context, external stores, transitions and Suspense, server and client component boundaries, rendering performance, and React-focused tests. It supplies the documented React rules, the failures each one prevents, and the evidence that proves a fix. Do not use for React Native platform work, for Vue or another framework, or for a repository that merely lists React as a transitive dependency the task never touches.
---

# Use React

Make render purity, state ownership, and effect necessity explicit before changing a component.

Most React defects are not syntax errors. They are a value derived in state instead of during
render, an effect standing in for an event handler, or a store read that React cannot see. Find the
category first.

## Check the installed version

Read `package.json` and the lockfile before applying version-gated guidance:

```sh
npm ls react react-dom
```

This skill targets React 19.x on the stable channel. Never make a development-only warning, an
`unstable_` API, a canary or experimental build, or an undocumented internal a production default;
they sit outside React's semver guarantee. If the project is on React 18 or earlier, say so and
scope the advice, and read [versions-and-migration.md](references/versions-and-migration.md) before
an upgrade.

## Work in this order

1. Record the React and `react-dom` versions, and whether the app uses Server Components.
2. Reproduce the symptom and classify it: impure render, misplaced state, unnecessary effect, an
   untracked external value, a concurrency-visible tear, or measured slowness.
3. Fix ownership and purity before reorganizing files or adding memoization.
4. Prefer removing an effect over correcting its dependency array.
5. Prove the fix through rendered output and user-visible behavior, not through internal state.

## Keep components and hooks pure

React may call a component more than once for the same input, and it can discard or replay a
render. The documented rules are that components and hooks are idempotent, that side effects stay
out of render, and that props, state, hook arguments, and values already used in JSX are treated as
immutable.

```jsx
// Bad: render mutates a prop and writes to an external system.
function Row({ item }) {
  item.seen = true;
  analytics.track('row-render');
  return <li>{item.label}</li>;
}

// Good: render only derives; the effect on the outside world belongs to an event.
function Row({ item, onSeen }) {
  return <li onClick={() => onSeen(item.id)}>{item.label}</li>;
}
```

The bad version breaks because a double render double-counts the analytics event and silently
edits data another component may still render from. Enable Strict Mode and
`eslint-plugin-react-hooks`; they exist to surface exactly this class of bug in development.

Call Hooks only at the top level of a component or another Hook, never inside a condition, loop,
nested function, or after an early return. Never call a component as a plain function, and never
pass a Hook around as a value.

## Own state at one level, and derive the rest

State is for values that cannot be computed. Everything else is derived during render.

```jsx
// Bad: a second source of truth that can disagree with the first.
const [fullName, setFullName] = useState('');
useEffect(() => { setFullName(first + ' ' + last); }, [first, last]);

// Good: one source of truth.
const fullName = first + ' ' + last;
```

To reset state when the identity of the thing changes, change the `key` rather than clearing state
from an effect — the effect version renders once with stale values before it corrects itself.

## Question every effect

An effect is for synchronizing with a system outside React. If no external system is involved, the
work belongs in render or in an event handler. [effects.md](references/effects.md) holds the table
of unnecessary effects and their replacements; read it before writing or keeping a `useEffect`.
Rendered data belongs in state, never in a `useRef`.

## Read only the needed reference

- Purity, derived values, state placement, and list identity:
  [rendering-and-state.md](references/rendering-and-state.md)
- An effect that fires too often, never cleans up, or should not exist:
  [effects.md](references/effects.md)
- Refs, context shape, and reading a store React does not own:
  [refs-context-and-stores.md](references/refs-context-and-stores.md)
- Transitions, deferred values, Suspense boundaries, and tearing:
  [concurrency-and-suspense.md](references/concurrency-and-suspense.md)
- Server Components, `'use client'`, and props that cross the boundary:
  [server-and-client.md](references/server-and-client.md)
- Profile-led rendering work and what memoization actually costs:
  [performance.md](references/performance.md)
- Behavior-first component tests, `act`, and async assertions:
  [testing.md](references/testing.md)
- React 19 removals, deprecations, and upgrade evidence:
  [versions-and-migration.md](references/versions-and-migration.md)
- Claim-to-source audit map: [sources.md](references/sources.md)

## Report findings as evidence

```text
[HIGH] Derived value stored in state
Location: src/checkout/Summary.jsx:18
Evidence: useEffect(() => setTotal(items.reduce(sum, 0)), [items])
Why: total is computable from items, so the effect adds a render pass and a second source of truth
     that can disagree with items after an interrupted update.
Fix: const total = items.reduce(sum, 0)
Check: render with a changed items prop and assert the displayed total in the same commit.
```

Call a documented rule violation a defect. Label file layout, naming, and hook-extraction taste as
preferences, and say which is which.
