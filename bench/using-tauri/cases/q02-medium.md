+++
skill = "using-tauri"
cases_version = 1
kind = "quality"
difficulty = "medium"
fixture = "notevault-acl"
rubric = """
result.1  Finds why the main window broke: a file under `src-tauri/permissions/` turns on the app ACL, after which every app command needs an `allow-<command>` permission, so `list_notes`, `read_note` and the rest are refused in the main window.
result.2  Restores the main window without granting everything everywhere: grants the commands the main window uses to the main window's capability (per-command permissions, or `AppManifest::commands` with generated `allow-*`), and keeps `export_all` limited as intended, or explains a deliberate alternative.
result.3  Finds the second cause: the new `settings` window is listed in no capability, so its fs plugin call is denied. Adds a capability for `settings` with only what it needs.
result.4  Scopes the settings window's file access to the app's config directory (e.g. `$APPCONFIG/**` or the one file), not `$HOME/**` or an unscoped fs permission.
result.5  Does not widen the existing capabilities (for example by adding `settings` and `export` to the main capability with `$HOME/**`) to make the errors go away.
conduct.1 Runs `cargo check` in `src-tauri` (which regenerates and validates the ACL) and reports the result.
conduct.2 Shows evidence the commands are allowed per window: the generated `gen/schemas` files, a mock-runtime test, or a run of the app, rather than reasoning alone.
"""
+++
I added a permission file so only the new Export window can run the export, and now the whole app
is broken: every button in the main window fails with "Command list_notes not allowed by ACL" (and
the same for the others). The new Settings window also can't load settings.json — it says the
read isn't allowed. Fix both properly; I don't want to just open everything up.
