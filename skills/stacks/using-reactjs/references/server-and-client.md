# React server and client boundaries

Applies only where React Server Components are actually in use — an RSC build, a framework that
documents support, or `'use client'` already in the tree. A plain client-rendered app has no
boundary and none of this applies.

## Understand what the directive does

`'use client'` at the top of a module marks that module and everything it transitively imports as
client code, creating a boundary in the module graph. It is not a per-component annotation and not a
performance hint. Once a module is imported from a client module, adding the directive again changes
nothing.

The practical consequence is that a single `'use client'` near the top of the tree pulls the whole
subtree to the client. Push the directive down to the components that genuinely need interactivity,
state, effects, or browser APIs.

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

## Respect the serialization contract

Props passed from a Server Component to a Client Component must be serializable. Allowed: strings,
numbers, bigints, booleans, `undefined`, `null`, symbols registered with `Symbol.for`, arrays,
`Map`, `Set`, typed arrays and `ArrayBuffer`, `Date`, plain objects of serializable values, JSX
elements, promises, and functions that are Server Functions or exports of a `'use client'` module.

Not allowed: ordinary functions, class instances other than the built-ins above, objects with a null
prototype, and unregistered symbols.

```jsx
// Bad: a plain function cannot cross the boundary.
<Counter onClick={handleClick} />

// Bad: a class instance cannot cross either.
<Row model={new OrderModel(order)} />

// Good: pass data, and let the client module own its handler.
<Counter initialValue={42} />
```

The failure is a build- or request-time serialization error, not a silent degradation — but the
common workaround of flattening a class instance into a plain object also strips its methods, so
decide deliberately where the behavior should live.

Passing a promise is allowed and is the intended way to stream a value the client will await.

## Keep server-only data on the server

A Server Component can read secrets, databases, and the filesystem. The moment a value is passed as
a prop it is serialized into the payload the browser receives. Shape the object at the boundary; do
not pass a whole record and rely on the client not rendering the sensitive fields.

`'use server'` marks Server Functions that a client may call. Every such function is a public
endpoint: authenticate and authorize inside it, and validate its arguments, exactly as you would a
route handler. Being defined next to the component that calls it is not access control.

## Prove the boundary

Inspect the payload actually sent to the browser for fields that should not be there, confirm which
modules ended up in the client bundle, and exercise a Server Function directly rather than only
through the UI that normally calls it.
