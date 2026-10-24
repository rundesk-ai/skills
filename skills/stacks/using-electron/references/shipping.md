# Shipping

Read this when packaging, adding a native module or a bundled executable, signing, notarizing,
setting up auto-update, or upgrading Electron.

## Packaging and ASAR

- **Paths differ between development and the package.** In the package, `__dirname` is inside
  `app.asar` and resources sit under `process.resourcesPath`. Branch on `app.isPackaged`, resolve
  from `app.getAppPath()` or `process.resourcesPath`, never from the working directory.
- **Node's `fs` reads inside `app.asar`; other programs cannot.** `sh <script in app.asar>` failed
  with `Not a directory`. Anything another process opens — a shell script, a helper binary, a
  native library — goes in `asarUnpack` and is addressed through the `app.asar.unpacked` path.
- **Check what shipped.** `npx @electron/asar list <app.asar>`: tests, `.env` files, source maps
  and other platforms' native builds end up there unless `files` excludes them. electron-builder
  unpacked 26 MB of other platforms' prebuilds and C sources beside a 424 KB `app.asar`.

## Native modules

Electron has its own Node ABI (`NODE_MODULE_VERSION` 150 in Electron 45, not Node's). A module
built for Node fails to load with `was compiled against a different Node.js version using
NODE_MODULE_VERSION 141. This version of Node.js requires NODE_MODULE_VERSION 150`.

- Modules built on N-API (`better-sqlite3` 13, `bufferutil`) loaded without a rebuild; prefer them.
- Otherwise rebuild for Electron with `@electron/rebuild` (Forge and electron-builder run it). An
  old module version may not compile against Electron's newer V8 at all; upgrade the module rather
  than adding rebuild flags.
- Rebuild in CI for each target platform and architecture, and keep native modules out of the
  renderer.

## Signing and notarization

- **macOS** needs a Developer ID signature with the hardened runtime and notarization
  (`@electron/notarize`, run by Forge and electron-builder when the credentials are set).
  Electron's V8 needs the `com.apple.security.cs.allow-jit` entitlement: without it the app crashes
  at launch with a misleading `Fatal process out of memory: Failed to reserve virtual memory for
  CodeRange`. Auto-update on macOS requires a signed app. Verify
  with `codesign --verify --deep --strict --verbose=2 <app>` and `spctl -a -vv <app>`.
- **Windows**: code-signing keys (OV and EV) must live in hardware or a cloud signing service (such
  as Azure Artifact Signing) since 2023, so CI signs through that service, not a `.pfx` file, and an
  EV certificate no longer skips SmartScreen's reputation building.
- **Secrets** the app stores go through `safeStorage`, not `localStorage` or a JSON file in
  `userData`; on Linux check `safeStorage.getSelectedStorageBackend()`, since `basic_text` means
  no real encryption.

## Auto-update

- The built-in `autoUpdater` uses Squirrel: on macOS it requires a signed app and a zip artifact;
  on Windows it follows Squirrel.Windows installers.
- With `electron-updater` (electron-builder), read its behaviour from the version you ship:
  - Windows signature verification compares the installer's publisher with `publisherName`; when
    `app-update.yml` has none, version 6.8.11 skipped the check. Set `publisherName` (or the
    `win.signtoolOptions` publisher) so an attacker-controlled server cannot ship any installer.
  - `allowPrerelease` (and `allowDowngrade`) let the feed move users to an older or unstable
    version; leave them off for production channels.
  - It does nothing when the app is not packaged unless `forceDevUpdateConfig` is set; test
    updates with two real packaged versions.
- Serve the update feed over HTTPS from a host you control; the code signature, not the transport,
  is what proves an artifact is yours.

## Upgrading Electron

Each major is a Chromium and Node upgrade with breaking changes: read the breaking-changes page for
every major crossed, rebuild native modules, and re-run the security checks above. Changes most often
recalled wrongly:

| Change | Since |
|---|---|
| `contextIsolation` on by default | 12 |
| `remote` module removed (use IPC) | 14 |
| renderers sandboxed by default | 20 |
| `ipcRenderer` and `event.sender` lose their methods through `contextBridge` (their data, such as `_events`, still crosses) | 29 |
| `protocol.handle` replaces `registerFileProtocol` and the other `register*Protocol` calls | 25 |
| ES module main process | 28 |
| `WebContentsView` replaces `BrowserView` | 30 |
| the Electron binary downloads on first run, not at install: cache it in CI | 42 |
| sandboxed preloads lose the `Buffer`, `events`, `url` and `timers` shims | 45 |
