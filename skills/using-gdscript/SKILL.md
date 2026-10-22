---
name: using-gdscript
description: Use when writing, reviewing, debugging, or refactoring GDScript in a Godot 4 project, including static typing and warnings, style and code order, signals, lambdas and `await`, exports and `@onready`, Resources versus nodes, errors without exceptions, Godot 3 or Python syntax that will not parse, per-frame performance, and headless checks or GUT and gdUnit4 tests. It supplies version-gated GDScript defaults and the traps with how to prove each. Do not use it for C# in Godot, or for scene, project-setting or export work that changes no script.
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

`config/features` names the version the project targets. Your recall of GDScript mixes Godot 3, early
Godot 4 and Python; code from the wrong one either fails to parse or, worse, parses and means something
else. Gate every newer feature on that version:

| Since | Feature |
|---|---|
| 4.1 | `static var`, `_static_init()` |
| 4.2 | typed `for` variables, `when` guards in `match`, raw strings `r"..."`, `UNTYPED_DECLARATION` |
| 4.3 | `@export_storage`, `@export_custom` |
| 4.4 | `Dictionary[K, V]`, `@export_tool_button`, `@warning_ignore_start`, `.uid` files |
| 4.5 | `@abstract`, variadic `...args`, `duplicate_deep()` |
| 4.6 | `MISSING_AWAIT` warning, `warnings/directory_rules` |

Read [Syntax from elsewhere](references/syntax-from-elsewhere.md) whenever you are unsure a construct is
Godot 4 GDScript — before writing it, not after the parser objects.

## Work in this order

1. **Read the script, its scene and its callers.** A script's behaviour is split with the `.tscn` that
   sets its exported values and node paths; renaming either side breaks the other silently.
