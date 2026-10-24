# Command line, headless runs and captures

The command line is what makes a Godot game testable by something other than a person. These are the
flags with traps; `"$GODOT" --help` lists the rest.

| Flag | Trap |
|---|---|
| `--quit-after <n>` | Counts main-loop iterations, not seconds. Pass it to every automated run, `--script` runs included: an error before `quit()` leaves the process idling forever |
| `--fixed-fps <n>` | Without it, physics steps per frame vary with wall-clock time and runs do not repeat |
| `--log-file <path>` | A relative path resolves against the project, and its directory must exist; pass an absolute one |
| `--write-movie <path>` | Crashes under `--headless`: it needs a window |
| `--build-solutions` | Implies the editor and never exits without `--quit`; hides compiler errors — prefer `dotnet build` |
| `--script <file>` | Must extend `SceneTree` or `MainLoop`; not available in a release export |
| `-- <args>` | Everything after a bare `--` is the game's: `"--smoke" in OS.get_cmdline_user_args()` |

## Import and what to commit

`.godot/` is the generated import cache, machine-specific and never committed, so a clean checkout has
none: a resource loads as null and a `class_name` is "not declared" until
`"$GODOT" --headless --path . --import` has run. Run it first in CI, and again after adding an asset or a
`class_name` script.

Commit every `*.import` file beside its asset (its import settings), every `*.uid` beside its script,
scene or shader (4.4+), and `export_presets.cfg`; export credentials live in the ignored
`.godot/export_credentials.cfg`.

## A smoke run with teeth

**The exit code alone proves nothing**: a script error is logged, the callback abandoned, and the process
still exits 0. A smoke run that means something:

1. runs a bounded number of frames, headless, at a fixed step;
2. asserts in game what must be true — the scene built, the simulation advanced, the expected nodes
   exist — and **prints a single verdict line**, then `get_tree().quit(0)`, or `quit(1)` on failure;
3. is checked for the exit code, the verdict line, and the absence of errors.

```sh
LOG="$PWD/smoke.log"
"$GODOT" --headless --path "$ROOT" --fixed-fps 60 --quit-after 600 --log-file "$LOG" -- --smoke \
  || { cat "$LOG" >&2; exit 1; }
grep -q '^SMOKE OK' "$LOG" || { echo "no verdict line" >&2; cat "$LOG" >&2; exit 1; }
! grep -n -e 'SCRIPT ERROR' -e 'ERROR:' -e 'Exception' "$LOG" || exit 1
```

Assert that the game starts, ticks and builds — not game rules, which belong in a suite that needs no
engine. A run with `--editor` prints `leaked at exit` errors on quit that are not yours; exclude them in
that mode only. A performance budget can be asserted too: register the tick's duration with
`Performance.add_custom_monitor`, or time it with `Time.get_ticks_usec()`, and fail the verdict above it.

## Captures

Given a `.png` path, `--write-movie` writes a numbered sequence; the last frame is the screenshot. It
forces `--fixed-fps`, so two captures of the same seed line up frame for frame.

```sh
"$GODOT" --path . --write-movie "$PWD/tmp/shot/frame.png" --quit-after 90
```

## Exporting

Export templates must match the engine version exactly — the .NET templates for a C# project, which also
needs a solution file. The target's directory must exist:

```sh
mkdir -p build/linux
"$GODOT" --headless --path . --export-release "Linux" "$PWD/build/linux/game.x86_64"
"$GODOT" --headless --path . --export-pack "Linux" "$PWD/build/game.pck"   # just the data
"$GODOT" --headless --path . --main-pack "$PWD/build/game.pck" --quit-after 300   # run what ships
```

An export can exit 0 and still ship a broken game: wrong-case paths, a missing C# assembly, folders listed
with `DirAccess`. Running the exported pack is the only check that sees the player's filesystem — see
[Organization and naming](organization-and-naming.md).
