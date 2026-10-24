# React source basis

Use this mapping to verify a lesson before changing it. Official documentation establishes the
contracts; registries establish version facts; the lint and Strict Mode rules establish which
mistakes are mechanically detectable. Documentation links were checked on 23 August 2026 and again in October 2026;
the observed sections were added in October 2026, with each behaviour reproduced on React
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

## Rules, lint, and Strict Mode

- [Rules of React](https://react.dev/reference/rules) and
  [`eslint-plugin-react-hooks`](https://registry.npmjs.org/eslint-plugin-react-hooks) establish the rules
  the lint plugin checks; [`StrictMode`](https://react.dev/reference/react/StrictMode) establishes the
  development-only double invocation of bodies, effects and ref callbacks, which supports the profiling
  caveat in `performance.md`.
- [Preserving and resetting state](https://react.dev/learn/preserving-and-resetting-state) establishes
  that changing `key` resets and remounts a subtree.

## Effects, refs, context, and stores

- [You might not need an Effect](https://react.dev/learn/you-might-not-need-an-effect) supplies the
  replacement rows in `effects.md`; [Synchronizing with Effects](https://react.dev/learn/synchronizing-with-effects)
  establishes cleanup and stale-response handling;
  [Removing Effect dependencies](https://react.dev/learn/removing-effect-dependencies) establishes
  changing what the effect depends on rather than trimming the array.
- [`useContext`](https://react.dev/reference/react/useContext) establishes consumer re-render on an
  `Object.is` change of the provider value.
- [`useSyncExternalStore`](https://react.dev/reference/react/useSyncExternalStore) establishes the stable
  `subscribe`, the cached `getSnapshot` and its infinite-loop error, and the server snapshot.

## Concurrency, Suspense, and actions

- [`useTransition`](https://react.dev/reference/react/useTransition) and
  [`useDeferredValue`](https://react.dev/reference/react/useDeferredValue) establish non-urgent updates,
  the pending flag, and that updates after an `await` leave the transition.
- [`useFormStatus`](https://react.dev/reference/react-dom/hooks/useFormStatus) establishes that it reads
  only the parent `<form>`.

## Server and client boundaries

- [`'use client'`](https://react.dev/reference/rsc/use-client) establishes the transitive module boundary,
  the serializable props, and that Server Components passed as props stay on the server.
- [`'use server'`](https://react.dev/reference/rsc/use-server) establishes that Server Function arguments
  are client-controlled, which is why `security.md` treats each one as a public endpoint.
- [`suppressHydrationWarning`](https://react.dev/reference/react-dom/components/common#common-props)
  establishes that it applies one level deep and only silences the warning.

## Performance and migration

- [`<Profiler>`](https://react.dev/reference/react/Profiler) supports measuring render time;
  [`memo`](https://react.dev/reference/react/memo) establishes the shallow prop comparison.
- The [React 19 upgrade guide](https://react.dev/blog/2024/04/25/react-19-upgrade-guide) is the source of
  the removals, the silently ignored `propTypes`, the error-reporting change, `ref` as a prop, and the
  TypeScript changes in `versions-and-migration.md`.

## Tests

- [`act`](https://react.dev/reference/react/act) establishes its import from `react` and that testing
  libraries wrap it.

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
  `configs.recommended` crashes a flat config; stale closures and async effects are warnings;
  `static-components` reports a nested component rendered directly but not one rendered from a `.map`
  callback.
- Observed: a component carrying `// eslint-disable-next-line react-hooks/exhaustive-deps` is skipped by
  the compiler ("one or more React ESLint rules were disabled").
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
- Observed under Vitest without `globals: true`: the second test in a file found the first test's DOM
  ("Found multiple elements"); `afterEach(cleanup)` fixes it.
- Observed: `isPending` stays true across an awaited async action.

## Types

- Observed with TypeScript 7.0.2 and `@types/react` 19: a hook returning `[value, fn]` without `as const`
  makes `fn()` fail with TS2349; `useRef<HTMLDivElement>(null)` holds `HTMLDivElement | null`;
  `ComponentProps<'button'>` spreads onto a `<button>`.

## Judgments not stated by the sources

These are the skill's own judgments, not claims made by the sources above:

- Classifying a defect first — impure render, misplaced state, unnecessary effect, untracked
  external value, tear, or measured slowness — is a local triage order. React documents the rules
  individually; the ordering is ours.
- "Move state down before memoizing" generalizes from the documented costs of memoization and the
  measured table in `performance.md`; React does not publish that ranking.
- Keeping Server Components on the server by passing them as `children` follows from the documented
  transitive-boundary behaviour; React does not state it as a rule.

Omitted on purpose: undated blog tutorials, class-component-era advice presented as current, and
performance claims without a stated measurement method.
