# Organization and naming

Names in Godot are lookups: a path, a class name, a node name, a group or an action is a string resolved
at run time, and most of the failures below are silent. Observed on Godot 4.7.2 unless marked.

## Paths that work in the editor and fail in the export

- **Case.** On macOS and Windows, `load("res://Art/Tree.png")` finds `art/tree.png`; inside the exported
  pack it returns `null`, and a wrong-case `preload` makes the whole script fail to parse — so a main
  scene's script never runs. The export itself warns about nothing and exits 0. From 4.4 a run from the
  project prints `Case mismatch … will not open when exported`: treat every hit as an error
  (`grep -n 'Case mismatch' run.log`). Name every file and folder lowercase `snake_case` — C# scripts
  excepted — and write each path exactly as stored.
- **Listing a folder.** In an export, `DirAccess.get_files_at("res://data")` returns `.remap`, `.import`
  and `.gdc` names and no `.png` at all, so a registry built from "every `.tres` in a folder" is empty in
  the shipped game. Use `ResourceLoader.list_directory()` (4.4+), or an explicit list resource.
- **`res://` is read-only in an export.** Saves, caches and generated files go to `user://`.
- **`.gdignore`** keeps a folder out of import and out of the export — but a text `.tres` inside one
  still loads from a project run, so nothing the game loads may live there.
- **Prove it with the pack**: `--export-pack` a preset and run the game with `--main-pack`; it is the
  filesystem the player gets.

## Moving and renaming files outside the editor

The editor's FileSystem dock moves a file and its references together. A terminal, an IDE refactor or
`git mv` does not:

| Moved | Scene reference | `preload("res://old/path.gd")` |
|---|---|---|
| with its `.uid`, before `--import` | not resolved yet | parse error |
| with its `.uid`, after `--import` | works | parse error |
| **without** its `.uid` | **the node loads with no script**, logged once | parse error |

A scene that lost its script still loads, and the failure surfaces later as a missing method. After any
move: carry the `.uid`, run `--headless --import`, grep for the old path in `.gd`, `.cs`, `.tscn` and
`.tres` files — UIDs do not cover `preload`, `load`, `change_scene_to_file` or paths in data files — and
load each scene that referenced it.

## Names that must be unique

- **`class_name`s are one flat namespace**, addons included. Two scripts with the same name report
  nothing at run time and one silently wins. Prefix by domain: `BuildingDef`, `ItemDef`.
- **An autoload named like a `class_name`** fails both, with every caller ("hides an autoload
  singleton"). Keep the autoload name callers use; rename the class.
- **C# `[GlobalClass]` names ignore the namespace**: two `ItemDef`s in different namespaces build and run,
  and one vanishes from the global class list and the inspector.
- **A C# file is named exactly like its class.** A mismatch — including a `snake_case.cs` file — builds
  without a diagnostic and fails only when the script is instantiated.
- **Do not name your own C# types after engine or framework types** (`Timer`, `Range`, `Node`,
  `Resource`). In another namespace that imports `Godot` it is an ambiguity error; inside your own
  namespace `new Timer()` silently builds yours where a reader expects the engine's.

## Names looked up as strings

- **Members you declare in C# keep their C# name.** Engine members are found by snake_case
  (`"add_child"`), but `call_group("guards", "enter_alert_mode")` silently skips a C#
  `EnterAlertMode()` — and from GDScript, `has_method`, `has_signal` and `get` need the PascalCase name.
  In C#, use the generated `MethodName`, `SignalName` and `PropertyName`; in a mixed-language group,
  every implementation shares one exact method name.
- **Do not find spawned nodes by name.** A node added with the name of one freed earlier in the same frame
  is renamed `@Node@2` for good, and the name setter replaces `. : @ / " %` with `_` — `"farm:3"` is not
  the name you will look up. Keep a dictionary from entity id to node.
- **`%Unique` names find only nodes the same scene owns.** A node added from code is found only once its
  `owner` is the scene root.
- **Groups and input actions are strings with no checking**: `get_nodes_in_group("guard")` for
  `"guards"` is an empty array. Declare each once — constants on a `class_name`, or `static readonly
  StringName` in C# — and use that.
- Editor-made handlers are named `_on_<node>_<signal>`; renaming the node does not rename the handler or
  the `[connection]` line in the `.tscn`.

## Organizing a game's systems

- **Group files by feature, with assets beside the scene that uses them**
  (`buildings/farm/farm.tscn`, `farm.gd`, `farm.png`, `farm_def.tres`), and third-party code in `addons/`.
  A tree sorted by type (`scripts/`, `textures/`, `scenes/`) scatters one feature across folders and makes
  every move touch all of them.
- **A scene needs nothing from its surroundings.** Its parent gives it references, data or callables and
  listens to its signals; a signal reports what happened (`building_placed`) and does not start behaviour.
  A scene that reaches up the tree cannot be instanced anywhere else, or tested alone.
- **Autoload only a system that owns its own data, must be global, and stands alone.** A system that edits
  other systems' data is a node or a plain class instead. A signals-only "event bus" autoload is community
  practice for the one or two events that cross unrelated scenes; used for local wiring, it makes every
  event a search of the whole project.
- **Definitions are custom Resources** (`class_name BuildingDef extends Resource`, or a C#
  `[GlobalClass]` with a parameterless constructor), one `.tres` per definition; runtime state never goes
  on a definition, which is shared.
- **Simulation state lives in plain objects or arrays, with nodes as views.** Component nodes
  (`HealthComponent`) are community practice for a handful of entities; Godot's own design notes say its
  nodes "do not work like components", and each one is a node with a node's cost and lifetime — so at
  thousands of entities, components are columns in the data layer.
- **Groups for rare queries and events across scenes; your own registry for anything per tick.**
  `get_nodes_in_group` builds a new array every call, and `find_child` walks every descendant.