2. **Match the project's style**, then the official order and naming below where it has none.
3. **Type everything you write.** See the defaults.
4. **Parse every changed script, then run the behaviour.** See [Prove it](#prove-it).

## Defaults and the failure each prevents

| Prefer | Avoid | Failure prevented |
|---|---|---|
| `var speed: float = 4.0`, `:=` only where the type is visible on the line, typed parameters and `-> void` | untyped `var`, `:=` on `get_node()` or a `Variant` | slower generic opcodes; errors found at runtime instead of parse time |
| `Array[Enemy]`, `Dictionary[StringName, int]` (4.4+), `PackedFloat32Array` for numbers | bare `Array` and `Dictionary` | wrong element types travelling silently |
| `if body is Enemy:` then use it | `body as Enemy` and carry on | `as` returns `null` on a failed object cast with no error |
| `@onready var _bar: ProgressBar = %HealthBar`, or `@export var bar: ProgressBar` | `get_node("../../UI/Bar")` in `_process`, or a path string in many places | a path that breaks when a node moves, and a lookup every frame |
| `signal health_changed(new_value: int)`; `health_changed.emit(hp)`; `sig.connect(_on_x)` | `emit_signal("...")`, `connect("sig", self, "m")`, `call`/`has_method` by name | typos that only fail at runtime, or never |
| Return an `Error` or a typed result; `push_error()` on a broken invariant | expecting an exception | GDScript has no `try`; an error aborts the current function and the game carries on |
| `assert(cond, "why")` with no side effects | `assert(_load_level())` | asserts are not evaluated in release exports, so the call disappears |
| `RefCounted` or `Resource` for data; a `Node` only for something in the tree | a `Node` per data record; a plain `Object` | per-node processing cost; an `Object` leaks unless freed |
| `class_name` plus static functions for helpers | an autoload for stateless utilities | global mutable state and load-order coupling |
| Typed math (`clampf`, `absi`, `lerpf`), `is_equal_approx` for floats | `clamp`, `abs`, `==` on floats | `Variant` results; float comparisons that fail by one ulp |

**Order and naming** (the official style guide): `@tool`/`@icon`, `class_name`, `extends`, `##` doc
comment, signals, enums, constants, static vars, `@export` vars, other vars, `@onready` vars,
`_static_init`, static methods, built-in virtuals (`_init`, `_enter_tree`, `_ready`, `_process`,
`_physics_process`, …), other overrides, then public before private methods, inner classes last. Files
`snake_case.gd` matching the `class_name`; classes and nodes `PascalCase`; functions, variables and
signals `snake_case`, signals in the past tense; constants and enum members `CONSTANT_CASE`; a leading
`_` for private members. Tabs, `and`/`or`/`not`, double quotes, two blank lines between functions.

Read [Idioms](references/idioms.md) for signals, lambdas, `await`, properties, exports, resources and
performance, with paired good and bad code.

## The traps, and how to prove each one

| Trap | What you see | The cause, and the proof |
|---|---|---|
| A runtime error in a callback | The feature does nothing; the process exits 0 | The function aborted after logging `SCRIPT ERROR`. Grep the whole log: `grep -n -e 'SCRIPT ERROR' -e 'ERROR:' run.log` |
| `--check-only` on a broken script | Exit 0 | It prints the parse error but does not fail the exit code on 4.7. Use the checker below, or grep its output |
| A `class_name` "not declared" on a clean checkout | Parse errors in files that are fine in the editor | The global class cache lives in the ignored `.godot/`. Run `--headless --import` once first |
| A lambda reassigning a captured local | The outer variable never changes | Locals are captured by value at creation; mutate an Array, Dictionary or member instead (`CONFUSABLE_CAPTURE_REASSIGNMENT`) |
| `await` on a signal of a node that is then freed | The coroutine never resumes, silently | Await only what is guaranteed to emit, or check `is_instance_valid` and use a timeout |
| A function containing `await` called without it | The caller runs on before the work finishes | Any `await` makes the function a coroutine; callers needing its result must `await` it |
| `var a: Array[int] = untyped_array` | An error and an empty or unchanged array | Typed and untyped arrays are distinct; `typed.assign(untyped)` converts, and logs on a bad element |
| `5 / 2` | `2` | Integer division; write `5 / 2.0` or `float(a) / b` (`INTEGER_DIVISION`) |
| `-7 % 3` | `-1` | `%` truncates toward zero; use `posmod`/`fposmod` |
| A shared `Resource` edited at runtime | Every instance changes together | Resources load once and are shared; `duplicate()` it or set `resource_local_to_scene` |
| `duplicate()` on nested data | Inner arrays still shared | It is shallow; `duplicate(true)`, or `duplicate_deep()` from 4.5 for resources inside |
| Erasing from an Array while iterating it | Skipped elements | Unsupported; iterate a copy, or build a new array with `filter` |
| An exported member renamed | Scenes silently lose their saved value | Values are stored in the `.tscn` by name; grep the scenes and re-set them |

## Prove it

Warnings never reach a headless run, and errors rarely reach the exit code, so prove a change in three
steps:

```sh
"$GODOT" --headless --path . --import                                   # once per clean checkout
"$GODOT" --headless --path . --script <skill>/scripts/check_scripts.gd   # every .gd parses; exits 1 if not
"$GODOT" --headless --path . --log-file run.log --quit-after 300         # then grep run.log for SCRIPT ERROR
```

`<skill>` is the directory this `SKILL.md` was loaded from. `scripts/check_scripts.gd` reloads every
script under `res://`, addons included, or under the roots passed after `--`, with the project's
autoloads registered, and prints `GDSCRIPT CHECKED n FAILED m`. Then run the project's tests. Read
[Checking and testing](references/checking-and-testing.md) for warnings as errors, gdtoolkit, GUT and
gdUnit4 commands, and a smoke run whose verdict line cannot pass by accident.

## Report

Name the script and function, the engine version, and the command whose output proves it: the checker's
verdict line, the test run, or the log grep that came back empty. A visual result is the owner's to
judge; say exactly what to look at.

## References

- [Idioms](references/idioms.md) — signals, lambdas, coroutines, properties, exports, resources versus
  nodes, errors, performance; good and bad pairs.
- [Typing and warnings](references/typing-and-warnings.md) — typed collections, casts, which warnings to
  raise to errors and how.
- [Syntax from elsewhere](references/syntax-from-elsewhere.md) — Godot 3 and Python constructs, and what
  replaces each.
- [Checking and testing](references/checking-and-testing.md) — headless checks, linters, test runners, CI.
- [Sources](references/sources.md) — the evidence behind each claim, and what was observed on the engine.
