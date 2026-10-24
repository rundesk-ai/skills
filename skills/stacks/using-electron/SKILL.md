---
name: using-electron
description: Use when building, reviewing, debugging, securing, upgrading or shipping an Electron app — `electron` in package.json, a BrowserWindow, a preload script — including the main, renderer and preload split, contextBridge and IPC design, webPreferences, navigation and remote content, custom protocols and CSP, fuses and ASAR, packaging, native modules, code signing, notarization, auto-update, and memory use or slow startup. It supplies Electron's traps, secure defaults and the commands that prove a change. Do not use for plain Node or browser code that touches no Electron API.
---

# Use Electron

The renderer is a browser tab that may run hostile content; the main process is Node with full
access to the machine. Everything between them — the preload's bridge, the IPC handlers, the
protocol handler, `shell.openExternal` — is the security boundary, and most mistakes there work
perfectly in a demo. Prove a change by running the app and calling the bridge, not by reading it.

## Establish the version before changing code

```sh
npx electron --version
npm ls electron electron-builder @electron-forge/cli electron-updater
```

Electron supports only its three newest majors with security fixes, and each major brings a new
Chromium and Node, so an app more than two majors behind ships known browser vulnerabilities.
Answers recalled from older Electron are often wrong now — see the version table in
[Shipping](references/shipping.md).

## The traps, and how to prove each one

| Trap | What you see | The proof |
|---|---|---|
| A preload exposing `invoke: (channel, ...args) => ipcRenderer.invoke(channel, ...args)` | Works; any script in the page can call every handler, including internal ones | Expose one named function per operation, with the channel fixed in the preload; try calling an internal channel from the devtools console |
| A handler that trusts its caller | Any frame or navigated page can call it | Check `event.senderFrame` in every handler: not null, and its URL's scheme and host are yours. Validate every argument as untrusted input |
| Comparing `new URL(u).origin` for `app:` or `file:` pages | `"null" === "null"`: every such page passes | Compare `protocol` and `host`, or use `senderFrame.origin` |
| No `will-navigate`, `will-redirect` and `setWindowOpenHandler` guards | A link, `location.href` or a server redirect loads a remote page **with the preload still exposed**; `window.open` creates a full `BrowserWindow` | Deny by default for every `webContents`; open allowed `https:` links with `shell.openExternal` |
| No permission handler on the session | Notifications, geolocation, camera and other requests are granted without asking | `session.setPermissionRequestHandler` and `setPermissionCheckHandler` on every session you use, allowing only what the app needs |
| `ipcMain.handle` registered inside `createWindow` | `Attempted to register a second handler` when macOS `activate` opens a second window | Register handlers once at startup |
| `shell.openExternal(url)` with page-supplied text | `file:`, `smb:` or a custom scheme launches a program | Allow `https:` (and `mailto:` if needed) only, parsed with `new URL` |
| A `protocol.handle` file server with `decodeURIComponent` then `path.join` | `..%2f` escapes the root and serves `/etc/hosts` | `path.resolve` under the root, then require `path.relative(root, p)` to not start with `..` — see [Security](references/security.md) |
| The app loaded with `loadFile` (`file://`) | The page can `fetch` any local file | Serve from a privileged custom scheme (`app://`), and turn off the `GrantFileProtocolExtraPrivileges` fuse |
| `nodeIntegration: true`, `contextIsolation: false` or `sandbox: false` to make a library work | `nodeIntegration` silently turns the sandbox off; without isolation `exposeInMainWorld` throws and the preload stops | Keep all three defaults; move the Node code to the main process behind a named IPC call |
| Large data returned through the bridge | 1 M rows: IPC 0.5 s, the contextBridge copy 76 s with the page frozen | Send a JSON string and `JSON.parse` in the page (0.8 s), or a `MessagePort` — see [IPC and processes](references/ipc-and-processes.md) |
| Synchronous or CPU-heavy work in the main process; `ipcRenderer.sendSync` | Every window's IPC stalls for the whole duration | Move it to a `utilityProcess` or worker; use `invoke` |
| Throwing a custom error from `ipcMain.handle` | The page gets only `Error invoking remote method 'x': Error: msg`; `code` and fields are gone | Return `{ ok: false, code, message }` instead of throwing |
| A native module built for Node | `was compiled against a different Node.js version using NODE_MODULE_VERSION` | Prefer N-API modules (no rebuild); otherwise `@electron/rebuild`, and upgrade the module if it no longer compiles against Electron's V8 |
| A file in `app.asar` run by another program (`sh`, a binary) | `Not a directory` | `asarUnpack` it and use the `app.asar.unpacked` path |
| Fuses flipped on macOS without re-signing | The app is killed at launch (exit 137) | `resetAdHocDarwinSignature`, or sign after flipping; check with `npx @electron/fuses@latest read --app <path>` |

## Defaults for a new window

Leave `sandbox`, `contextIsolation` and `webSecurity` on and `nodeIntegration`,
`nodeIntegrationInSubFrames` and `allowRunningInsecureContent` off, which are the defaults; any
change to one of them needs a stated reason in review. Load the app from a custom protocol, and
install the navigation guards for every `webContents` — the code is in
[Security](references/security.md).

## Prove it from the command line

```sh
npx electron .                                   # never `electron src/main.js`: the app name becomes "Electron" and userData moves
npx electron-builder --dir                       # or `npx electron-forge package`: an unpacked build to inspect
npx @electron/fuses@latest read --app <built app>
npx @electron/asar list <built app>/…/app.asar   # what shipped: no secrets, tests or source maps you did not intend
```

Test the bridge and handlers end to end with Playwright's `_electron.launch` — see [IPC and
processes](references/ipc-and-processes.md) for what it cannot launch and what hidden windows hide.

## Read only what the task needs

- The preload bridge, IPC handlers, sender checks, navigation, `openExternal`, custom protocols,
  CSP, permissions, or fuses: [Security](references/security.md).
- IPC design, payload size, errors across IPC, the process model, memory per window, startup time,
  ESM, utility processes: [IPC and processes](references/ipc-and-processes.md).
- Packaging, ASAR, native modules, signing, notarization, auto-update, upgrading Electron:
  [Shipping](references/shipping.md).
- Auditing a claim here: [Sources](references/sources.md).

## Report

Name the window, channel or setting, the file, and the run that proves it: a bridge call that
succeeded or was refused, a fuse read from the built app, a launch of the packaged build.
