# Using React Validation

This is the current validation record for `using-reactjs`.

## Boundary under test

The skill should activate for React component and hook semantics — render purity, state ownership
and derivation, effects and their alternatives, refs, context, external stores, transitions and
Suspense, server and client component boundaries, rendering performance, and React-focused tests.
It should not activate for Vue or another framework, for React Native platform work, or for a
repository that merely lists React as a dependency the current task never touches.

## Trigger and exclusion cases

| ID | Request shape | Expected behavior |
|---|---|---|
| RCT-T01 | Review a component whose `useEffect` copies props into state | Load |
| RCT-T02 | "Typing in the search box is laggy once results appear" (React never named) | Load |
| RCT-T04 | Change a native module in a React Native application | Do not load; platform work is outside this scope |
| RCT-T05 | Edit a Laravel controller in a repository that also ships a React frontend | Do not load; the task never reaches React |
| RCT-T06 | Upgrade an application from React 18 to React 19 | Load |

## Workflow and authority cases

| ID | Request shape | Expected behavior |
|---|---|---|
| RCT-W01 | `useEffect(() => setFullName(first + ' ' + last), [first, last])` | Derive during render and delete the effect and the state, explaining the extra render pass and the second source of truth |
| RCT-W02 | State cleared from an effect when a prop changes | Use a `key`, and name the one stale render the effect version causes |
| RCT-W03 | A store read mirrored into state through an effect | Move to `useSyncExternalStore`, with a cached `getSnapshot` and a stable `subscribe`, and explain tearing |
| RCT-W04 | An example uses `ReactDOM.render`, `findDOMNode`, or `propTypes` | Check the installed version; identify the React 19 removal and its replacement, and flag that `propTypes` fails silently rather than erroring |
| RCT-W05 | A Server Component passes an event handler to a client child | Reject it against the serialization contract and move the handler into the `'use client'` module |
| RCT-W06 | "I added `useMemo` everywhere and it's much faster now" | Reject fluent assurance; require a production-mode profile before and after and a named metric |
| RCT-W07 | Whether the project uses Server Components cannot be determined | Inspect the build and directives, or stop and name the unknown; do not apply RSC guidance on assumption |
| RCT-W08 | A component test asserts internal state and passes on broken code | Move to accessible queries and prove the test fails against a deliberately broken implementation |

## Provider evidence

Last verification: not yet run against a live provider matrix.

- Claude Code: pending. Cases marked for the sampled run are RCT-T01, RCT-T03, RCT-W06, RCT-T08,
  and RCT-T05.
- Codex: not run.

No case below is marked passed. Record client versions, model identifiers, isolation constraints,
and per-case results here before claiming provider compatibility.

## Limits

This package was built from React's official contracts rather than migrated from an existing
catalog package, so it has no inherited field history. Its trigger boundary and its exclusions
packages and should be exercised first.

RCT-T05 is the shared-repository exclusion case: several supported technologies present, task
touches one. RCT-T07 and RCT-T08 require the composing packages in the same workspace.
