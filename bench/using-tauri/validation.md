# Using Tauri validation

The current record for `using-tauri`; the method is `prompts/benchmark-skill.md`, and the latest result
is in `bench/results/using-tauri/`.

Fixtures are Tauri 2 apps (tauri 2.12, plugins fs and opener, Vite and TypeScript frontend without
`node_modules`). Defects were reproduced on the mock runtime before the rubrics were written:

- `notevault` (easy and complex): `export_all` is a synchronous command (about 200 ms per note) and so
  runs on the main thread; `read_note` read `/etc/hosts` through `../`; `run_hook` ran `echo pwned; id
  -un` from the page through `sh -c`; the `help` window's remote capability for
  `https://*.notevault.example` read a non-hidden file in the home directory through
  `fs:allow-read-text-file` with a `$HOME/**` scope; the main capability has read and write over
  `$HOME/**`; `csp` is `null` and `withGlobalTauri` is `true`.
- `notevault-acl` (medium): a `src-tauri/permissions/allow-export.toml` turns on the app ACL, so
  `list_notes` from the main window was refused while `export_all` from the `export` window was
  allowed; the new `settings` window is in no capability, so its fs read was denied.
- `tempconv` (routing near miss): a plain Rust CLI whose integer division gives 21.0C for 70f.

2026-10-24: see `bench/results/using-tauri/2026-10-24.json`.
