# Security

Read this before handling a request body, a file path, a shell command, a regular expression applied to
input, a URL, or a secret. Write each proof as a test that fails on the old code. Putting data into a web
page is covered in [the browser](browser.md).

## Prototype pollution

`JSON.parse('{"__proto__": {"isAdmin": true}}')` creates an ordinary own key named `__proto__`; it does
nothing by itself. A recursive merge, a deep defaults helper, or a dotted-path setter then assigns through
it, and every object in the process inherits `isAdmin`. The `constructor.prototype` route does the same
without the word `__proto__`. After that, `'isAdmin' in user` and `user.isAdmin` are both true for a user
object that never had the key.

```js
const BLOCKED = new Set(['__proto__', 'constructor', 'prototype']);
function merge(target, source) {
  for (const key of Object.keys(source)) {
    if (BLOCKED.has(key)) continue;
    const value = source[key];
    if (value && typeof value === 'object' && !Array.isArray(value)) {
      const base = Object.hasOwn(target, key) && target[key] && typeof target[key] === 'object' ? target[key] : {};
      target[key] = merge(base, value);
    } else {
      target[key] = value;
    }
  }
  return target;
}
```

Also: merge into `Object.create(null)`, hold dynamic keys in a `Map`, read flags with
`Object.hasOwn(user, 'isAdmin')` rather than `in` or a truthy read, and validate request bodies against a
schema that rejects unknown keys. `node --disable-proto=delete` blocks the `__proto__` route but not
`constructor.prototype`: defence in depth, not a fix. Prove it: merge both payloads, then assert
`({}).isAdmin === undefined`.

## File paths

- `path.resolve(root, '/etc/passwd')` ignores `root` entirely, and a symlink inside `root` that points
  outside passes every lexical check, so resolve real paths before comparing.
- Decode percent-encoding before checking: `%2e%2e%2f` is `../` once decoded.
- `realpath` throws for a file that does not exist yet, so for a write, check the real path of the parent
  directory and then join the validated file name.

```js
import path from 'node:path';
import { realpath } from 'node:fs/promises';
async function insideRoot(root, requested) {
  const base = await realpath(root);
  const target = await realpath(path.resolve(base, requested)); // throws ENOENT for a missing file
  const rel = path.relative(base, target);
  return rel !== '' && !rel.startsWith('..') && !path.isAbsolute(rel) ? target : null;
}
```

`rel.startsWith('..')` also rejects a file literally named `..something`, an acceptable cost. A null byte
in a path makes Node throw, so that old trick is gone.

## Running programs

With `execFile` or `spawn` and an argument array, still put `--` before user-supplied operands so a value starting with `-` is not read as an option. Node prints
deprecation `DEP0190` when arguments are passed together with `shell: true`, because they are joined,
not escaped. On Windows, `.bat` and `.cmd` files need a shell, and Node refuses to spawn them without
one.

## Regular expressions on input

Nested quantifiers over overlapping characters (`(a+)+`, `([a-z0-9.]+)+@`) backtrack exponentially on a
string that almost matches: `/^(a+)+$/` took 1.2 s on 28 characters and doubled with each added
character, while the process served nothing else. Write patterns without overlapping repetition (`a+`
instead of `(a+)+`), cap the input length before matching, and pass user text through
`RegExp.escape` (Node 24 and later) before building a pattern from it.

Prove a fix by timing the pattern against input of growing length; the time must stay flat:

```js
for (const n of [20, 25, 30]) {
  const s = 'a'.repeat(n) + '!';
  const t = performance.now();
  pattern.test(s);
  console.log(n, (performance.now() - t).toFixed(1), 'ms');
}
```

V8's experimental linear engine (`node --enable-experimental-regexp-engine`, then the `l` flag) runs a
backtracking pattern in linear time when it uses no backreferences or lookaround; it is a way to confirm
backtracking is the cost, not a portable fix.

## URLs from input

`URL.parse(input, base)` returns `null` instead of throwing. Besides `//evil.example` and
`/\evil.example`, `https://good.example@evil.example/` points at `evil.example`: decide on `url.origin`,
never on a string prefix. A server that fetches a user-supplied URL must also refuse private and loopback
addresses after resolving the host, and re-check every redirect.

## Secrets and randomness

- `===` on a secret leaks timing. `crypto.timingSafeEqual` throws on buffers of different lengths, so
  compare fixed-length digests: HMAC both values with the same key, then compare.
- `eval`, `new Function` and `setTimeout(string)` run code from strings; `node
  --disallow-code-generation-from-strings` proves a codebase does not need them.
