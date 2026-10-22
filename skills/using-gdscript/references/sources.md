# GDScript source basis

Checked against the Godot 4.7 documentation (`/en/stable/`, which serves 4.7) and the engine
source at `4.7-stable`. Claims marked *observed* were reproduced on Godot 4.7.2 stable, headless. Read
this when a claim is challenged or a new Godot release may have changed it; read `/en/<version>/` for the
version a project pins.

Shorthand: `GS` = `https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/`,
`BP` = `https://docs.godotengine.org/en/stable/tutorials/best_practices/`,
`ART` = `https://godotengine.org/article/`.

## Language and style

- `GS/gdscript_styleguide.html` — naming table, code order (17 groups, public before private), tabs,
  `and`/`or`/`not`, double quotes, lowercase hex, two blank lines, file name matches `class_name`, `:=`
  only when the type is on the line.
- `GS/gdscript_basics.html` — initialization order; lambdas capture locals by value at creation, shared
  content for Arrays, Dictionaries and objects (*observed*); variadic functions and `@abstract` "Since
  Godot 4.5" (*observed*); typed dictionaries since 4.4; `assert` not evaluated in release exports;
  `await` on signals and coroutines; `match` stricter than `==`; `&"..."` and `^"..."` literals; memory
  management (`RefCounted`, `Object.free`, `weakref`, `is_instance_valid`); integer division and `%`
  truncating toward zero (*observed*); packed arrays faster than typed, typed faster than untyped.
- `GS/static_typing.html` — typed code uses optimized opcodes; typed arrays and their untyped methods;
  typed `for` variables since 4.2; `as` returns null on a failed object cast (*observed*); safe lines;
  typed global functions.
- `GS/gdscript_exports.html` — exported values are not applied in `_init`; `@export_tool_button` needs
  `@tool` (4.4); exporting nodes.
- `GS/gdscript_documentation_comments.html` — `##` comments, `@tutorial`, `@deprecated`, `@experimental`.
- `GS/warning_system.html`, `https://docs.godotengine.org/en/stable/classes/class_projectsettings.html` —
  levels 0/1/2, `@warning_ignore`, `@warning_ignore_start`/`_restore` (4.4), `directory_rules` (4.6).
- `https://github.com/godotengine/godot/blob/4.7-stable/modules/gdscript/gdscript_warning.h` — the 4.7
  warning list and defaults: untyped and unsafe warnings off, `INFERENCE_ON_VARIANT` and
  `ONREADY_WITH_EXPORT` errors by default.
- `https://docs.godotengine.org/en/stable/classes/class_@gdscript.html` — annotations, `preload`,
  `assert` warning about side effects.
- `https://docs.godotengine.org/en/stable/classes/class_object.html` — duplicate `connect` is an error
  unless reference-counted; `CONNECT_ONE_SHOT`; `call`/`has_method` slower than direct calls.
- `https://docs.godotengine.org/en/stable/classes/class_array.html` — erasing while iterating is
  unsupported; `duplicate` is shallow; `assign`.
- `https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html` — resources load once and
  are shared; `_init` parameters need defaults.

## Best practices and performance

- `BP/scene_organization.html` — scenes without dependencies, parents respond to child signals, siblings
  through an ancestor. "Call down, signal up" is community wording for this, not the docs'.
- `BP/autoloads_versus_regular_nodes.html` — static functions on a `class_name` and `static var` (4.1)
  instead of an autoload for helpers.
- `BP/godot_interfaces.html` — node lookup cost, cached `@onready` or exported references fastest.
- `BP/logic_preferences.html` — preload into constants; set properties before `add_child`.
- `BP/node_alternatives.html` — `Object`, `RefCounted`, `Resource`.
- `https://docs.godotengine.org/en/stable/tutorials/performance/cpu_optimization.html` — profile first;
  node processing cost; engine calls run at native speed.
- `ART/gdscript-progress-report-typed-instructions/` — debug-build gains from typed code: 25–50% for
  operators and built-in calls, 120–150% for native method calls.
