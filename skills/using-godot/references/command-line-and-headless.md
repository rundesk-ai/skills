# Command line, headless runs and captures

The command line is what makes a Godot game testable by something other than a person.

## The flags that matter

| Flag | Does |
|---|---|
| `--path <dir>` | Run the project in that directory. Always pass it |
| `--headless` | No window and no rendering device. Scripts run; there are no pixels to check |
| `--quit-after <n>` | Quit after n main-loop iterations (frames). Bounds any automated run |
| `--fixed-fps <n>` | Advance a fixed step per frame instead of wall-clock time, so runs repeat |
| `--import` | Start the editor, import, and quit |
| `--build-solutions` | C#: build. Implies `--editor`; add `--quit` or it never exits |
| `--editor` | Open the editor on the project |
| `--log-file <path>` | Also write the log to a file. Pass an absolute path: a relative one resolves against the project, and its directory must exist |
| `--verbose` | Engine-level detail, for a failure below your own code |
| `--write-movie <path>` | Capture frames. Needs a window: under `--headless` it crashes |
| `--script <file>` | Run a script extending `SceneTree` or `MainLoop` instead of the main scene |
| `-- <args>` | Everything after a bare `--` is for the game: `OS.get_cmdline_user_args()` |

```gdscript
var smoke := "--smoke" in OS.get_cmdline_user_args()
```

## Import and what to commit

Godot converts source assets into its own formats and caches them in `.godot/`, which is generated,
machine-specific and never committed. So a clean checkout has no import cache: a resource may load as
null, and a `class_name` may be "not declared", until `"$GODOT" --headless --path . --import` has run
once. Run it first in CI, and suspect it whenever something is null on a machine where the project has
never run.

What **is** committed: every `*.import` file next to its asset (it holds the import settings), every
`*.uid` file next to its script or shader (4.4+; references by UID break on the next clone without it),
and `export_presets.cfg` once it holds no secrets. Move or rename a file in the editor, or move its `.uid`
with it, so the UID follows the file.

## A smoke run with teeth

**The exit code alone proves nothing.** A script error is logged and the callback abandoned, and the
process still exits 0 — so a check that only tests the exit code passes on a game that never started
properly.

A smoke run that means something has three parts:

1. The game runs a bounded number of frames, headless, at a fixed step.
2. It asserts, in game, on things that must be true — the scene built, the simulation advanced, the
   expected nodes exist — and **prints a single verdict line**, then calls `get_tree().quit(0)`, or
   `quit(1)` on failure.
3. The script checks the exit code, the verdict line, and the absence of errors.

```sh
LOG="$PWD/smoke.log"
"$GODOT" --headless --path "$ROOT" --fixed-fps 60 --quit-after 600 --log-file "$LOG" -- --smoke \
  || { cat "$LOG" >&2; exit 1; }
grep -q '^SMOKE OK' "$LOG" || { echo "no verdict line" >&2; cat "$LOG" >&2; exit 1; }
! grep -n -e 'SCRIPT ERROR' -e 'ERROR:' -e 'Exception' "$LOG" || exit 1
```

`--quit-after` is the backstop for a game that never reaches its verdict. Keep the assertions about the
**harness** — that the game starts, ticks and builds — not about game rules. Rules belong in a suite
that needs no engine, and an assertion here about what a level contains will be deleted by the next
feature. A headless run has no pixels, so "it drew" is not checkable here; that is a capture's job.

## Captures

Given a `.png` path, `--write-movie` writes a numbered sequence; the last frame is
the screenshot. It forces `--fixed-fps`, so two captures of the same seed line up frame for frame.

```sh
"$GODOT" --path . --write-movie "$PWD/tmp/shot/frame.png" --quit-after 90
```

In a C# project, **build before capturing**: the engine runs the last built assembly, and a capture
taken without a build shows the old behaviour. Captures belong in an ignored directory; they are evidence
for one conversation, not an artifact.

## Exporting

Export presets live in `export_presets.cfg` and need export templates matching the engine version
exactly (the .NET templates for a C# project). In CI:

```sh
mkdir -p build/linux
"$GODOT" --headless --path . --export-release "Linux" "$PWD/build/linux/game.x86_64"
```

The target path names the file, and its directory must exist. Exporting is its own task with its own
verification; it is not part of an ordinary change.
