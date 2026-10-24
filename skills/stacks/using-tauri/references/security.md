# Security

Read this when adding a command, plugin, window or remote URL, when changing a capability,
permission, scope or the CSP, or when reviewing what the page can reach.

## What the page may call

| Kind | Allowed when | Restricted by |
|---|---|---|
| A plugin command (`plugin:fs|read_file`) | a capability attached to that window grants its permission | the capability's `windows`/`webviews`, `remote`, `platforms`, and the permission's scope |
| Your own command, by default | it is in `generate_handler!` | **nothing**: every local window can call it |
| Your own command, with `AppManifest::commands` in `build.rs` | a capability grants `allow-<command>` | the same as a plugin command |

To limit which window may call your commands, list them in `build.rs`:

```rust
fn main() {
    tauri_build::try_build(
        tauri_build::Attributes::new()
            .app_manifest(tauri_build::AppManifest::new().commands(&["read_config", "upload"])),
    )
    .expect("failed to run tauri-build");
}
```

Each command then needs `allow-read-config` (or `allow-upload`) in a capability, and a command left
out of the list is refused.

## Capabilities

- **Grant the smallest set to the window that needs it.** Run `npx tauri permission ls <plugin>` to
  see what a set such as `fs:default` actually grants before adding it.
- **A capability with no `remote` key applies only to the app's own pages.** Remote content gets
  nothing unless a capability names it in `remote.urls`, and the patterns are literal: 
  `https://*.app.example` matches `www.app.example` but not `app.example`. Grant remote pages only
  read-only, non-filesystem commands. On Linux and Android Tauri cannot tell an iframe from its
  window, so an embedded third-party frame gets the window's capabilities.
- **`platforms`** limits a capability to desktop or mobile targets.

## Scopes

`fs`, `opener`, `shell`, `http` and the asset protocol take scopes of allowed paths or URLs.

- Path scopes use variables (`$APPDATA/**`, `$RESOURCE/**`). On Unix, glob patterns skip dot-files
  and dot-directories unless `requireLiteralLeadingDot: false`; on Windows the default is the
  opposite, so `$HOME/**` there covers `.ssh` and every other hidden folder. Scope to the app's own
  directories, never to the home directory.
- For a file the user picks, use the dialog plugin's open dialog: it adds just that path to the fs
  and asset scopes for the session (the persisted-scope plugin keeps it across restarts), instead
  of a broad static scope every page script can use.
- `opener` and `shell` turn page input into launched programs: keep `opener:default` (web, mail and
  phone links, revealing a file) rather than widening it, and never pass a page-supplied string to
  a shell command.

## Content Security Policy

The scaffold sets `"csp": null`, meaning none. Before shipping, set one in `app.security.csp`:

```json
"csp": "default-src 'self'; img-src 'self' asset: http://asset.localhost data:; connect-src ipc: http://ipc.localhost"
```

- **`connect-src ipc: http://ipc.localhost` is required for fast IPC.** Without it, IPC still works
  through a `postMessage` fallback, so nothing looks broken: raw responses arrive as a JavaScript
  `Array` instead of an `ArrayBuffer`, about 30 times slower (175 ms against 6 ms for 10 MiB).
- Tauri adds `sha256` hashes for the inline scripts and styles in your bundled HTML to the policy,
  so do not add `'unsafe-inline'` for them; only content the bundler cannot see (injected at
  runtime) needs another source.
- Remote origins your page fetches from go in `connect-src`; keep `script-src` to `'self'`.
- `withGlobalTauri: true` (the scaffold default) puts `window.__TAURI__` on every page, where any
  injected script finds it. Import from `@tauri-apps/api` and turn it off.

## The asset protocol

Serving local files to the page with `convertFileSrc` needs `app.security.assetProtocol` with
`enable: true` and a narrow `scope`, `asset: http://asset.localhost` in the CSP, and the
`protocol-asset` feature on the `tauri` crate in `Cargo.toml` — without it `cargo check` fails with
`features ... does not match the allowlist`. The scope is the whole defence: `**` exposes every file
the user can read.

## The isolation pattern

`"pattern": { "use": "isolation" }` passes every IPC message through a sandboxed iframe where you
can inspect and reject it, which helps when the frontend pulls in many dependencies. ES modules do
not load inside the isolation app, and it does not replace validating arguments in the command.
