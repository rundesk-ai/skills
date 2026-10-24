---
name: using-reactjs
description: Use when building, reviewing, debugging, upgrading, or securing React components and hooks in JSX or TSX, including rendering purity, state ownership, effects and their alternatives, refs, context, external stores, transitions, Suspense and form actions, React Server Components and hydration, the React Compiler, rendering performance, prop and hook types, and component tests. It supplies React rules, the failures each one prevents, and the evidence that proves a fix. Do not use it for React Native platform work, for Vue or another framework, or for plain JavaScript or TypeScript in a React project that touches no component or hook.
---

# Use React

Most React defects are not syntax errors. They are a value derived in state instead of during render,
an effect standing in for an event handler, or a store read that React cannot see. Classify the defect
before changing code: impure render, misplaced state, unnecessary effect, an untracked external value, a
hydration mismatch, or measured slowness.

## Check the installed version and setup

```sh
npm ls react react-dom react-server-dom-webpack react-server-dom-turbopack react-server-dom-parcel next
grep -rl "babel-plugin-react-compiler\|reactCompiler" package.json vite.config.* next.config.* babel.config.* 2>/dev/null
```

This skill targets React 19 on the stable channel. Never make a development-only warning, an
`unstable_` API, a canary or experimental build, or an undocumented internal a production default; they
sit outside React's semver guarantee. If the project is on React 18 or earlier, say so and scope the
advice. Record whether the app uses Server Components and whether the React Compiler is on: both change
which advice applies, and neither is visible from a component file. Read
[versions-and-migration.md](references/versions-and-migration.md) before an upgrade: 19.1 to 19.3 changed
behaviour (the `useId` format, transitions committing separately, `onReset` on form actions).

## Lint, and gate on warnings

`eslint-plugin-react-hooks` 7 checks the Rules of React (refs read during render, impure calls, state set
in render or synchronously in an effect, components created during render) as well as hook order and
dependencies. In a flat config the object is `reactHooks.configs.flat.recommended`; `configs.recommended`
crashes a flat config. Stale closures and `useEffect(async () => …)` are only warnings, so run
`npx eslint . --max-warnings 0`. A component declared inside another one and rendered from a `.map`
callback is not reported; it is a new type every render, so its rows remount and lose state.

Do not silence a hooks rule with `eslint-disable`: where the React Compiler is on, a disabled React rule
makes the compiler skip that whole component, silently. Fix the dependency instead.

## Prefer deriving over storing, and removing over fixing

State is for values that cannot be computed; derive the rest during render. To reset state when the
identity of the thing changes, change its `key` (which also remounts the subtree, rebuilding anything
expensive inside) rather than clearing state in an effect. An effect is for synchronizing with a system
outside React; if none is involved, the work belongs in render or an event handler, and removing the
effect beats correcting its dependency array. Read [effects.md](references/effects.md) before writing or
keeping a `useEffect`.

## Traps that render without an error

| Code | What happens | Instead |
|---|---|---|
| `use(fetchThing(id))` in a Client Component | a promise created during render is new every render: the fallback stays forever and the component re-renders about 100 times a second, usually with no warning | create the promise outside render (a Server Component, a loader, a cache keyed by id) |
| `useDeferredValue(query)` passed to a slow child without `memo` | the keystroke still renders the slow child with the old value, then again in the background: no gain | wrap the child in `memo`, or confirm the compiler compiled the parent |
| An uncontrolled input in a `<form action>` | React resets the form after the action, even when it returns a validation error, so the user's input disappears | return the submitted values and feed them back as `defaultValue`, or control the field |
| A server/client difference in an attribute (`className`, `href`) | React 19 never patches attributes during hydration, and production logs nothing | render the same on both sides; switch after mount (see [server-and-client.md](references/server-and-client.md)) |
| A `useRef` "run once" guard around a fetch with an abort cleanup | Strict Mode keeps the ref across its simulated remount, so the retry is skipped and the data never loads in development | delete the guard; the double request in development is the check working |
| `useEffect(async () => { … })` | the promise is taken for a cleanup function: an error on mount, `destroy is not a function` on unmount | define the async function inside the effect and call it |
| `<div {...dataFromApi} />` | user data can carry `dangerouslySetInnerHTML` or `srcDoc`; React blocks only `javascript:` URLs, not `data:` | pick known keys; allow-list URL protocols |

Read [security.md](references/security.md) before rendering user content, reading environment variables
in client code, or deciding whether a Server Components app is patched: the Server Components runtime has
had a long run of critical advisories, `npm audit` has lagged behind them, and some frameworks ship their
own copy of it.

## Types for components and hooks

- A custom hook that returns a tuple needs `as const`: `return [on, toggle]` is inferred as an array of
  `boolean | (() => void)`, so every caller's `toggle()` fails to type-check (TS2349).
- A wrapper takes `ComponentProps<'button'>` and spreads the rest, instead of re-declaring DOM props by
  hand.
- In React 19, `useRef<HTMLDivElement>(null)` holds `HTMLDivElement | null`, `useRef` requires an
  argument, and `ref` is an ordinary prop, so a component accepts it without `forwardRef`.

## Read only the needed reference

- An effect that fires too often, never cleans up, or should not exist: [effects.md](references/effects.md)
- Refs, context shape, and reading a store React does not own:
  [refs-context-and-stores.md](references/refs-context-and-stores.md)
- Transitions, deferred values, Suspense, form actions, and optimistic updates:
  [concurrency-and-suspense.md](references/concurrency-and-suspense.md)
- Server Components, `'use client'`, props that cross the boundary, and hydration:
  [server-and-client.md](references/server-and-client.md)
- XSS through props, client-side secrets, and Server Components advisories:
  [security.md](references/security.md)
- Profile-led rendering work, the React Compiler, and what memoization costs:
  [performance.md](references/performance.md)
- Component tests, `act`, fake timers, and cleanup: [testing.md](references/testing.md)
- React 19.x removals, behaviour changes, and upgrade evidence:
  [versions-and-migration.md](references/versions-and-migration.md)
- Claim-to-source audit map: [sources.md](references/sources.md)

## Report findings as evidence

```text
[HIGH] Profile never loads in development
Location: src/profile/Profile.jsx:9
Evidence: if (didFetch.current) return; didFetch.current = true; ... return () => controller.abort();
Why: Strict Mode keeps the ref across its simulated remount, so the cleanup aborts the first request
     and the guard skips the second.
Fix: delete the guard and keep the abort cleanup.
Check: render inside <StrictMode> in a test and assert the profile appears.
```

Call a documented rule violation a defect. Label file layout, naming, and hook-extraction taste as
preferences, and say which is which.
