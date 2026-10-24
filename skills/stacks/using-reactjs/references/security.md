# React security

Read this before rendering content that came from users, a CMS, a URL or a database; before reading
environment variables in client code; and before saying a Server Components app is patched.

## What React escapes and what it does not

React escapes text and attribute values, and since React 19 it replaces a `javascript:` URL in `href`,
`src`, `action` and `formAction` with one that throws, whatever its case or embedded whitespace. That is
the whole of it:

- `data:` and other schemes pass through unchanged; an `<iframe src>` or `<object data>` taking a user URL
  needs an allow-list (`new URL(value).protocol` in `https:`, `mailto:`).
- `dangerouslySetInnerHTML` inserts the string as HTML, and `<img src=x onerror=…>` in it runs.
  Sanitize with a maintained HTML sanitizer, or render the content as text.
- `srcDoc` on an iframe is escaped as an attribute, and the browser then parses it as a whole document,
  scripts included.
- Spreading an object you did not build onto an element hands it every prop:
  `<div {...JSON.parse(body)} />` renders `dangerouslySetInnerHTML` if the JSON has that key. Lowercase
  `onclick` strings are dropped, but `dangerouslySetInnerHTML`, `srcDoc`, `href` and `style` are not.
  Destructure the keys you expect: `const { label, title } = data`.

Prove it: render the component with the hostile payload through `renderToString` from
`react-dom/server` in a Node script, and read the HTML.

## Client environment variables are public

A variable under the client prefix (`VITE_`, `NEXT_PUBLIC_`, the older `REACT_APP_`) is replaced by its
literal value in the shipped JavaScript, and referencing the whole `import.meta.env` object ships every
prefixed value. Keep secrets unprefixed and read them only on the server. Prove it: build, then search
the output directory for the secret's value (`grep -r "<value>" dist/`).

## Server Components runtime advisories

The `react-server-dom-*` packages, which run Server Components and Server Functions on the server, have
had a long series of advisories since December 2025: unauthenticated remote code execution, source-code
exposure, and repeated denial-of-service bugs, each fixed by new patch releases of every supported minor
line. A version that was "the fix" a month earlier can be vulnerable again, and not every advisory gets a
post on the React blog.

To check a project:

1. List what is installed: `npm ls react-server-dom-webpack react-server-dom-turbopack react-server-dom-parcel`.
2. Compare it with the repository's security advisories page (github.com/facebook/react/security/advisories),
   not only with `npm audit`: a critical advisory was missing from the global advisory database, and so
   from `npm audit`, days after it was published.
3. Check the framework too. A framework can ship its own build of React and the Server Components
   runtime: in a Next.js App Router project `npm ls react-server-dom-webpack` prints nothing, the copy
   lives under `node_modules/next/dist/compiled/`, and upgrading `react` patches nothing. Upgrade the
   framework to the release its own advisory names.
4. An app with no server-side React, or no framework or bundler plugin that supports Server Components,
   is not affected; say which case applies.

The source-exposure bug returned Server Function source code to the caller, so a key written into a
Server Function's body was readable; values read from the environment at run time were not.

## Server Functions are endpoints

Every function marked `'use server'` can be called by anyone with any arguments, whatever UI normally
calls it. Authenticate, authorize and validate inside it, as you would in a route handler. Props a Server
Component passes to a Client Component are serialized into the page payload: shape the object at the
boundary rather than passing a whole record and trusting the client not to render some fields.

The `server-only` package throws when imported outside the `react-server` export condition, which marks
a module as server-only in a Server Components build. In a unit test it throws too, unless the runner sets
that condition or the module is mocked.
