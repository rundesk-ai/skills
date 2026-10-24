# React server and client boundaries

The first two sections apply only where React Server Components are in use: an RSC build, a framework
that documents support, or `'use client'` already in the tree. Hydration applies to any app rendered on
the server. Security for both is in [security.md](security.md).

## Understand what the directive does

`'use client'` at the top of a module marks that module and everything it transitively imports as
client code, creating a boundary in the module graph. It is not a per-component annotation and not a
performance hint. Once a module is imported from a client module, adding the directive again changes
nothing.

A single `'use client'` near the top of the tree therefore pulls the whole subtree to the client. Push
the directive down to the components that need interactivity, state, effects, or browser APIs.

```jsx
// Bad: the directive on the page turns every child into client code.
'use client';
export default function ProductPage({ id }) { /* layout, copy, and one button */ }

// Good: the page stays a Server Component; only the interactive part crosses.
export default function ProductPage({ id }) {
  return <><ProductCopy id={id} /><AddToCart id={id} /></>;
}
// AddToCart.jsx
'use client';
```

## Pass data across the boundary, not behaviour

Props from a Server Component to a Client Component must be serializable: primitives, plain objects and
arrays of them, `Date`, `Map`, `Set`, typed arrays, JSX, promises, and functions only when they are
Server Functions. An ordinary function or a class instance fails at build or request time with a
serialization error. Flattening a class instance into a plain object to get past the error also strips
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

Prove it: render with `renderToString`, then `hydrateRoot` that HTML in a DOM environment with the
development build, and read the warning. The production build will not tell you.

## Prove the boundary

Inspect the payload sent to the browser for fields that should not be there, confirm which modules ended
up in the client bundle, and call a Server Function directly rather than only through the UI that
normally calls it.
