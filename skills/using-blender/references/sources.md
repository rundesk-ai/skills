# What these rules rest on

Use this file to audit a rule, not as more procedure.

## Blender's own documentation

The API moves between releases and this is the half that must be re-checked, not recalled:

- **Command-line arguments** — the manual's "Command Line" section defines `-b`,
  `--factory-startup`, `--python`, `--python-exit-code` and the `--` separator, and states the order
  rule that makes `--python-exit-code` effective only before `--python`.
  <https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html>
- **The Python API reference for the installed build** — `bpy.data`, `bpy.ops`, `bmesh`,
  `Mesh.from_pydata`, `Object.evaluated_get`, `Depsgraph.update` and `Context.temp_override`.
  <https://docs.blender.org/api/current/>
- **The 4.1 release notes** record the removal of `use_auto_smooth`, the auto-smooth angle and
  `calc_normals_split()`, and the move to the `sharp_face` and `sharp_edge` attributes. A script
  written before that release fails on any build after it.

Read the documentation for **the build that is installed**. The version is the first thing to confirm,
because a wrong-version answer looks like a mistake in your script.

## Formats

- **glTF 2.0** is right-handed, +Y up, in meters, and declares counter-clockwise front faces. The
  specification is the authority on what a reader may assume.
- **FBX carries axis metadata**, which is why the export flags and the import settings must agree, and
  why a calibration piece beats reasoning about them.

Neither format is byte-stable across runs: FBX embeds a timestamp and GUIDs, glTF a generator string.
That is a property of the writers, not a bug, and it is why a geometry digest is the change signal.

## Recorded practice

The determinism contract, the ordering hazards, the name-collision traps and the assertion list are
**practice recorded after each failure was met**, not measured results. Each states a mechanism you
can check yourself:

- A `set` of datablocks iterates in pointer-hash order, which changes between runs.
- `bpy.data.<collection>.new()` appends a numeric suffix on a duplicate name and returns the new
  datablock, silently.
- `evaluated_get()` returns geometry as of the last depsgraph flush.

What is **not** established here: any claim about a particular consumer's importer. Those belong to
the consumer's own skill, and its behavior must be proven by importing a calibration piece rather than
inferred from this page.

## Re-check when

- The installed Blender version changes — the API is the volatile part.
- The consumer changes its importer, its axis convention or its unit scale.
