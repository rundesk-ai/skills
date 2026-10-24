# TypeScript

Read this when the project has a `tsconfig.json` or `.ts` files. It covers where types and the runtime
part ways; component typing belongs with the component framework.

## Check the compiler version first

`npm exec --no -- tsc -v`. TypeScript 7, the native compiler, is the current release and changed defaults:
`strict` is on when the tsconfig does not set it, `moduleResolution: node10` is removed, and
`tsc file.ts` refuses to run when a tsconfig is present (TS5112). Upgrading a project that relied on the
old default can surface hundreds of errors at once; set `"strict": false` explicitly to defer them, or fix
them. A check run with the wrong compiler (a global 5.x against a project on 7) reports a different set of
errors, or none.

## Types are erased

Nothing in a type survives to run time, so these compile under the strictest settings and fail in
production:

```ts
interface User { id: number; name: string; tags: string[] }
const user = JSON.parse('{"id":"7","name":null}') as User;
user.id + 1;          // "71"
user.tags.length;     // TypeError: Cannot read properties of undefined
```

`JSON.parse`, `response.json()`, environment variables, `localStorage` and message events return data the
compiler has never seen. `as`, `any` and the non-null `!` are claims the compiler takes on trust. Validate
at the boundary, with a schema validator the project already uses or a type guard:

```ts
function isUser(value: unknown): value is User {
  if (typeof value !== 'object' || value === null) return false;
  const v = value as Record<string, unknown>;
  return typeof v.id === 'number' && typeof v.name === 'string'
    && Array.isArray(v.tags) && v.tags.every((t) => typeof t === 'string');
}
```

Treat each `as`, `any` and `!` in a review as an unchecked claim that needs a reason.

## Options that change what the compiler catches

| Option | Catches | Without it |
|---|---|---|
| `strict` | implicit `any`, possibly-`null` access, unchecked `this` | most of the type system is advisory |
| `noUncheckedIndexedAccess` | `arr[i]` and `record[key]` typed as possibly `undefined` | `const first: number = list[10]` type-checks and is `undefined` |
| `exactOptionalPropertyTypes` | assigning `undefined` to an optional property explicitly | `{ retries: undefined }` passes as "not set", and `'retries' in opts` is true |
| `useUnknownInCatchVariables` (in `strict`) | `catch (e)` typed `unknown` | `e.message` on a thrown string crashes |
| `verbatimModuleSyntax` | a type imported without `import type` | the import survives type stripping and fails at load |
| `erasableSyntaxOnly` | `enum`, parameter properties, value namespaces | Node's type stripping refuses the file at load |

Turn on `noUncheckedIndexedAccess` for new code; it reported exactly the lines that crashed in the
example above. `skipLibCheck` hides errors inside declaration files, and declarations from `@types` can
disagree with the installed library's version.

## Module settings must match the runtime

The compiler resolves imports by `module` and `moduleResolution`; if those do not describe how the code
actually runs, the type check passes and the program fails to start.

- Code that Node runs directly, without a bundler: `"module": "nodenext"`. Relative imports then need
  their extension (`./helper.js`, or `./helper.ts` with `allowImportingTsExtensions`), and the compiler
  reports a missing one (TS2835).
- `"moduleResolution": "bundler"` accepts extensionless imports that only a bundler can resolve. With it,
  `tsc` passed and `node dist/main.js` failed with `ERR_MODULE_NOT_FOUND`. Use it only when a bundler
  really builds the code.
- `"module": "commonjs"` output in a `"type": "module"` package fails with `exports is not defined in ES
  module scope`.

## Running TypeScript is not checking it

Node runs `.ts` files by stripping the types, and so do most bundlers and runners: a file with type errors
runs. Type stripping also ignores `tsconfig.json` (no path aliases), refuses `.ts` files under
`node_modules`, needs explicit `.ts` extensions, and rejects syntax that is not erasable: `enum`,
parameter properties (`constructor(private x: number)`), and namespaces with values. Use a union of
literals or an `as const` object instead of an enum.

Prove a change type-checks separately from running it:

```sh
npm exec --no -- tsc --noEmit -p .   # or the project's own typecheck script
```

Use the project form. On TypeScript 5, `tsc --noEmit src/file.ts` ignores the tsconfig, so it checks with
default options and can pass while the project form fails; on 7 it refuses to run.

## What the compiler never checks

The run-time shape of any input; whether an index or key exists unless `noUncheckedIndexedAccess` is on;
whether an import resolves under the runtime's rules, unless the module settings match it; which
exceptions a function throws; and whether a declaration file describes the installed version of its
library.
