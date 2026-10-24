+++
skill = "using-tauri"
cases_version = 1
kind = "quality"
difficulty = "complex"
fixture = "notevault"
rubric = """
result.1  `run_hook`: removes or constrains the page-supplied shell command (`sh -c` from any script in the webview is arbitrary code execution); for example a fixed, user-configured command read in Rust, arguments passed without a shell, or the command removed — not only a frontend check.
result.2  `read_note`: rejects names that escape the notes directory (`../`, absolute paths, symlinks), validated in Rust by canonicalizing or by allowing only plain file names, with a test or a demonstrated refusal.
result.3  The `help` capability: the remote docs site (`https://*.notevault.example`) can read any non-hidden file in the home directory through `fs:allow-read-text-file` with a `$HOME/**` scope; removes the fs permission from the remote capability (or the remote access entirely).
result.4  The main capability's `$HOME/**` fs scope (with read and write) is narrowed to the app's own data directory, or justified.
result.5  Sets a real CSP in `tauri.conf.json` (not `null`), including `connect-src ipc: http://ipc.localhost` or noting IPC needs it, and addresses `withGlobalTauri: true` (turned off, since the frontend imports `@tauri-apps/api`).
result.6  Reports what was changed and what remains (e.g. app commands callable from every local window unless an app manifest restricts them; updater signing, code signing not set up), separating fixed from not fixed.
conduct.1 Runs `cargo check` in `src-tauri` after the changes and reports the result.
conduct.2 Proves at least one fix by exercising it (a mock-runtime test, a unit test of the path check, or a run), not only by reading the code.
"""
+++
We ship NoteVault 1.0 to customers next week. Do a security pass on the desktop app before then —
fix what you find, and tell me what you changed and what's still open.
