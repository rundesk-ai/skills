# React server and client boundaries

The first two sections apply only where React Server Components are in use: an RSC build, a framework
that documents support, or `'use client'` already in the tree. Hydration applies to any app rendered on
the server. Security for both is in [security.md](security.md).

## Keep server code on the server

`'use client'` marks a module and everything it imports as client code. A Server Component imported into
a client module becomes client code too, but one passed to it as `children` (or any prop) stays on the
server. So wrap a context provider or an interactive shell in a small client component that takes
`children`, and render the server content inside it from the server side, instead of moving the whole
layout to the client.

## Pass data across the boundary, not behaviour

An ordinary function or a class instance passed from a Server Component to a Client Component fails with
a serialization error. Flattening a class instance into a plain object to get past the error also strips
its methods, so decide deliberately where the behaviour lives. Passing a promise is the intended way to
stream a value the client will read with `use()`.

## Hydration renders must match

The server's HTML and the client's first render must produce the same output. React 19 handles the two
kinds of mismatch differently:

- **Text** that differs makes React discard the server HTML for that boundary and render it again on the
  client. Development logs a diff; production logs a minified error #418.
- **Attributes** that differ (`className`, `href`, `style`) are never patched: the server's value stays
  in the DOM. Development warns ("This won't be patched up"); production logs nothing. A wrong theme
  class or a link to the wrong locale survives, and checking production logs finds nothing.

Usual causes: `Date.now()`, `Math.random()`, `typeof window` branches, locale or time-zone formatting,
and reading `localStorage` during render. Render the same thing on both sides and switch after mount:
`useSyncExternalStore` with a `getServerSnapshot` that returns the server's value, or, from 19.3,
`use(browser())` inside a Suspense boundary, which renders the fallback on the server and the real
content on the client.

`suppressHydrationWarning` hides the warning for one element's own text and attributes and fixes
nothing: the server's attribute value still stays in the DOM. Use it only for content that is meant to
differ, such as a timestamp.

Prove it: render with `renderToString`, then `hydrateRoot` that HTML in a DOM environment with the
development build, and read the warning. The production build will not tell you.

## Prove the boundary

Inspect the payload sent to the browser for fields that should not be there, confirm which modules ended
up in the client bundle, and call a Server Function directly rather than only through the UI that
normally calls it.
