---
name: using-gdscript
description: Use when writing, reviewing, debugging, or refactoring GDScript in a Godot 4 project, including static typing and warnings, style and code order, signals, lambdas and `await`, exports and `@onready`, Resources versus nodes, errors without exceptions, Godot 3 or Python syntax that will not parse, per-frame performance, data layout and memory for simulations with thousands of agents or large chunked maps, threads, deterministic replays and save formats, and headless checks or GUT and gdUnit4 tests. It supplies version-gated GDScript defaults and the traps with how to prove each. Do not use it for C# in Godot, or for scene, project-setting or export work that changes no script.
---

# Use GDScript

Write statically typed Godot 4 GDScript for the engine version this project pins, and prove each change
by parsing and running it — a GDScript failure is usually a logged line in a process that still exits 0.

## Establish the version before writing code

`$GODOT` below is the engine binary: `command -v godot`, or wherever the project's rules say it lives.

```sh
"$GODOT" --version                              # the exact engine build
grep -E "config/features|gdscript/warnings" project.godot
ls addons/ 2>/dev/null                          # gut, gdUnit4, and what else ships
```

Your recall mixes Godot 3, early Godot 4 and Python; gate newer features on `config/features`:

| Since | Feature |
|---|---|
| 4.1 | `static var` |
| 4.2 | typed `for` variables (`for e: Enemy in enemies`) |
| 4.4 | `Dictionary[K, V]` |
| 4.5 | `@abstract`, variadic `...args`, `duplicate_deep()` |

Read [Syntax from elsewhere](references/syntax-from-elsewhere.md) whenever you are unsure a construct is
Godot 4 GDScript — before writing it, not after the parser objects.

A script's behaviour is split with the `.tscn` that sets its exported values, node paths and signal
connections: read both before changing either, because renaming one side breaks the other silently.

## Defaults and the failure each prevents

| Prefer | Avoid | Failure prevented |
|---|---|---|
| `var speed: float = 4.0`, `:=` only where the type is visible on the line, typed parameters and `-> void` | untyped `var`; `:=` on `get_node()`, `$Label` (infers `Node`) or a `Variant` | slower generic opcodes; errors found at runtime instead of parse time |
| `Array[Enemy]`, `Dictionary[StringName, int]` (4.4+), packed arrays for numbers | bare `Array` and `Dictionary` | wrong element types travelling silently |
| `if body is Enemy:` then use it | `body as Enemy` and carry on | `as` returns `null` on a failed object cast with no error |
| `signal health_changed(new_value: int)`; `health_changed.emit(hp)`; `sig.connect(_on_x)` | `emit_signal("...")`, `connect("sig", self, "m")`, `call`/`has_method` by name | typos that only fail at runtime, or never |
| Return an `Error` or a typed result; `push_error()` on a broken invariant | expecting an exception | GDScript has no `try`; an error aborts the current function and the game carries on |
| `assert(cond, "why")` with no side effects | `assert(_load_level())` | asserts are not evaluated in release exports, so the call disappears |
| Data in `RefCounted` or `Resource`; a `Node` only for something in the tree | a `Node` per data record; a bare `Object` | per-node processing cost; an `Object` leaks unless `free()`d |
| `class_name` plus `static func` for helpers | an autoload for stateless utilities | global mutable state and load-order coupling |
| Typed math (`clampf`, `absi`, `lerpf`), `is_equal_approx` for floats | `clamp`, `abs`, `==` on floats | `var x := clamp(...)` does not parse (`clamp` returns `Variant`); float comparisons that fail by one ulp |

Follow the project's style, or the official style guide where it has none. Two naming rules have
consequences beyond style: the file is the `class_name` in snake_case with acronyms as one word
(`YAMLParser` in `yaml_parser.gd`), and **`class_name`s are one flat namespace across the project and its
addons** — see the traps.

Read [Idioms](references/idioms.md) for the signal, coroutine, setter and resource traps with code.

## The traps, and how to prove each one

