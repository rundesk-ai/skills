extends SceneTree
## Parses every GDScript file under the given roots and exits non-zero if any fails.
##
## Run from the project directory, after an import on a clean checkout:
##   godot --headless --path . --script <this file> [-- res://dir ...]
## Roots default to res://, addons included. Directories holding .gdignore, and hidden ones, are
## skipped, because the engine skips them too. The work runs in _initialize, not _init, because
## autoloads are registered by then and a script naming one would otherwise fail to parse.


func _initialize() -> void:
	var roots := OS.get_cmdline_user_args()
	if roots.is_empty():
		roots = PackedStringArray(["res://"])

	var checked := 0
	var failed := 0
	for dir in roots:
		if not DirAccess.dir_exists_absolute(dir):
			failed += 1
			printerr("GDSCRIPT ROOT MISSING ", dir)
			continue
		for path in _scripts(dir):
			checked += 1
			var script := load(path) as GDScript
			if script == null or script.reload(true) != OK:
				failed += 1
				printerr("GDSCRIPT FAILED ", path)

	print("GDSCRIPT CHECKED %d FAILED %d" % [checked, failed])
	quit(1 if failed > 0 or checked == 0 else 0)


func _scripts(dir: String) -> PackedStringArray:
	var found := PackedStringArray()
	if FileAccess.file_exists(dir.path_join(".gdignore")):
		return found
	for file in DirAccess.get_files_at(dir):
		if file.get_extension() == "gd":
			found.append(dir.path_join(file))
	for sub in DirAccess.get_directories_at(dir):
		if not sub.begins_with("."):
			found.append_array(_scripts(dir.path_join(sub)))
	return found
