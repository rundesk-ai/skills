# Electron source basis

Behaviour marked *observed* was reproduced in October 2026 on macOS (arm64) with Electron 45.0.0
(Node 24.22.0, Chromium 156, `NODE_MODULE_VERSION` 150), electron-builder 26.18.0, electron-updater
6.8.11 and Playwright 1.64.1, by running small apps whose main process printed results to stdout.
Windows and Linux were not run, nor were real Developer ID signing, notarization or Electron
Forge; claims about them rest on the documentation cited. Read this when a claim in the skill is
challenged or a new Electron major may have changed it.

## Why Electron is its own skill

Its work starts from `electron` in `package.json`, a `BrowserWindow` and a preload script, and its
decisions — the process split, the preload bridge, fuses, ASAR, Electron's own Node ABI, Squirrel
and electron-updater — do not arise in plain Node or browser code, which another skill owns, nor
in Tauri, which uses the system webview and a Rust core with a capability ACL. Plain Node or DOM
code that happens to run inside Electron stays with the JavaScript skill; this one covers what
exists because of Electron. Shared ideas (the page is untrusted, validate IPC, set a CSP, sign
updates) are outweighed by mechanics that share nothing, so one combined "desktop shell" skill
would load half of its content wrongly every time.

## Security

- [Security checklist](https://www.electronjs.org/docs/latest/tutorial/security),
  [process sandboxing](https://www.electronjs.org/docs/latest/tutorial/sandbox),
  [context isolation](https://www.electronjs.org/docs/latest/tutorial/context-isolation).
  Observed: a bridge exposing `invoke(channel, ...args)` let the page call an internal file-reading
  handler; after `location.href` changed, `window.api` still existed; `window.open` without a
  handler created a `BrowserWindow`; `new URL(...).origin` was `"null"` for both `app:` and `file:`
  URLs while `senderFrame.origin` was `app://bundle`; a same-origin `srcdoc` iframe calling
  `parent.api` arrived as the main frame; `nodeIntegration: true` turned the sandbox off;
  `contextIsolation: false` made `exposeInMainWorld` throw; `ipcRenderer` and the event's `sender`
  lost their methods through the bridge (since 29), but an unsubscribe function returning
  `removeListener`'s result handed the page `ipcRenderer._events`, and the page called a preload
  listener with a forged event; sandboxed preloads in 45 had no `Buffer`, `events`, `url` or
  `timers`.
- [`shell.openExternal`](https://www.electronjs.org/docs/latest/api/shell#shellopenexternalurl-options)
  with untrusted URLs: [Electronegativity check](https://github.com/doyensec/electronegativity/wiki/OPEN_EXTERNAL_JS_CHECK)
  and [URL-open code execution](https://positive.security/blog/url-open-rce).
- [`protocol.handle`](https://www.electronjs.org/docs/latest/api/protocol). Observed: a
  `decodeURIComponent` plus `path.join` handler served `/etc/hosts` for `..%2f`, while literal `../`
  was normalized away by the URL parser; the `path.relative` check returned 403; a page loaded by
  `loadFile` could `fetch` `file:///etc/hosts` and the same page from `app://` could not.
- [Fuses](https://www.electronjs.org/docs/latest/tutorial/fuses). Observed: a stock build honoured
  `ELECTRON_RUN_AS_NODE` and `NODE_OPTIONS`, a fused build ignored them and `--inspect`;
  `child_process.fork()` threw and named `utilityProcess.fork()`, which worked; an edited
  `app.asar` failed with `Integrity check failed for asar archive entry` (exit 133) when the file
  was read; without `resetAdHocDarwinSignature` the fused app was killed at launch (exit 137); an
  old fuses reader printed `undefined is Enabled`. `EnableCookieEncryption`, session partitions and
  `setPermissionRequestHandler` rest on the documentation.

## IPC and processes

- [IPC](https://www.electronjs.org/docs/latest/tutorial/ipc) and
  [MessagePorts](https://www.electronjs.org/docs/latest/tutorial/message-ports). Observed: a thrown
  error reached the page as `Error invoking remote method 'x': Error: msg` without `code` or custom
  fields; class instances lost their methods; a function threw `An object could not be cloned`;
  rows of `{ id, name, tags, when }` took 348 ms by IPC and 21.4 s through the bridge at 600,000,
  and 536 ms against 76–81 s at 1,000,000 (page frozen), 817–847 ms as a JSON string, 466 ms over a
  `MessagePort`.
- [Process model](https://www.electronjs.org/docs/latest/tutorial/process-model). Observed: a 2 s
  loop in main delayed every IPC reply by 2,005 ms while the page kept animating; `sendSync`
  blocked the renderer for the handler's duration; `app.getAppMetrics()` gave 349, 688 and 1,111 MB
  for 1, 5 and 10 windows; after `hide()` 5 of 500 timer ticks and no animation frames ran in 5 s,
  while a never-shown `show: false` window ran at full speed; a 10 MB top-level require added about
  190 ms before `ready`, and `module.enableCompileCache()` cut it from 291 ms to about 60 ms.
- [ES modules](https://www.electronjs.org/docs/latest/tutorial/esm). Observed: top-level
  `await app.whenReady()` never resolved (stopped after 120 s); a sandboxed ESM preload failed with
  `Cannot use import statement outside a module`.
- Observed: `electron src/main.js` named the app "Electron" and moved `userData`; Playwright's
  [`_electron.launch`](https://playwright.dev/docs/api/class-electron) timed out against a build
  with `EnableNodeCliInspectArguments` off and launched the development app in 329 ms.
  [Headless CI](https://www.electronjs.org/docs/latest/tutorial/testing-on-headless-ci).

## Shipping

- [ASAR archives](https://www.electronjs.org/docs/latest/tutorial/asar-archives). Observed:
  `sh <script in app.asar>` failed with `Not a directory`; electron-builder unpacked 26 MB of other
  platforms' prebuilds and C sources beside a 424 KB `app.asar`; a minimal app was 283 MB on disk
  and 131 MB zipped.
- [Native modules](https://www.electronjs.org/docs/latest/tutorial/using-native-node-modules).
  Observed: N-API `better-sqlite3` 13 and `bufferutil` loaded without a rebuild; `better-sqlite3`
  11 failed with `NODE_MODULE_VERSION 141` against 150, and `@electron/rebuild` could not compile it
  against Electron 45's V8.
- [Code signing](https://www.electronjs.org/docs/latest/tutorial/code-signing) and
  [@electron/notarize](https://github.com/electron/notarize). Observed with ad-hoc signing: the
  hardened runtime without `allow-jit` crashed with `Failed to reserve virtual memory for
  CodeRange`. The Windows EV and macOS `safeStorage`, login item and auto-update consequences rest
  on the documentation.
- [`autoUpdater`](https://www.electronjs.org/docs/latest/api/auto-updater). electron-updater 6.8.11
  behaviour was read in its source: the Windows publisher check skipped without `publisherName`,
  macOS needing a zip, no check when unpackaged without `forceDevUpdateConfig`, `allowPrerelease`
  permitting downgrades.
- [Breaking changes](https://www.electronjs.org/docs/latest/breaking-changes),
  [release timelines](https://www.electronjs.org/docs/latest/tutorial/electron-timelines) and the
  [schedule](https://releases.electronjs.org/schedule): 45 current, 43–45 supported, 42 out of
  support on 2026-10-20; the binary downloads on first run from 42.

## Added after an independent review (observed unless marked)

- Every snippet in the skill was run in a headless Electron 45 app: the bridge's unsubscribe
  returned `undefined`; `..%2f` traversal got 403 and a malformed escape 400 from the protocol
  handler, which now serves `index.html` for the root; a `window.open` with a space in the host,
  which had thrown `Invalid URL` in the main process, was denied without an exception; `file:` was
  not opened externally; navigation and a 302 redirect to a remote page were both blocked (the
  redirect, unguarded, had loaded the remote page with the bridge still exposed).
- With no permission handler, `Notification.requestPermission()` and a geolocation query returned
  `granted` ([permission requests](https://www.electronjs.org/docs/latest/tutorial/security#5-handle-session-permission-requests-from-remote-content)).
- A second `ipcMain.handle` for one channel threw `Attempted to register a second handler`; an
  `invoke` on an unregistered channel rejected with `No handler registered`.
- Documented: [`will-redirect`](https://www.electronjs.org/docs/latest/api/web-contents#event-will-redirect),
  [`<webview>` options](https://www.electronjs.org/docs/latest/tutorial/security#12-verify-webview-options-before-creation),
  [`safeStorage`](https://www.electronjs.org/docs/latest/api/safe-storage) and the Linux
  `basic_text` backend, [`render-process-gone`](https://www.electronjs.org/docs/latest/api/web-contents#event-render-process-gone),
  Windows signing keys in hardware and EV reputation ([code signing](https://www.electronjs.org/docs/latest/tutorial/code-signing)).