| Trap | What you see | The cause, and the proof |
|---|---|---|
| A runtime error in a callback | The feature does nothing; the process exits 0 | The function aborted after logging `SCRIPT ERROR`. Grep the whole log: `grep -n -e 'SCRIPT ERROR' -e 'ERROR:' run.log` |
| `--check-only` on a broken script | Exit 0 | It prints the parse error but does not fail the exit code on 4.7. Use the checker below, or grep its output |
| A `--script` run that hits an error | The process never exits | `quit()` was never reached; always pass `--quit-after` |
| A `class_name` "not declared" | Parse errors in files that are fine in the editor | The global class cache lives in the ignored `.godot/`. Run `--headless --import` on a clean checkout and after adding or moving a `class_name` file |
| Two scripts with the same `class_name` | Nothing at run time; one silently wins | Only reloading the script reports "hides a global script class" — the checker below catches it. Prefix by domain: `BuildingDef`, `ItemDef` |
| An autoload named like a `class_name` | Both fail to load, and every caller with them | "Class hides an autoload singleton". Keep the autoload name callers type; rename the class |
| A lambda reassigning a captured local | The outer variable never changes | Locals are captured by value at creation; mutate an Array, Dictionary or member instead |
| `await` on a signal of a node that is then freed | The coroutine never resumes, silently | Await only what is guaranteed to emit, or check `is_instance_valid` and use a timeout |
| A function containing `await` called without it | The caller runs on before the work finishes | Any `await` makes the function a coroutine; callers needing its result must `await` it |
| `await` inside `_ready` | The parent and the `ready` signal see the node before its setup finished | Keep `_ready` synchronous, or emit your own signal when done |
| `_init` or `_ready` overridden in a subclass | The parent's setup never runs | Neither chains, even with no arguments (observed on 4.7.2); only `_notification` runs on every level. Call `super()` |
| `var a: Array[int] = untyped_array`; `typed.map(...)` | An error, an empty array, or an untyped result | Typed and untyped arrays are distinct, and `map` returns an untyped `Array` (`filter` keeps the type). `typed.assign(untyped)` converts, and logs on a bad element |
| `5 / 2`; `-7 % 3` | `2`; `-1` | Integer division; `%` truncates toward zero — `posmod` and `floori` for grid coordinates |
| `"1" == 1`, or any `==` between mismatched types | `SCRIPT ERROR`, and the function aborts | Not `false`: a runtime error. Convert first, or `is_same()` |
| A shared `Resource` edited at runtime | Every instance changes together | Resources load once and are shared; `duplicate()` it or set `resource_local_to_scene` |
| `duplicate()` on nested data | Inner arrays still shared | It is shallow; `duplicate(true)`, or `duplicate_deep()` from 4.5 for resources inside |
| Two `RefCounted` objects referring to each other | Memory climbs; `leaked at exit` | Reference counting never frees a cycle — `building.residents` ↔ `citizen.home` is the usual one. Make one side a `WeakRef` or an id |
| `line.points[0] = p` on an engine property | Nothing changes, silently | The property returns a copy; read, modify, assign back |
| An exported member renamed | Scenes silently lose their saved value | Values are stored in the `.tscn` by name; grep the scenes and re-set them |
| Data read back from JSON | Lookups miss, `match` skips every branch, a `'5.0'` key error | Every number comes back a `float` and every key a `String`; `int()` at the load boundary |
| `randf`, `randi`, `shuffle`, `pick_random` in simulation code | A replay or a loaded save drifts | One global generator that anything can draw from; own a `RandomNumberGenerator` and save its `seed` and `state` |
| Enum values in a save or a `.tres` | Reordering the enum changes every saved value | Enums are plain ints; see [Determinism and saves](references/determinism-and-saves.md) |

## Simulation scale

A simulation with thousands of agents or a large map lives in packed arrays, not objects:

- **A grid is one flat packed array** indexed `y * width + x`: about 8 times faster than a `Dictionary`
  keyed by `Vector2i` (7 times on a neighbour sum), at 1–4 bytes a cell against 82.
- **Thousands of agents are columns** — one packed array per field — at 12 bytes an agent against about
  1,000 for a script `RefCounted`, and four times faster to update.
- **Every GDScript call costs about 40 ns in a release build**: inline the work in the loop the profiler
  names, batch signals per tick, and never `sort_custom` thousands of objects per tick (141 ms against
  4.8 ms for a packed-key sort).
- **`WorkerThreadPool.add_group_task` with `high_priority = true`, one task per chunk** — the default low
  priority stalled at 4 times on 16 cores.
- `PackedInt32Array`, `PackedFloat32Array` and `Vector2` are 32-bit while `int` and `float` are 64-bit:
  a counter wraps and a position loses precision far from the origin. Money and populations go in
  `PackedInt64Array` or plain `int`.

Read [Simulation scale](references/simulation-scale.md) before writing a grid, an agent list, a tick loop
or a chunked world, and [Determinism and saves](references/determinism-and-saves.md) before a replay, a
save format or anything seeded.

## Prove it

Warnings never reach a headless run, and errors rarely reach the exit code, so prove a change in three
steps:

```sh
"$GODOT" --headless --path . --import                                   # clean checkout, or new files
"$GODOT" --headless --path . --quit-after 600 --script <skill>/scripts/check_scripts.gd
"$GODOT" --headless --path . --log-file "$PWD/run.log" --quit-after 300  # then grep run.log for SCRIPT ERROR
```

`<skill>` is the directory this `SKILL.md` was loaded from; the checker prints
`GDSCRIPT CHECKED n FAILED m` and exits 1 on any failure. Then run the project's tests. Read
[Checking and testing](references/checking-and-testing.md) for what the checker covers, warnings as
errors, test runners, and a smoke run whose verdict line cannot pass by accident; read
[Typing and warnings](references/typing-and-warnings.md) before raising a warning to an error.

Report the engine version and the output that proves the change — the checker's verdict line, the test
run, or the log grep that came back empty — and for a visual result, exactly what the owner should look
at. [Sources](references/sources.md) holds the evidence behind each rule.
