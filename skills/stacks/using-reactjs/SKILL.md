---
name: using-reactjs
description: Use when building, reviewing, debugging, upgrading, or securing React components and hooks, including rendering purity, state ownership, effects and their alternatives, refs, context, external stores, transitions, Suspense and form actions, server and client components and hydration, the React Compiler, rendering performance, prop and hook typing, and React-focused tests. It supplies React rules, the failures each one prevents, and the evidence that proves a fix. Do not use it for React Native platform work, for Vue or another framework, or for plain JavaScript or TypeScript in a React project that never touches a component.
---

# Use React

Make render purity, state ownership, and effect necessity explicit before changing a component.

Most React defects are not syntax errors. They are a value derived in state instead of during
render, an effect standing in for an event handler, or a store read that React cannot see. Find the
category first.

## Check the installed version and setup

```sh
npm ls react react-dom react-server-dom-webpack react-server-dom-turbopack react-server-dom-parcel next
grep -rl "babel-plugin-react-compiler\|reactCompiler" package.json vite.config.* next.config.* babel.config.* 2>/dev/null
```

This skill targets React 19 on the stable channel. Never make a development-only warning, an
`unstable_` API, a canary or experimental build, or an undocumented internal a production default;
they sit outside React's semver guarantee. If the project is on React 18 or earlier, say so and scope
the advice. Read [versions-and-migration.md](references/versions-and-migration.md) before an upgrade:
19.1 to 19.3 changed behaviour (the `useId` format, transitions committing separately, `onReset` on
form actions).

Record whether the app uses Server Components and whether the React Compiler is on. Both change which
advice applies, and neither is visible from a component file.

## Work in this order

1. Record the versions, Server Components, and the compiler.
2. Reproduce the symptom and classify it: impure render, misplaced state, unnecessary effect, an
   untracked external value, a concurrency-visible tear, a hydration mismatch, or measured slowness.
3. Fix ownership and purity before reorganizing files or adding memoization.
4. Prefer removing an effect over correcting its dependency array.
5. Prove the fix through rendered output and user-visible behavior, not through internal state.

## Keep components and hooks pure

React may call a component more than once for the same input, and it can discard or replay a
render. Components and hooks must be idempotent, side effects stay out of render, and props, state,
hook arguments, and values already used in JSX are treated as immutable.

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

The bad version double-counts the analytics event under a double render and silently edits data
another component may still render from. Strict Mode surfaces this class of bug in development.

Call Hooks only at the top level of a component or another Hook. Never call a component as a plain
function, and never declare a component inside another component: it is a new type on every render,
so its subtree remounts and loses state each time, and the lint rules do not report a plain nested
`function Item()`.

## Lint, and gate on warnings

`eslint-plugin-react-hooks` 7 checks the Rules of React (refs read during render, impure calls, set
state in render or synchronously in an effect) as well as hook order and dependencies. In a flat
config the object is `reactHooks.configs.flat.recommended`; `configs.recommended` crashes a flat
config. Stale closures and `useEffect(async () => …)` are only warnings, so run
`npx eslint . --max-warnings 0`.

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
from an effect: the effect version renders once with stale values before it corrects itself.

## Question every effect

An effect is for synchronizing with a system outside React. If no external system is involved, the
work belongs in render or in an event handler. [effects.md](references/effects.md) holds the table
of unnecessary effects and their replacements; read it before writing or keeping a `useEffect`.
Rendered data belongs in state, never in a `useRef`.

## Traps that render without an error

| Code | What happens | Instead |
|---|---|---|
| `use(fetchThing(id))` in a Client Component | a promise created during render is new every render: the fallback stays forever and the component re-renders about 100 times a second, usually with no warning | create the promise outside render (a Server Component, a loader, a cache keyed by id) |
| `useDeferredValue(query)` passed to a slow child without `memo` | the keystroke still renders the slow child with the old value, then again in the background: no gain | wrap the child in `memo`, or confirm the compiler compiled the parent |
| An uncontrolled input in a `<form action>` | React resets the form after the action, even when it returns a validation error, so the user's input disappears | return the submitted values and feed them back as `defaultValue`, or control the field |
| A server/client difference in an attribute (`className`, `href`) | React 19 never patches attributes during hydration, and production logs nothing | render the same on both sides; switch after mount with `useSyncExternalStore` and a server snapshot |
| A `useRef` "run once" guard around a fetch with an abort cleanup | Strict Mode keeps the ref across its simulated remount, so the retry is skipped and the data never loads in development | delete the guard; the double request in development is the check working |
| `<div {...dataFromApi} />` | user data can carry `dangerouslySetInnerHTML` or `srcDoc`; React blocks only `javascript:` URLs, not `data:` | pick known keys; allow-list URL protocols |

Read [security.md](references/security.md) before rendering user content, reading environment
variables in client code, or deciding whether a Server Components app is patched: the Server Components
runtime has had a long run of critical advisories, `npm audit` has lagged behind them, and some
frameworks ship their own copy of it.

## Read only the needed reference

- Purity, derived values, state placement, and list identity:
  [rendering-and-state.md](references/rendering-and-state.md)
- An effect that fires too often, never cleans up, or should not exist:
  [effects.md](references/effects.md)
- Refs, context shape, and reading a store React does not own:
  [refs-context-and-stores.md](references/refs-context-and-stores.md)
- Transitions, deferred values, Suspense boundaries, form actions, and optimistic updates:
  [concurrency-and-suspense.md](references/concurrency-and-suspense.md)
- Server Components, `'use client'`, props that cross the boundary, and hydration:
  [server-and-client.md](references/server-and-client.md)
- XSS through props, client-side secrets, and Server Components advisories:
  [security.md](references/security.md)
- Profile-led rendering work, the React Compiler, and what memoization actually costs:
  [performance.md](references/performance.md)
- Behavior-first component tests, `act`, fake timers, and async assertions:
  [testing.md](references/testing.md)
- React 19.x removals, behaviour changes, and upgrade evidence:
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
