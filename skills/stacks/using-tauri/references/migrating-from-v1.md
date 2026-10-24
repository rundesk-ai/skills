# Moving from Tauri 1

Read this when the project is on Tauri 1, when moving it to Tauri 2, or when code or an answer may
come from Tauri 1 memory — most published examples and much of an agent's recall are Tauri 1.

## What no longer exists

| Tauri 1 | Tauri 2 |
|---|---|
| `tauri > allowlist` in `tauri.conf.json` | capabilities in `src-tauri/capabilities/*.json` and permissions |
| `tauri.conf.json > tauri`, `build.devPath`, `build.distDir` | `app` (`windows`, `security`, `withGlobalTauri`), top-level `bundle` and `identifier`, `build.devUrl`, `build.frontendDist` |
| `@tauri-apps/api/tauri` (`invoke`) | `@tauri-apps/api/core` |
| `fs`, `shell`, `dialog`, `http`, `clipboard`, `notification`, `updater`, ... in the core | plugins: a crate `tauri-plugin-x`, `.plugin(tauri_plugin_x::init())`, npm `@tauri-apps/plugin-x`, and a permission |
| `Window`, `get_window` | `WebviewWindow`, `get_webview_window` |
| `app.emit_all`, `listen_global` | `emit` (now reaches every listener) with `use tauri::Emitter`; `listen_any` |
| one `main.rs` | `lib.rs` holding `run()` with `#[cfg_attr(mobile, tauri::mobile_entry_point)]`, and a `main.rs` that calls it |

## Traps

- **A Tauri 1 config under Tauri 2** fails with `unknown field tauri, expected one of ...` and then
  advises running `cargo update`. The advice is wrong: the configuration is the problem.
- **`tauri migrate` is not the whole migration.** It needs a `Cargo.lock` (otherwise `failed to
  parse tauri version 1`). It upgrades the Rust crates, turns allowlist entries into plugins and a
  `capabilities/migrated.json`, and rewrites imports, but it left `@tauri-apps/api` and
  `@tauri-apps/cli` at `^1` — so the frontend fails with `TS2307: Cannot find module
  '@tauri-apps/api/core'` — and it created no `lib.rs`. Upgrade both npm packages to 2, split
  `lib.rs` out by hand, then read `migrated.json` and cut it down: it grants what the old allowlist
  granted, which is usually more than the app uses.
- **The compiler points at the renamed trait.** `emit` and `listen` need `use tauri::{Emitter,
  Listener}`, and `get_webview_window` needs `use tauri::Manager`; follow the hint rather than
  rewriting the call.
- **Windows users lose local data on upgrade.** Tauri 2 serves the app from
  `http://tauri.localhost` instead of `https://tauri.localhost` on Windows, a new origin, so
  `localStorage`, IndexedDB and cookies start empty. Set `app.windows[].useHttpsScheme: true` for an
  app upgraded from 1, or migrate the data on first launch.
- **Updates from a Tauri 1 install** need the updater's `createUpdaterArtifacts: "v1Compatible"`
  for the transition release.

## Prove the migration

`cargo check` in `src-tauri` (config schema and permissions), the frontend's type check, then run
the app and invoke one command of each kind — your own, a plugin's, and a window control — since
a missing permission rejects only at runtime.
