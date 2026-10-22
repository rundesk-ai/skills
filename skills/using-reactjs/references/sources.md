# React source basis

Use this mapping to verify a lesson before changing it. Official documentation establishes the
contracts; registries establish version facts; the lint and Strict Mode rules establish which
mistakes are mechanically detectable. Every link below was opened and checked on 23 August 2026.

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
  states that arguments and return values cross the network boundary, which is why the file treats
  every Server Function as a public endpoint requiring its own authorization and validation.

## Performance

- [`<Profiler>`](https://react.dev/reference/react/Profiler) establishes programmatic render timing
  and warns that profiling adds overhead, supporting the measure-in-production-mode rule.
- [`useMemo`](https://react.dev/reference/react/useMemo) and
  [`memo`](https://react.dev/reference/react/memo) establish that memoization has its own cost, that
  `memo` compares props shallowly, and that a new object or function prop defeats it. They supply
  the two "pointless" examples in `performance.md`.
- [React Compiler](https://react.dev/learn/react-compiler) establishes that the compiler applies
  memoization automatically based on the Rules of React and depends on those rules holding. It
  supports checking whether the compiler is enabled before adding manual memoization.

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
