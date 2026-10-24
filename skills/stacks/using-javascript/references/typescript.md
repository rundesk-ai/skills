# TypeScript

Read this when the project has a `tsconfig.json` or `.ts` files. It covers where types and the runtime
part ways; component typing belongs with the component framework.

## Check the compiler version first

`ls node_modules/.bin/tsc && npm exec --no -- tsc -v`. TypeScript 6 changed defaults that older advice
assumes: `strict` is on when the tsconfig does not set it, and `tsc file.ts` refuses to run when a
tsconfig is present (TS5112; `--ignoreConfig` overrides). `moduleResolution: node10` is deprecated in 6
and removed in 7, the native compiler. Upgrading a project that relied on the old default can surface
hundreds of errors at once; set `"strict": false` explicitly to defer them, or fix them. A check run with
the wrong compiler (a global 5.x against a project on 7) reports a different set of errors, or none.

## Types are erased

These compile under the strictest settings and fail in production:

```ts
interface User { id: number; name: string; tags: string[] }
const user = JSON.parse('{"id":"7","name":null}') as User;
user.id + 1;          // "71"
user.tags.length;     // TypeError: Cannot read properties of undefined
```

`JSON.parse`, `response.json()`, environment variables, `localStorage` and message events return data the
compiler has never seen. Validate it where it enters, with the schema validator the project already uses
or a type guard (`function isUser(v: unknown): v is User`) that checks every field. In a review, treat
each `as`, `any` and non-null `!` as an unchecked claim that needs a reason.

## Options that change what the compiler catches

| Option | Catches | Without it |
|---|---|---|
| `noUncheckedIndexedAccess` | `arr[i]` and `record[key]` typed as possibly `undefined` | `const first: number = list[10]` type-checks and is `undefined` |
| `exactOptionalPropertyTypes` | assigning `undefined` to an optional property explicitly | `{ retries: undefined }` passes as "not set", and `'retries' in opts` is true |
| `useUnknownInCatchVariables` (in `strict`) | `catch (e)` typed `unknown`, so you must narrow it | `e.message` on a thrown string is `undefined` in the log, and a thrown `null` crashes the handler |
| `verbatimModuleSyntax` | a type imported without `import type` | the import survives type stripping and fails at load |
| `erasableSyntaxOnly` | `enum`, parameter properties, value namespaces | Node's type stripping refuses the file at load |

Turn on `noUncheckedIndexedAccess` for new code; it reported exactly the line that crashed in the example
above. `skipLibCheck` hides errors inside declaration files, and declarations from `@types` can disagree
with the installed library's version.

## Module settings must match the runtime

The compiler resolves imports by `module` and `moduleResolution`; if those do not describe how the code
actually runs, the type check passes and the program fails to start.

- Code that Node runs directly, without a bundler: `"module": "nodenext"`. Relative imports then need
  their extension, and the compiler reports a missing one (TS2835). Write `./helper.js`, or `./helper.ts`
  with `rewriteRelativeImportExtensions` when `tsc` emits the JavaScript.
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

## Prove the check covered the code

Use the project form, `tsc --noEmit -p .` or the project's own typecheck script; on TypeScript 5 the
single-file form ignores the tsconfig and checks with default options. A root tsconfig with
`"files": []` and `references` (a solution file) makes `tsc --noEmit -p .` check zero files and exit 0
on a broken project: use `tsc -b`, and confirm the file count with `tsc -p . --listFilesOnly | wc -l`.
