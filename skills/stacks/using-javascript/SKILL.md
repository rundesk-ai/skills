---
name: using-javascript
description: Use when writing, reviewing, debugging, or building JavaScript or TypeScript outside a component framework's own model — a Node script, CLI, server handler, worker or npm package, framework-free browser code, or the language underneath any of them — including numbers and money, dates and time zones, promises and unhandled rejections, streams and memory, ESM and CommonJS, package.json, lockfiles and dependency safety, tsconfig and type checking, and untrusted input. It supplies runtime traps, safe defaults, and command-line proof. Do not use it for React or Vue component, hook, or reactivity work.
---

# Use JavaScript

Most JavaScript defects never throw: a value is rounded, shifted, coerced or reordered, and the first
symptom is a wrong number on an invoice. Find the category, reproduce it in a one-file script, and prove
the fix from the command line.

## Establish the target before changing code

```sh
node -v; npm -v; pnpm -v 2>/dev/null; ls node_modules/.bin/tsc 2>/dev/null && npm exec --no -- tsc -v
grep -n -E '"(type|engines|packageManager|module|moduleResolution|strict)"' package.json tsconfig.json 2>/dev/null
ls package-lock.json pnpm-lock.yaml yarn.lock 2>/dev/null
```

- The Node line decides which APIs exist (`RegExp.escape` is missing on 22). Read `engines` and `.nvmrc`
  and test on the lowest supported line; `engines` is advisory, and npm and pnpm only warn.
- Tool defaults change between major versions of npm, pnpm and TypeScript, and a flag the installed
  version does not know may warn and do nothing: `npm i --min-release-age=1` on npm 11.6 installs
  anyway. Check the version before trusting a flag's effect.
- Use the package manager the lockfile belongs to; never switch managers or regenerate the lock to make
  an install pass.

Then read the reference for where the code runs: [Node](references/node.md),
[the browser](references/browser.md), and [TypeScript](references/typescript.md) when there is a
`tsconfig.json` or `.ts` files.

## Values that are wrong without an error

| Code | What happens | Instead |
|---|---|---|
| Money in floats, `x.toFixed(2)` | 1.005 is stored just below 1.005, so `(1.005).toFixed(2)` is `"1.00"`, while `Intl.NumberFormat` shows `$1.01`; amounts rounded separately stop adding up | integer minor units (the exponent comes from the currency: JPY has none), one explicit rounding, `Intl.NumberFormat` only to display |
| `JSON.parse` of a 64-bit id | `9007199254740993` becomes `9007199254740992`, and two ids can collide | ids as strings in the API; at the boundary, the reviver's `context.source` (`(k, v, ctx) => k === 'id' ? ctx.source : v`) |
| `new Date('2026-03-08')` | a date-only string is UTC midnight; local getters show 7 March west of UTC. A date-time without an offset is local | keep calendar dates as `YYYY-MM-DD` strings or parse the parts; format with `Intl.DateTimeFormat` and an explicit `timeZone` |
| `new Date('2026-02-30')` | rolls over to 2 March; `isNaN` passes | rebuild the date and compare year, month and day with the input |
| `sort((a, b) => a > b)`, or `arr.sort()` on an array you were given | a boolean comparator leaves the array unsorted, silently; `sort` reorders the caller's array in place | a comparator returning a negative, zero or positive number; `toSorted` |
| `str.replace(x, userValue)` | `$&`, `$'` and `$$` in the value are patterns; a string pattern replaces only the first match | `replace(x, () => userValue)`; `replaceAll` |
| `counts[word] = (counts[word] ?? 0) + 1` | `constructor` and `toString` are inherited keys; `__proto__` stores nothing | `Map` |
| `setTimeout(fn, 30 * 86400000)` | a delay above 2^31 − 1 ms (about 24.8 days) fires after 1 ms; Node warns, browsers do not | store the due time and re-arm in shorter steps |
| `Math.max(...rows)` | `RangeError` at about 120,000 elements, depending on stack depth | a loop or `reduce` |
| `process.env.DEBUG === 'false'` read as `if (process.env.DEBUG)` | every variable is a string or `undefined`, so `'false'` and `'0'` are truthy | parse and check every variable once at start-up, and fail fast on a missing one |
| `JSON.stringify(err)` | `{}`: `message`, `stack` and `cause` are not enumerable | log them explicitly, or `util.inspect(err)` |

Read [Language](references/language.md) for numbers, dates, strings and collections in depth.

## Async failures

- **An unhandled rejection exits Node with code 1.** A `try`/`catch` does not save code that starts two
  promises and then awaits them one at a time: if the second rejects while the first is pending, nothing
  is listening yet. `await Promise.all([a, b])` or `allSettled`. `array.forEach(async ...)` neither waits
  nor lets a throw reach the surrounding `try`.
- **`Promise.all` rejects on the first failure and leaves the rest running**; resources they opened leak.
  Use `allSettled` and clean up what succeeded, or pass an `AbortSignal` and abort.
- **Unbounded fan-out** (`Promise.all(items.map(fetchOne))` over thousands) exhausts sockets and file
  descriptors (`EMFILE`). Run a small pool of workers pulling from a shared index.
- **`fetch` has no total timeout.** Pass `AbortSignal.timeout(ms)`; a timeout rejects with
  `err.name === 'TimeoutError'`, a manual abort with `'AbortError'`. In Node, read or cancel every
  response body (`await res.body?.cancel()`): an unread body keeps its connection out of the pool.

## Untrusted input

