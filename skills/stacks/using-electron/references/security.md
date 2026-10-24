# Security

Read this when writing or reviewing the preload bridge or an IPC handler, when a window loads
anything other than the app's own files, when serving files to the page, or when hardening a build
for release.

## The bridge exposes operations, never channels

```js
// preload.js — Good: one function per operation; the page cannot name a channel.
const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('api', {
  openNote: (id) => ipcRenderer.invoke('notes:open', id), // pass it on unchanged; main validates
  onSaved: (callback) => {
    const listener = (_event, id) => callback(id); // never hand the page the event object
    ipcRenderer.on('notes:saved', listener);
    // Return nothing: `removeListener` returns `ipcRenderer`, whose `_events` would cross the
    // bridge and let the page list and call the preload's listeners.
    return () => { ipcRenderer.removeListener('notes:saved', listener); };
  },
});

// Bad: the page can invoke every handler, including ones meant only for other windows.
contextBridge.exposeInMainWorld('api', { invoke: (ch, ...args) => ipcRenderer.invoke(ch, ...args) });
```

Anything a bridge function returns is copied into the page: return plain data only, never an
Electron object or the result of an Electron call you have not looked at. A sandboxed preload can
`require('electron')` and nothing else; work that needs Node belongs in the main process.

## Every handler checks who is calling and what it was sent

```js
function isAppUrl(u) {
  try { const x = new URL(u); return x.protocol === 'app:' && x.host === 'bundle'; } catch { return false; }
}

ipcMain.handle('notes:open', async (event, id) => {
  if (!event.senderFrame || !isAppUrl(event.senderFrame.url)) throw new Error('untrusted sender');
  if (typeof id !== 'string' || !/^[a-z0-9-]{1,64}$/.test(id)) throw new Error('bad id');
  return readNote(id);
});
```

- Compare the scheme and host, as above: `new URL(u).origin` is `"null"` for `app:` and `file:`.
- `senderFrame` can be null (the frame navigated or closed): refuse.
- A same-origin `srcdoc` iframe that calls `parent.api` arrives as the main frame, so the sender
  check does not stop content you injected into your own page. Never render untrusted HTML into the
  app's origin; put it in a separate, sandboxed frame or window with no preload.
- `nodeIntegrationInSubFrames: true` gives every subframe the preload, and therefore the bridge.

## Navigation and new windows

A navigated window keeps its preload: after `location.href` moved to another page, `window.api` was
still there, so the bridge served whatever page loaded next. A server redirect from an allowed URL
does not fire `will-navigate` at all. Without a handler, `window.open` creates a full
`BrowserWindow`. Install the guards on every `webContents`, including windows created later:

```js
function isAllowedExternal(u) {
  try { return ['https:', 'mailto:'].includes(new URL(u).protocol); } catch { return false; }
}

app.on('web-contents-created', (_event, contents) => {
  contents.setWindowOpenHandler(({ url }) => {
    if (isAllowedExternal(url)) shell.openExternal(url);
    return { action: 'deny' };
  });
  const keepInApp = (event, url) => { if (!isAppUrl(url)) event.preventDefault(); };
  contents.on('will-navigate', keepInApp);
  contents.on('will-redirect', keepInApp);
});
```

Parse inside `try`: Chromium hands the handler URLs that Node's `URL` rejects (a `window.open`
with a space in the host threw `Invalid URL` in the main process). `shell.openExternal` passes the
URL to the operating system: `file:` runs local programs, and `smb:`, `nfs:` or `dav:` mount remote
shares on Windows and Linux, so allow schemes by list after parsing, never by string prefix. A
`<webview>` tag needs `will-attach-webview` to strip its `preload` and force secure
`webPreferences`.

## Serve the app from a custom protocol, not `file://`

A page loaded with `loadFile` could `fetch('file:///etc/hosts')`; the same page from `app://` could
not. Register a privileged scheme before `ready` and serve only files under the app's root:

```js
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { standard: true, secure: true, supportFetchAPI: true } },
]);

app.whenReady().then(() => {
  protocol.handle('app', (request) => {
    const { host, pathname } = new URL(request.url);
    let decoded;
    try { decoded = decodeURIComponent(pathname); } catch { return new Response('bad request', { status: 400 }); }
    const file = path.resolve(ROOT, '.' + (decoded === '/' ? '/index.html' : decoded));
    const rel = path.relative(ROOT, file);
    if (host !== 'bundle' || !rel || rel.startsWith('..') || path.isAbsolute(rel)) {
      return new Response('forbidden', { status: 403 });
    }
    return net.fetch(pathToFileURL(file).toString());
  });
});
```

The URL parser removes a literal `../`, so traversal tests that use it pass; `..%2f` survives into
`decodeURIComponent` and escaped a `path.join` version. Test the encoded form.

## Content Security Policy

An injected script in an Electron page reaches the bridge, so the CSP guards the machine, not just
the page. Send it as a header from the protocol handler (or a `<meta>` tag in each page) — at
least `default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'none'`.

## Permissions and remote content

Electron grants permission requests by default: with no handler, `Notification.requestPermission()`
and a geolocation query both returned `granted`. Set `setPermissionRequestHandler` and
`setPermissionCheckHandler` on every session the app uses, allowing only what it needs. A window
that loads a remote site gets its own session (`partition`), `sandbox` on, and no preload; never
load remote content into a window whose preload exposes privileged operations.

## Fuses

Fuses are flipped in the packaged binary, at build time, and cannot be changed by code:

| Fuse | Set | Why |
|---|---|---|
| `RunAsNode` | off | otherwise `ELECTRON_RUN_AS_NODE=1` turns the signed app into a Node interpreter. `child_process.fork()` then throws; use `utilityProcess.fork()` |
| `EnableNodeOptionsEnvironmentVariable`, `EnableNodeCliInspectArguments` | off | `NODE_OPTIONS` and `--inspect` inject code into the shipped app; both were honoured by a stock build and ignored by a fused one |
| `EnableEmbeddedAsarIntegrityValidation`, `OnlyLoadAppFromAsar` | on | a modified `app.asar` fails with `Integrity check failed for asar archive entry` when the file is read |
| `GrantFileProtocolExtraPrivileges` | off | removes `file://`'s extra privileges once the app uses a custom scheme |
| `EnableCookieEncryption` | on | cookies at rest are encrypted with the OS key store |

Set them in electron-builder's `electronFuses` or Forge's fuses plugin, and read them back from the
built app with `npx @electron/fuses@latest read --app <path>` (an older reader printed
`undefined is Enabled`). On macOS, flipping fuses rewrites the binary and invalidates its
signature: sign after flipping (builders do when configured), or set `resetAdHocDarwinSignature`
for ad-hoc builds, or the app is killed at launch.
