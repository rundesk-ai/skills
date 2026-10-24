---
name: using-tauri
description: Use when building, reviewing, debugging, securing, upgrading or shipping a Tauri app — a web frontend with a Rust core in `src-tauri/`, `tauri.conf.json` or capability files — including commands and an `invoke` that rejects or never returns, adding windows, capabilities, permissions and plugin scopes, CSP and remote content, moving from Tauri 1 to 2, sidecars, bundling, code signing, the updater and mobile targets. It supplies Tauri 2 traps, secure defaults and the commands that prove a change. Do not use for Rust or frontend code that never crosses the Tauri bridge.
---

# Use Tauri

The webview is untrusted and the Rust core holds the authority. Everything the page can reach is
declared — commands, capabilities, scopes, CSP — and most mistakes in those declarations compile
cleanly and fail only at runtime, as a rejected `invoke` promise the frontend may swallow. Prove a
change by building it and invoking it, not by reading it.

## Establish the version before changing code

```sh
npx tauri info                      # tauri, tauri-build, @tauri-apps/api and CLI versions; CSP; plugins
grep -E '^tauri|tauri-build|tauri-plugin' src-tauri/Cargo.toml
ls src-tauri/capabilities src-tauri/permissions 2>/dev/null
```

`[tauri] 1.x`, an `allowlist` in `tauri.conf.json`, or `@tauri-apps/api/tauri` imports mean Tauri
1: the config schema, the JavaScript module paths, the event API and the whole security model
differ, so read [Moving from Tauri 1](references/migrating-from-v1.md) before writing anything. A
plugin's Rust crate and npm package must agree on major and minor version; `tauri info` lists both.

## The traps, and how to prove each one

| Trap | What you see | The proof |
|---|---|---|
| A **synchronous command** doing slow work | The window freezes: 0 animation frames during a 1 s command, and a second `invoke` waits for it | Sync commands run on the main thread. Make it `async fn`, or `#[tauri::command(async)]`, and measure a concurrent invoke |
| An error type that is not `Serialize` (`anyhow::Error`, `std::io::Error`) | `the method blocking_kind exists ... Into<InvokeError>` at `generate_handler!` | Return your own error enum with a `Serialize` impl that writes its `Display` — see [Commands and IPC](references/commands-and-ipc.md) |
| An argument key in snake_case from JavaScript | `invalid args filePath ... missing required key filePath` | Rust `file_path` is `filePath` in `invoke`. Rename on one side, or `#[tauri::command(rename_all = "snake_case")]` |
| An `async` command taking `&str` or `State` with a plain return | `async commands that contain references as inputs must return a Result` | Return `Result<T, E>`, or take owned arguments |
| A command not in `generate_handler!`, or a second `invoke_handler` call | `Command x not found` at runtime only | Only the last `invoke_handler` counts: register every command in one list |
| `manage(T)` but `State<'_, Mutex<T>>` (or the reverse) | The invoke rejects: `state not managed for field state on command x` | The managed type and the requested type must match exactly; invoke it once |
| Any file under `src-tauri/permissions/` | Every app command rejects: `Command x not allowed by ACL` | One file there switches app commands to deny-by-default. `tauri permission new` writes there. Grant `allow-<cmd>` in a capability for each command, or delete the directory; `__app-acl__` in `src-tauri/gen/schemas/acl-manifests.json` shows it is on |
| A capability's `windows` list assumed to restrict your commands | A second window calls a privileged command | Plain registered commands are callable from every local window. Gate them with `AppManifest::commands` in `build.rs` and per-command permissions — see [Security](references/security.md) |
| A plugin added to `Cargo.toml` only | `plugin x not found` at runtime | A plugin needs four parts: the crate, `.plugin(init())`, the npm package and a permission in a capability. `tauri add <plugin>` does all four, but also ran `cargo fmt` over the crate and reformatted the JSON config; commit first |
| A new window whose label no capability lists | Your own commands work from it; every plugin call is denied | Add the label to a capability's `windows` (or a new capability) with only what that window needs |
| A window built inside a synchronous command or event handler | The `invoke` never returns on Windows (a deadlock) | Create windows from an `async` command |
| Widening the `fs` scope so the page can open a file the user picked | Every page script can now read that whole tree | Let the user choose with the dialog plugin, which grants the picked path for the session only |
| A plugin permission misspelled | The build fails and suggests the right name | Read the suggestion; `tauri permission ls <plugin>` lists what each set grants. `core:default` does not include window controls such as `core:window:allow-close` |
| Bytes sent as `Vec<u8>` or `Array.from` | 10 MiB took 97 ms out and 544 ms in, as a JSON number array | Raw `Response`, raw request bodies and `Channel` — see [Commands and IPC](references/commands-and-ipc.md) |
| A CSP without `connect-src ipc: http://ipc.localhost` | IPC still works, but raw bytes arrive as a JS `Array`, 30 times slower | Tauri falls back to `postMessage`; add both sources and check the response is an `ArrayBuffer` |
| The scaffold's `"csp": null` and `"withGlobalTauri": true` shipped | Any injected script can call every allowed command | Set a CSP and turn the global off before release — see [Security](references/security.md) |
| Sidecar file named without the target triple | `resource path binaries/helper-aarch64-apple-darwin doesn't exist` | Name the file `<name>-$(rustc --print host-tuple)`; the bundle drops the suffix — see [Shipping](references/shipping.md) |
| Updater signing key lost, or set as a relative path | Installed apps can never update again; or `Invalid symbol 46` after a full bundle | Back up the private key outside the repository; give `TAURI_SIGNING_PRIVATE_KEY` the key or an absolute path |

## Validate in Rust, never in the page

A command is a public endpoint that any script in the webview can call with any arguments. A
capability decides *whether* a window may call it, never *what* it may pass. Check every path,
URL, size and identifier inside the command: canonicalize a path and require it under an allowed
base, cap lengths before allocating, refuse URL schemes you did not expect. Plugin scopes (`fs`,
`opener`, `shell`) do not protect your own commands' file access.

Release builds have no devtools (and on Windows no console): add the log plugin to see what failed
in a shipped build, and never ship the `devtools` feature, whose private macOS APIs the App Store
rejects.

## Prove it from the command line

```sh
(cd src-tauri && cargo check)       # also validates config schema, permission names, sidecar paths, Cargo features
(cd src-tauri && cargo test)        # command tests on the mock runtime: see references/commands-and-ipc.md
npx tauri build --debug --bundles app   # fastest real bundle (macOS; deb/appimage or nsis elsewhere)
```

`src-tauri/gen/schemas/capabilities.json` shows the capabilities that were compiled in. A command's
runtime failures — unregistered, denied, wrong state — surface only by invoking it: run the app, or
the mock-runtime test, and read the rejection.

## Read only what the task needs

- Writing or changing a command, state, events, channels, binary payloads, or testing commands:
  [Commands and IPC](references/commands-and-ipc.md).
- Capabilities, permissions, scopes, CSP, remote URLs, the asset protocol, the isolation pattern:
  [Security](references/security.md).
- A Tauri 1 project, or code or answers written from Tauri 1 memory:
  [Moving from Tauri 1](references/migrating-from-v1.md).
- Webview differences per platform, sidecars, resources, bundle size, signing, notarization, the
  updater, mobile targets: [Shipping](references/shipping.md).
- Auditing a claim here: [Sources](references/sources.md).

## Report

Name the command or capability changed and the run that proves it: an `invoke` that returned or
was refused, not a build that merely compiled.