Each row works until someone sends a hostile value. Read [Security](references/security.md) before
handling request bodies, file paths, shell commands, URLs, or HTML.

| Work | Default that fails | Do |
|---|---|---|
| Request bodies | concatenating `req` chunks with no limit lets one client exhaust memory | count bytes as they arrive and answer 413 past a limit |
| Merging or path-setting parsed JSON | a recursive merge honours `__proto__` and `constructor.prototype`, so one request makes `({}).isAdmin` true in the whole process | skip those keys and iterate own keys only, merge into `Object.create(null)` or a `Map`, or validate against a schema that rejects unknown keys |
| File paths from input | `path.join` does not confine; `resolved.startsWith(root)` passes a sibling directory that shares the prefix; a symlink leads outside | `realpath` both, then `path.relative(root, target)` must not start with `..` or be absolute |
| Running a program | `exec` with interpolated input runs `; anything` | `execFile` or `spawn` with an argument array and no `shell` option |
| Regular expressions on input | nested quantifiers (`(a+)+`) backtrack exponentially: 28 characters blocked the process for over a second | patterns without overlapping repetition, a length cap first, `RegExp.escape` for user text in a pattern |
| URLs from input | `startsWith('javascript:')` misses `' JaVaScRiPt:'` and `'java\tscript:'`; `//evil.example` and `/\evil.example` are absolute | `URL.parse(input, base)`, then allow-list `protocol`, and compare `origin` before a redirect |
| HTML from input | `innerHTML`, `insertAdjacentHTML` and template-literal HTML run `<img onerror>` | `textContent`, or build elements and set properties |
| Tokens and secrets | `Math.random`; `===` on secrets | `crypto.randomUUID`, `crypto.getRandomValues`; `crypto.timingSafeEqual` on equal-length digests |

## Dependencies are code you run

- **`npx some-tool` without a terminal installs and runs whatever owns that name**, with only a warning.
  An agent's shell has no terminal, so a typo runs a stranger's code: `npx tsc` where TypeScript is not
  installed runs the unrelated `tsc` package. `npm exec --no` refuses a new download but still runs a
  package left in npx's cache by an earlier run, so first confirm the binary is the project's own
  (`ls node_modules/.bin/<tool>`, `npm ls <package>`). Keep the `--` in `npm exec --no -- tool`: without
  it npm takes the tool's flags as its own (`npx --no tsc -v` prints npm's version; `-p` reads as
  `--package`).
- Before adding a package, ask whether the platform already does it (`fetch`, `URL.parse`,
  `crypto.randomUUID`, `util.parseArgs`, `node:test`, `node --env-file`, `node --watch`,
  `structuredClone`). Otherwise check the exact name, its install scripts, its publish date and
  maintainers (`npm view <pkg> time maintainers scripts`).
- Install in CI and reproductions with `npm ci` or `pnpm install --frozen-lockfile`; `npm install`
  rewrites the lock to fit `package.json`. Read the lockfile diff of any dependency change.
- `npm audit` knows published advisories only: a package compromised today reports
  `found 0 vulnerabilities`. Install scripts and release-age gates are in [Node](references/node.md).

## Types are erased

TypeScript checks nothing at run time, and Node and most bundlers strip types without checking them.
Validate data where it enters, and run the type check as its own step (the command is below). Read
[TypeScript](references/typescript.md) for the compiler options that decide what it catches.

## Write it once, for a reader that exists

Duplication and dead code arrive one reasonable edit at a time, often from different agents each
revising code they did not write, and every copy is a place the next fix misses:

- **Before writing a formula, threshold, tolerance, lookup or list of cases, search for it by its
  inputs**, not by the name you would give it: a copy someone else wrote has another name or none.
  Found, call it; not found, give it one home beside its inputs.
- **Never copy a function to change one value or one end**; take the difference as a parameter.
  Copies that already disagree are a bug: decide which is right and prove it with a test.
- **A component, preview, handler or test helper calls the model's rule and reads its state**; it never
  re-derives them or keeps its own copy.
- **Add an output in the same change as the code that reads it.** A prop, field, option or parameter
  nothing reads is dead on arrival, and a test that only exercises it is not a reader. A parameter
  every caller passes the same value is a constant.
- **A comment names only what exists in this repository**: no task or phase id, no document from
  another project, no function that is not there. Those go stale the day they are written.
- **Leave nothing your change made unused.** When new code replaces old, delete the old in the same
  change, then every helper, test, asset (icon, image, sound, scene), configuration key and string only
  it used, until nothing new is unused. Anything that was already unused, list in your hand-off for the
  owner to decide rather than deleting it: it may be kept on purpose. Before finishing, read your diff:
  every new name has a reader.

Two or three repeated lines, or one number meaning two things, are not duplication. `noUnusedLocals`
and `noUnusedParameters` report an unexported declaration and a parameter, never an export nothing
imports: keep a helper unexported until a second module needs it, and before adding or keeping an
export, search every importer, dynamic imports and string-keyed registries included.

## Prove it

```sh
node --test                                # built-in runner; fails a file that leaves a floating rejection
TZ=America/New_York node --test && TZ=Asia/Tokyo node --test   # date code, on both sides of UTC
npm exec --no -- tsc --noEmit -p .         # types, separately from running; `tsc -b` when tsconfig has references
```

A test suite pinned to `TZ=UTC` hides every date bug above; run it in two other zones. Report the
behaviour, the file, and the command whose output proves it. [Sources](references/sources.md) holds the
evidence behind each rule.
