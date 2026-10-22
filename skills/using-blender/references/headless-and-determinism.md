# Headless Blender and determinism

Read this before writing a script that must run in a build, or when a script that behaved in the
interface produces different or empty geometry in background mode.

The requirement is one sentence: **same inputs, same geometry, on another machine, next month.**

## The invocation, flag by flag

```sh
blender -b --factory-startup --python-exit-code 1 --python author-<asset>.py -- --arg value
```

| Flag | Why |
|---|---|
| `-b` | No window. Everything below follows from this. |
| `--factory-startup` | Ignores saved preferences, unit settings, enabled add-ons and the startup scene. Without it, a machine's local configuration becomes part of the geometry. |
| `--python-exit-code 1` | Blender exits **0 on an uncaught Python traceback**. Without this, a crashed script reports success. **It must precede `--python`**; after it, it is ignored. |
| `--python <file>` | Runs the script. Prefer a file over `--python-expr` so the run is reproducible from the repository. |
| `--` | Everything after it is ignored by Blender and left in `sys.argv` for the script. |

Reset inside the script as well, with `bpy.ops.wm.read_factory_settings(use_empty=True)`, so it is also
correct when someone runs it another way.

## Why operators misbehave headlessly

`bpy.ops` is a user-interface layer wearing a Python coat. Five separate mechanisms make it unreliable
in background mode:

1. **Context.** An operator resolves `window`, `screen`, `area`, `region` and `active_object` from the
   current context. In background mode most are `None`, so the call raises `RuntimeError: context is
   incorrect` — or worse, resolves against a different area than the one you meant.
2. **Poll.** Each operator has a `poll()` deciding whether it may run. A failed poll is not always an
   exception; some paths return `{'CANCELLED'}`, which reads in Python as a successful call.
3. **Selection state.** Operators act on the selection and the active object, both global mutable
   state. The minimum ceremony is: link the object into the collection, set
   `view_layer.objects.active`, then `select_set(True)`. Miss one line and the operator applies to
   whatever was selected last — a different mesh on the second iteration of a loop.
4. **Undo steps.** Every operator pushes one. A script building ten thousand pieces through operators
   grows an undo stack it never uses and slows to a crawl.
5. **Depsgraph re-evaluation.** Operators flush the dependency graph on each call. Correctness
   survives; throughput does not, and the flush hides ordering bugs that reappear the moment the same
   code is rewritten against the data API.

**The consequence:** a script built from operators works interactively and produces different or empty
geometry headlessly — the one failure nobody catches until the asset is already committed.

Where an operator is genuinely unavoidable, wrap it in `bpy.context.temp_override(...)`, give it the
objects explicitly, and say in a comment why no data-API path exists.

## Ordering hazards

Same seed and same script must produce the same geometry and manifests. Three things silently break that:

- **Iterating a Python `set` of bmesh elements or datablocks.** Set order follows pointer hashes, which
  change between runs. Sort first: `sorted({key[0] for key in keys})`, never a bare `for x in some_set`.
- **Unsorted filesystem walks.** `sorted(path.rglob('*'))`, or a manifest's source-hash block reorders
  on a different filesystem and the stored artifact churns with no semantic change.
- **Unsorted output collections.** Sort bindings by a declared key before writing them, or a partial
  re-run reorders the whole manifest.

**Seed from what is being drawn, not from when.** A seed built from stable indices —
`random.Random(base + species_index * 101 + variant * 17 + stage * 1009)` — is a pure function of the
thing, so regenerating one item reproduces exactly the geometry it had before. Never module-level
`random`, never wall time.

## Datablock name collisions

`bpy.data.<collection>.new(name)` never fails on a duplicate. It appends `.001`, `.002` and returns the
new datablock, and nothing warns you.

- A helper mesh created on every call accumulates names and memory unless the object **and** its data
  are removed afterwards. Deleting the object alone leaves the mesh datablock behind.
- A material created inside a loop becomes `Timber`, `Timber.001`, `Timber.002`. That is harmless where
  the consumer discards materials on import and each mesh has one slot. In a multi-slot kit it is not:
  importers commonly match slots **by name**, so a silently suffixed name becomes a mesh section with a
  null material.

Hold references rather than looking datablocks up by name after creating them.

## Depsgraph: evaluate before you read

`obj.evaluated_get(depsgraph)` returns geometry as of the last flush. Read it before the flush and you
get pre-modifier geometry, which usually looks plausible and is wrong. Call `depsgraph.update()` first;
`bpy.context.view_layer.update()` and `scene.frame_set()` also flush, which is why sampling a posed
position after a frame change is correct.

The same trap bites validation. Where the exporter evaluates modifiers itself, a degenerate-face
assertion reading `obj.data.polygons` directly is checking the **unevaluated** mesh. It passes while
the exported geometry is broken. **Assert against the mesh you actually export**: evaluate, then read.

## Where a connected Blender MCP fits

Use it to inspect a file, to look up the installed build's real API rather than recalling it, and to
render a preview for triage. **Nothing it produces is committed** — the script is the source, and an
asset that exists only because someone drove the interface cannot be rebuilt.
