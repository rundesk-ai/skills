# Tauri source basis

Behaviour marked *observed* was reproduced in October 2026 on macOS (arm64) with tauri 2.12.5,
tauri-build 2.7.4, wry 0.57.1, `@tauri-apps/cli` and `@tauri-apps/api` 2.12.4, rustc 1.91.1 and
Node 25, in a project made by `create-tauri-app` 4.7.5 (vanilla TypeScript), through the mock
runtime and through release builds that reported back to stdout. Windows, Linux, iOS and Android
were not run; claims about them rest on the documentation cited. Read this when a claim in the
skill is challenged or a new Tauri release may have changed it.

## Why Tauri is its own skill

Its work starts from `src-tauri/`, `tauri.conf.json` and capability files, and its decisions — what
the webview may call, how the capability ACL is compiled, the system webview per platform, the
updater's signing — do not arise in plain Rust or plain web work, nor in Electron, which bundles
Chromium and a Node main process and has a different security model, packaging and update path.

## Commands and IPC

- [Calling Rust from the frontend](https://v2.tauri.app/develop/calling-rust/): commands, argument
  casing, async commands, errors, state, channels, raw requests and responses. Observed: a sync
  command runs on the thread named `main` (0 animation frames and a 965 ms wait for a concurrent
  invoke during 1 s of work); `async fn` and `#[tauri::command(async)]` run on `tokio-rt-worker`
  (1 ms); the `anyhow::Error` compile error; `missing required key filePath`; `async commands that
  contain references as inputs must return a Result`; `Command nope not found`; `state not managed
  for field state on command counter`; `plugin opener not found`. Observed: a second
  `invoke_handler` call replaced the first (`Command greet not found`); a struct argument's fields
  were read as written (`missing field file_path` for `filePath`); an `async` command taking
  `State` with a plain return failed to compile with the same reference error.
- Binary payloads, observed with `performance.now()` around `invoke` for 10 MiB: 97 ms for a
  `Vec<u8>`, 5 ms for `ipc::Response`, 13 ms through a `Channel<Response>` in 64 KiB chunks, 544 ms
  for `Array.from` into `Vec<u8>`, 2 ms for a raw `Uint8Array` read through `Request::body()`.
- [Mock runtime](https://docs.rs/tauri/latest/tauri/test/index.html): observed with
  `generate_context!(test = true)` and `get_ipc_response`; a second plain `generate_context!()`
  failed with a duplicate `_EMBED_INFO_PLIST` symbol.
- [WebDriver testing](https://v2.tauri.app/develop/tests/webdriver/): `tauri-driver` supports
  Windows and Linux.

## Security

- [Capabilities](https://v2.tauri.app/security/capabilities/) and
  [permissions](https://v2.tauri.app/security/permissions/): registered app commands are allowed for
  all windows unless an app manifest makes them permissioned; iframes are indistinguishable from
  the window on Linux and Android. Observed: a window outside every capability called an app
  command but was denied a plugin command; with `AppManifest::commands` the unlisted command was
  refused; one file under `src-tauri/permissions/` (written by `tauri permission new`) set
  `__app-acl__` and every command failed with `not allowed by ACL`; `remote.urls`
  `https://*.app.example` allowed `www.app.example` and denied `app.example`; `core:default` denied
  `window.close`; misspelled permissions failed the build with a suggestion.
- [Content Security Policy](https://v2.tauri.app/security/csp/): observed that the scaffold ships
  `"csp": null` and `withGlobalTauri: true`; that a `default-src 'self'` policy gained `sha256`
  hashes for inline scripts in the response header; and that without
  `connect-src ipc: http://ipc.localhost` a raw response arrived as an `Array` in 175 ms instead of
  an `ArrayBuffer` in 6 ms.
- [Asset protocol scope](https://v2.tauri.app/security/asset-protocol/) and plugin scopes
  (dot-files and `requireLiteralLeadingDot`). Observed: enabling the asset protocol without the
  `protocol-asset` feature failed `cargo check`; `opener:default` refused `file:///etc/passwd`.
- [Isolation pattern](https://v2.tauri.app/concept/inter-process-communication/isolation/): ES
  modules unsupported in the isolation application.

## Migration

- [Upgrade from Tauri 1.0](https://v2.tauri.app/start/migrate/from-tauri-1/): renamed config keys,
  plugins, `api/core`, `Emitter`/`Listener`, `get_webview_window`, `listen_any`, the Windows origin
  change and `useHttpsScheme`, `v1Compatible` updater artifacts. Observed on a Tauri 1 project:
  the misleading `unknown field tauri` error; `tauri migrate` failing without `Cargo.lock`, then
  leaving the npm packages at `^1` (TS2307) and creating no `lib.rs`.

## Shipping

- [Webview versions](https://v2.tauri.app/reference/webview-versions/) and
  [Linux graphics debugging](https://v2.tauri.app/develop/debug/linux-graphics/).
- [Sidecars](https://v2.tauri.app/develop/sidecar/): observed the target-triple error and the
  suffix dropped in the bundle.
- [macOS signing](https://v2.tauri.app/distribute/sign/macos/) and
  [Windows signing](https://v2.tauri.app/distribute/sign/windows/); Gatekeeper checks with `spctl`
  and `stapler` from the [Apple developer forums](https://developer.apple.com/forums/thread/770443).
  Observed: an unconfigured build is ad-hoc signed.
- [Updater plugin](https://v2.tauri.app/plugin/updater/): the key cannot be recovered, `.env` is not
  read, the manifest takes the `.sig` content. Observed: `plugins > updater doesn't exist`; a
  missing key failing after bundling; `Invalid symbol 46` for a relative key path.
- [App size](https://v2.tauri.app/concept/size/). Observed: release `.app` 4.08 MiB and `.dmg`
  1.88 MiB, debug `.app` 24.13 MiB; physical footprint from `footprint` 29 MB for the app, 21 MB
  WebContent, 20 MB GPU, 6 MB networking; launch to first invoke 502 ms cold, 261–278 ms after.
- Observed: `tauri android init` failing without `ANDROID_HOME` and `NDK_HOME`, leaving the project
  unchanged. iOS was not run.

## Added after an independent review (read in the tauri 2.12.5 and plugin sources, or documented)

- Glob dot-file matching: `requireLiteralLeadingDot` defaults to true on Unix and false on Windows
  (tauri `src/scope/fs.rs`).
- Window creation from a synchronous command or event handler deadlocks on Windows
  ([`WebviewWindowBuilder`](https://docs.rs/tauri/latest/tauri/webview/struct.WebviewWindowBuilder.html)).
- The dialog plugin adds a picked path to the fs and asset scopes for the session
  (`tauri-plugin-dialog` 2.8.1 `commands.rs`; [dialog](https://v2.tauri.app/plugin/dialog/),
  [persisted scope](https://v2.tauri.app/plugin/persisted-scope/)).
- `opener:default` grants web, mail and phone links and revealing a file
  (`tauri-plugin-opener` 2.7.2 `permissions/default.toml`).
- Updater runtime: `updater:default`, Windows exit at install and `on_before_exit`, static JSON
  validated across platforms, insecure transport rejected unless opted in
  ([updater](https://v2.tauri.app/plugin/updater/)).
- Release builds without devtools and the log plugin ([debugging](https://v2.tauri.app/develop/debug/),
  [logging](https://v2.tauri.app/plugin/logging/)); single instance first and deep links
  ([single instance](https://v2.tauri.app/plugin/single-instance/),
  [deep linking](https://v2.tauri.app/plugin/deep-linking/)); `listen` returning the unlisten
  promise ([event API](https://v2.tauri.app/reference/javascript/api/namespaceevent/#listen)).
- Observed: `tauri add` ran `cargo fmt` over the crate and reformatted the JSON configuration; the
  canonicalize-and-`starts_with` `read_note` example compiled.
- Observed: commands taking a plain `AppHandle` failed inside a runtime-generic `configure` with `AppHandle: CommandArg<'_, R> is not satisfied`; making them generic over `R: Runtime` fixed it.