- `https://github.com/godotengine/godot/pull/70838` — about 30% on a release-build loop.

## Versions

- `ART/godot-4-1-is-here/` (static vars), `ART/godot-4-2-arrives-in-style/` (`UNTYPED_DECLARATION`, typed
  `for`, raw strings, `when`), `ART/dev-snapshot-godot-4-3-beta-1/` (`@export_storage`,
  `@export_custom`), `ART/dev-snapshot-godot-4-4-dev-2/` and `-dev-3/` and `-dev-7/` (typed dictionaries,
  tool buttons, warning regions), `ART/uid-changes-coming-to-godot-4-4/` (commit `.uid` files),
  `https://godotengine.org/releases/4.5/` (`@abstract`, variadic, `duplicate_deep`, release backtraces),
  `ART/dev-snapshot-godot-4-6-dev-2/` and `-dev-5/` (`MISSING_AWAIT`, `directory_rules`). No GDScript
  language changes were found for 4.7.

## Migration and other languages

- `https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.html` — what the
  converter misses: `tool`, string `connect`, part of `setget`; `File`/`Directory` replaced; `Time`;
  `super()` no longer implicit; automatic `randomize`.
- `https://github.com/godotengine/godot/blob/master/editor/project_upgrade/renames_map_3_to_4.cpp` — the
  rename table.
- `https://forum.godotengine.org/t/to-many-arguments-in-move-and-slide-godot-4-0-2/1604` — the
  `move_and_slide` argument error.
- godot-proposals #2972 (list comprehensions, not planned), #2135 and #2944 (unpacking, tuples, open),
  #11077 (keyword arguments, not planned), #4735 and #3194 (exceptions, none).

## Tooling and tests

- `https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html` — `--script`,
  `--check-only`, `--headless`, `--import`, `--quit-after`, `--lsp-port`, user args after `--`.
- godot issues #78587 and #111515 (`--check-only` false errors on autoloads), #117123 (`--check-only -d`
  loops in the debugger).
- `https://docs.godotengine.org/en/stable/tutorials/ui/creating_applications.html` — no integrated
  GDScript test framework; GUT and GdUnit4 named.
- `https://github.com/bitwes/Gut`, `https://gut.readthedocs.io/en/latest/Command-Line.html` — 9.x for
  Godot 4, `gut_cmdln.gd`, exit codes.
- `https://github.com/godot-gdunit-labs/gdUnit4` — `runtest.sh`, and why it passes `--remote-debug`.
- `https://github.com/Scony/godot-gdscript-toolkit` — gdlint and gdformat; no official formatter is
  merged (`https://github.com/godotengine/godot/pull/97383` open).
- `https://forum.godotengine.org/t/coroutines-hangs-on-tween-finished-if-tween-kill-is-called/131958` —
  a coroutine awaiting a signal that never fires is never resumed.

## Observed on 4.7.2, headless

- A runtime error logs `SCRIPT ERROR` with a backtrace, the function returns its default, execution
  continues, and the process exits 0.
- `--check-only --script` on a script with a parse error, and `--script` on one, both exit 0.
- Without `.godot/`, a script using another's `class_name` fails with "Identifier … not declared";
  after `--import` it parses.
- With `untyped_declaration=1`, a headless load prints nothing; at `2` it fails to parse.
- Awaiting a custom signal on a node that is then freed never resumes, with no message.
- `Array[int].assign()` with a bad element logs an error and leaves the array unchanged.
- Default argument values are fresh on each call.
- An inner class named like a global `class_name` is a parse error ("hides a global script class").
- A property initializer does not run its setter; a setter run before the node enters the tree sees
  `is_node_ready()` false.
- gdtoolkit 4.5.0 parses `@abstract`, variadic parameters and typed dictionaries.
- In a `--script` run, autoloads are not registered during `_init` but are by `_initialize`.
- `scripts/check_scripts.gd` exits 1 on a parse error, an unknown identifier, a missing import cache, a
  missing root and an empty root, and 0 on a clean project whose scripts name an autoload.
