# React source basis

Use this mapping to verify a lesson before changing it. Official documentation establishes the
contracts; registries establish version facts; the lint and Strict Mode rules establish which
mistakes are mechanically detectable. The links in the first sections were checked on 23 August 2026;
the sections from "Security" on were added in October 2026, with each behaviour reproduced on React
19.3.1, eslint-plugin-react-hooks 7.1.1, babel-plugin-react-compiler 1.0.0, Vitest 4 and 5, Testing
Library 16 on Node 25, in jsdom or `react-dom/server`.

## Version scope

- [React versions](https://react.dev/versions) and the
  [npm registry entry for `react`](https://registry.npmjs.org/react/latest) establish the current
  stable release; the current major is 19, so the skill scopes itself to React 19.x. Query the
  registry at review time for the exact version.
- [Versioning policy](https://react.dev/community/versioning-policy) establishes semver on the
  stable channel and states that development-only warnings, `unstable_`-prefixed APIs, canary and
  experimental builds, and undocumented internals are excluded from the major-version guarantee.
  It supports the "never make one of these a production default" rule in `SKILL.md` and
  `versions-and-migration.md`.

## Rules of React

- [Rules of React](https://react.dev/reference/rules) establishes the three rule families:
  components and Hooks must be pure and idempotent with side effects outside render; React calls
  components and Hooks, so neither may be invoked or passed as a plain value; Hooks are called only
  at the top level of a React function. It also recommends Strict Mode and the Hooks lint plugin.
- [Components and Hooks must be pure](https://react.dev/reference/rules/components-and-hooks-must-be-pure)
  establishes the immutability of props, state, Hook arguments and returns, and values already used
  in JSX. It supports the mutation pair in `SKILL.md` and the JSX-mutation pair in
  `rendering-and-state.md`.
- [Rules of Hooks](https://react.dev/reference/rules/rules-of-hooks) establishes the top-level and
  React-function-only constraints.
- [`StrictMode`](https://react.dev/reference/react/StrictMode) establishes that development-only
  double invocation covers component bodies, state initializers and updaters, `useMemo` and
  `useReducer` functions, effect setup–cleanup–setup, and ref-callback setup–cleanup–setup, and that
  none of it affects production. It supports the "an effect that breaks under remount will break in
  production" claim in `effects.md` and the profiling caveat in `performance.md`.
- [`eslint-plugin-react-hooks`](https://registry.npmjs.org/eslint-plugin-react-hooks) is the
  maintained lint implementation of these rules.

## State, derivation, and identity

- [You might not need an Effect](https://react.dev/learn/you-might-not-need-an-effect) is the source
  of the unnecessary-effect table in `effects.md`. It
  supplies every row: transforming data for rendering, caching with `useMemo`, handling user events,
  resetting state with a `key`, adjusting state on prop change, sharing logic between handlers,
  chains of computations, notifying parents, and subscribing to an external store.
- [Choosing the state structure](https://react.dev/learn/choosing-the-state-structure) establishes
  avoiding redundant and duplicated state and holding an id rather than a copied object.
- [Preserving and resetting state](https://react.dev/learn/preserving-and-resetting-state)
  establishes that position and `key` determine identity, and that changing `key` resets a subtree.
- [Sharing state between components](https://react.dev/learn/sharing-state-between-components)
  establishes lifting state to the closest common owner.
- [Rendering lists](https://react.dev/learn/rendering-lists) establishes that keys must be stable
  and unique among siblings, and warns against index keys for reorderable lists and against keys
  generated during render.

## Effects

- [Synchronizing with Effects](https://react.dev/learn/synchronizing-with-effects) establishes that
  effects exist to synchronize with systems outside React, and supplies the cleanup requirement and
  the ignore-stale-response pattern used in `effects.md`.
- [Lifecycle of reactive Effects](https://react.dev/learn/lifecycle-of-reactive-effects) and
  [Removing Effect dependencies](https://react.dev/learn/removing-effect-dependencies) establish
  that every reactive value read must be declared, and that the correct remedy is changing what the
  effect depends on rather than trimming the array. They support the "do not lie about the
  dependency array" rule.

## Refs, context, and external stores

- [`useRef`](https://react.dev/reference/react/useRef) establishes that mutating a ref does not
  trigger a render and that `ref.current` must not be read or written during render.
- [`useContext`](https://react.dev/reference/react/useContext) establishes that consumers re-render
  when the provider value changes by `Object.is`, and shows memoizing the provider value. It
  supports the provider-identity pair in `refs-context-and-stores.md`.
- [`useSyncExternalStore`](https://react.dev/reference/react/useSyncExternalStore) establishes the
  stable-`subscribe` requirement, the cached-immutable-`getSnapshot` requirement compared with
  `Object.is`, the "The result of `getSnapshot` should be cached" error and its infinite-loop cause,
  and the server-snapshot contract for hydration. It is the source of both code pairs in that file.

## Concurrency and Suspense

- [`useTransition`](https://react.dev/reference/react/useTransition) and
  [`useDeferredValue`](https://react.dev/reference/react/useDeferredValue) establish marking updates
  as non-urgent, the pending flag, and the caution that a controlled input's own value must not be
  deferred. They support the search-field pair in `concurrency-and-suspense.md`.
- [`<Suspense>`](https://react.dev/reference/react/Suspense) establishes the fallback region, that
  an already-visible region can be kept visible by updating inside a transition, and that Suspense
  does not catch errors.

## Server and client boundaries

- [`'use client'`](https://react.dev/reference/rsc/use-client) establishes that the directive marks
  a module and its transitive imports as client code, that re-declaring it below a boundary has no
  further effect, and the exact serializable-prop list and its exclusions. It is the source of both
  the boundary-placement guidance and the serialization table in `server-and-client.md`.
- [`'use server'`](https://react.dev/reference/rsc/use-server) establishes Server Functions and
  states that arguments and return values cross the network boundary, which is why `security.md` treats
  every Server Function as a public endpoint requiring its own authorization and validation.

## Performance

- [`<Profiler>`](https://react.dev/reference/react/Profiler) establishes programmatic render timing
  and warns that profiling adds overhead, supporting the measure-in-production-mode rule.
- [`useMemo`](https://react.dev/reference/react/useMemo) and
  [`memo`](https://react.dev/reference/react/memo) establish that memoization has its own cost, that
  `memo` compares props shallowly, and that a new object or function prop defeats it. They supply
  the two "pointless" examples in `performance.md`.
- [React Compiler](https://react.dev/learn/react-compiler) establishes that the compiler applies
  memoization automatically based on the Rules of React and depends on those rules holding.

## Tests

- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/), its
  [guiding principles](https://testing-library.com/docs/guiding-principles/),
  [query documentation](https://testing-library.com/docs/queries/about/), and
  [`user-event`](https://testing-library.com/docs/user-event/intro/) establish resembling real
  usage, the accessible-query priority, the `getBy`/`queryBy`/`findBy` distinction, and that
  `user-event` reproduces the full interaction a real user causes.
- [`act`](https://react.dev/reference/react/act) establishes that updates must be wrapped so effects
  flush before assertions, that testing libraries wrap it for you, and its import location in the
  `react` package.

## Migration

- The [React 19 upgrade guide](https://react.dev/blog/2024/04/25/react-19-upgrade-guide) is the
  source of both removal tables in `versions-and-migration.md`, the silently-ignored `propTypes`
  behavior, the render-error reporting change with `onUncaughtError` and `onCaughtError`, `ref` as a
  regular prop, the `element.ref` deprecation, the UMD removal, and the TypeScript changes.

## Security

- The repository's [security advisories](https://github.com/facebook/react/security/advisories) list the
  Server Components advisories: unauthenticated remote code execution (CVE-2025-55182, December 2025),
  source-code exposure (CVE-2025-55183), and a series of denial-of-service bugs through 2026, with a
  further critical remote-code-execution advisory published 14 October 2026. As of 23 October 2026 the
  unaffected releases were 19.0.9, 19.1.10, 19.2.9 and 19.3.1. The
  [December 2025 post](https://react.dev/blog/2025/12/11/denial-of-service-and-source-code-exposure-in-react-server-components)
  says previously patched apps must update again, lists affected frameworks, and states that hardcoded
  secrets in Server Function source were exposed while runtime environment values were not.
- Observed: `npm audit` reported 0 vulnerabilities for `react-server-dom-webpack` 19.2.8, which the
  October advisory affects, because that advisory was not yet in the global database.
- Observed: a Next.js 16 App Router project vendors React and the Server Components runtime under
  `next/dist/compiled`, so `npm ls react-server-dom-webpack` is empty. Next.js publishes its own
  advisories for the same bugs.
- Observed: React 19 replaces `javascript:` URLs in `href`, `src`, `action` and `formAction`; `data:` URLs,
  `srcDoc` and `dangerouslySetInnerHTML` pass through; spreading parsed JSON renders
  `dangerouslySetInnerHTML`.
- Observed: a Vite build inlines `VITE_`-prefixed variables and the whole `import.meta.env` object.
- Observed: `server-only` throws unless the `react-server` condition is set.

## React 19.1 to 19.3 behaviour

- [React 19.2](https://react.dev/blog/2025/10/01/react-19-2) and
  [React 19.3](https://react.dev/blog/2026/09/09/react-19-3) establish `useEffectEvent`, `<Activity>`, the
  `useId` format change, independent transitions, `onReset` on automatic form reset, Strict Mode effects
  during hydration, and `browser()`.
- Observed: `use()` on a promise created during render stayed on the fallback with about 50 renders in
  500 ms and no warning; a cached promise resolved in 3 renders. [`use`](https://react.dev/reference/react/use)
  says to create promises outside render.
- Observed: form actions reset uncontrolled inputs even when returning an error;
  [`<form>`](https://react.dev/reference/react-dom/components/form).
- Observed: `useOptimistic` outside a transition shows nothing and logs an error; inside, it rolls back.
- Observed: hydration patches text mismatches by client rendering and never patches attribute
  mismatches, with no production message.
- Observed: a `useRef` run-once guard with an abort cleanup never loads under Strict Mode;
  [Synchronizing with Effects](https://react.dev/learn/synchronizing-with-effects#how-to-handle-the-effect-firing-twice-in-development)
  advises against the guard.
- Observed: `useEffect(async …)` throws `destroy is not a function` on unmount.
- Observed: a ref callback returning a cleanup is not called with `null`; an inline one re-attaches
  every render.
- Observed: Suspense commits the fallback, pre-renders siblings, and reveals about 300 ms after
  resolution; [React 19 release post](https://react.dev/blog/2024/12/05/react-19).

## React Compiler and lint

- Observed with babel-plugin-react-compiler 1.0.0: components that read refs in render, mutate props,
  set state in render or write module variables are skipped with no build error; the `logger` and
  `panicThreshold: 'all_errors'` report them; compiled output contains `react.memo_cache_sentinel`.
- Observed: a library hook returning a mutated stable object renders stale UI when compiled; community
  reports in [TanStack Table #5903](https://github.com/TanStack/table/issues/5903) and
  [#6601](https://github.com/TanStack/table/issues/6601).
- [React Compiler 1.0](https://react.dev/blog/2025/10/07/react-compiler-1) recommends leaving existing
  memoization in place and keeping `useMemo`/`useCallback` as escape hatches.
- Observed with eslint-plugin-react-hooks 7.1.1 and ESLint 10: `configs.flat.recommended` works,
  `configs.recommended` crashes a flat config; stale closures and async effects are warnings; a plain
  nested component function is not reported.
- Observed: `useDeferredValue` without `memo` on a 50 ms child gave a 51 ms keystroke against under 1 ms
  with `memo`; [`useDeferredValue`](https://react.dev/reference/react/useDeferredValue) says `memo` is
  required.

## Measured costs

- 2,000 children, production build in jsdom, median of 40 `flushSync` updates after 5 warm-ups, two runs
  within 10%: the numbers in `performance.md` and the context fan-out in `refs-context-and-stores.md`.
  jsdom has no layout or paint, so these are reconciliation and DOM-call costs.

## Testing

- Observed with Vitest 4 and 5 and Testing Library 16: `vi.useFakeTimers()` hangs `user-event` and `findBy*`,
  with or without `advanceTimers`; `shouldAdvanceTime: true` works. Cause in Testing Library's async
  wrapper, which advances timers only when `jest` exists; community report
  [testing-library/react-testing-library#1197](https://github.com/testing-library/react-testing-library/issues/1197).
- Observed: `act` without `IS_REACT_ACT_ENVIRONMENT` warns that the environment is not configured.

## Judgments not stated by the sources

These are the skill's own judgments, not claims made by the sources above:

- Classifying a defect first — impure render, misplaced state, unnecessary effect, untracked
  external value, tear, or measured slowness — is a local triage order. React documents the rules
  individually; the ordering is ours.
- "Fix ownership and purity before memoizing" and the structural-cause table in `performance.md`
  generalize from the documented costs of memoization; React does not publish that ranking.
- Requiring a test to be proven by breaking the code it covers is a local evidence standard.
- The claim that pushing `'use client'` down the tree is usually preferable follows from the
  documented transitive-boundary behavior, but React does not state it as a rule.

Omitted on purpose: undated blog tutorials, class-component-era advice presented as current, and
performance claims without a stated measurement method.
