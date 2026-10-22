# Checking and testing GDScript

## The three facts that shape every check

1. **A runtime error does not stop the process.** The failing function logs `SCRIPT ERROR` with a
   GDScript backtrace, returns its default, and the game carries on; a headless run then exits 0. In the
   editor the debugger pauses on it instead, which is why it looks loud there and silent in CI.
2. **`--check-only` and a failed `--script` load both exit 0** on 4.7. The parse error is in the output,
   not the exit code. `--check-only` also reports false errors for autoload names, and combined with
   `-d` it can wait at the debugger prompt forever.
3. **`class_name` lookups need the import cache.** `.godot/` is ignored and machine-local, so on a clean
   checkout every script that names another script's `class_name` fails to parse until
   `--headless --import` has run.

So a check is only real when it either sets the exit code itself or greps for a verdict line.

## Parse every script

```sh
"$GODOT" --headless --path . --import
"$GODOT" --headless --path . --script <skill>/scripts/check_scripts.gd
"$GODOT" --headless --path . --script <skill>/scripts/check_scripts.gd -- res://player res://ui
```

The checker reloads each `.gd` under the roots, prints `GDSCRIPT FAILED <path>` for each that does not
parse, ends with `GDSCRIPT CHECKED n FAILED m`, and exits 1 on any failure, a missing root, or when it
found nothing. It skips hidden directories and those holding `.gdignore`, and includes `res://addons`; pass
your own directories as roots when a third-party addon targets another engine version. It runs after the
autoloads are registered, so unlike `--check-only` it does not report autoload names as undeclared.
Warnings set to error in `project.godot` fail it too; warnings set to warn do not appear.

## Lint and format

Godot has no built-in formatter or linter. gdtoolkit supplies both, outside the engine:

```sh
pipx run --spec "gdtoolkit==4.*" gdlint path/        # or: uvx --from "gdtoolkit==4.*" gdlint path/
pipx run --spec "gdtoolkit==4.*" gdformat --check path/
```

Use them only where the project already does — `gdformat` rewrites every file it touches, and on a
project that never used it the diff is the whole codebase. Its naming rules match the official style
guide; `gdlint -d` prints the configuration, and a `gdlintrc` in the project overrides it.

## Run it with a verdict

```sh
"$GODOT" --headless --path . --log-file run.log --quit-after 300 -- --smoke
grep -nE "SCRIPT ERROR|^ERROR:" run.log && exit 1
grep -q '^SMOKE OK' run.log || exit 1
```

The game reads `OS.get_cmdline_user_args()`, asserts the things that prove it started — the scene built,
the first tick ran — and prints one verdict line only when they hold. A smoke check that only reads the
exit code passes on a game whose `_ready` errored.

A one-off experiment runs as a script extending `SceneTree`. Put the work in `_initialize`, where the
project's autoloads exist (in `_init` they do not), and let `quit(code)` set the exit code:

```gdscript
extends SceneTree

func _initialize() -> void:
	var inv := Inventory.new()
	inv.add(&"sword")
	print("count ", inv.count(&"sword"))
	quit(0 if inv.count(&"sword") == 1 else 1)
```

## Unit tests

The engine ships no GDScript test runner; `--test` runs the engine's own C++ tests. Use the one the
project has in `addons/`, at the version matching its engine.

**GUT** (9.x for Godot 4). Tests are scripts extending `GutTest` with `test_` methods:

```gdscript
extends GutTest

func test_damage_clamps_at_zero() -> void:
	var stats := Stats.new()
	stats.hp = 3
	stats.take(10)
	assert_eq(stats.hp, 0)
```

```sh
"$GODOT" --headless -d -s --path . addons/gut/gut_cmdln.gd -gdir=res://test -gexit
```

It exits 0 on pass and 1 on failure; `res://.gutconfig.json` holds the project's settings.

**gdUnit4** (`GdUnitTestSuite`, `assert_int(x).is_equal(0)`), run with its own wrapper so a parse error
does not hang the debugger:

```sh
addons/gdUnit4/runtest.sh --godot_binary "$GODOT" -a res://test
```

Before trusting a new test, break the code it covers and watch it fail; a test that never failed has not
shown it can.

## The language server

The editor runs a GDScript language server on port 6005 (`--lsp-port` changes it). It gives diagnostics
with warnings, which a headless check does not; it needs the editor running on the project.
