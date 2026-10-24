# IPC and processes

Read this when designing a channel, moving data between the page and the main process, handling
errors across IPC, or when the app is slow to start, freezes, or uses too much memory.

## Choosing the call

Stream, or send large or repeated transfers, over a `MessagePort` (`MessageChannelMain`) handed to
the page. Never use `ipcRenderer.sendSync`: it blocks the page for the whole handler. Keep channel
names in one module both the main process and the preload import: an `invoke` on a renamed
channel rejects with `No handler registered`, but a `send` to one is dropped silently.

## What survives the trip

Arguments and results are copied with the structured clone algorithm:

- **Errors lose everything but the message.** A handler that throws an error with a `code` reaches
  the page as `Error invoking remote method 'notes:open': Error: not found` — no `code`, no custom
  fields. Return `{ ok: true, value }` or `{ ok: false, code, message }` and let the page branch.
- **Class instances arrive as plain objects** without their methods; a function anywhere in the
  value throws `An object could not be cloned`.
- **Large values are slow through `contextBridge`.** The bridge copies the value again into the
  page's world, and that copy grows much faster than the data:

  | Rows of `{ id, name, tags, when }` | IPC alone | returned through the bridge | as one JSON string | `MessagePort` |
  |---|---|---|---|---|
  | 600,000 | 0.35 s | 21 s | 0.48 s | — |
  | 1,000,000 | 0.54 s | 76–81 s, page frozen | 0.82 s | 0.47 s |

  Send bulk data as a JSON string and `JSON.parse` it in the page, or transfer it over a
  `MessagePort`; better, page it so the window never holds a million rows.

## The main process is shared by every window

A 2-second synchronous loop in the main process delayed every IPC reply in every window by 2 s
(the pages themselves kept animating, so it looks like a slow backend). Synchronous `fs`, `crypto`
or `child_process` calls, a large `JSON.parse`, and native modules doing work in the main process
all do this. Move heavy work to a `utilityProcess.fork()` (a Node child process that survives the
`RunAsNode` fuse) or a worker thread, and keep the main process to window management and routing.

## Memory and startup

- **Each window is its own renderer process, about 80 MB.** One, five and ten windows used 349,
  688 and 1,111 MB in `app.getAppMetrics()`. Reuse a window, or show content in one window, rather
  than opening a window per document; destroy windows you hide for good.
- **Hidden windows are throttled; never-shown ones are not.** After `hide()` a window's timers ran
  at 1% and animation frames stopped. A window created with `show: false` and never shown ran at
  full speed, so tests and benchmarks built that way miss throttling. Set
  `backgroundThrottling: false` only for a window that must keep working while hidden.
- **Startup is the top-level `require` graph.** A 10 MB module required at the top of `main.js`
  added about 190 ms before `ready`. Require heavy modules inside the function that needs them, and
  enable the compile cache in the main process (`module.enableCompileCache()`), which cut that
  require from 291 ms to about 60 ms. Show the window on `ready-to-show` so the user does not see a
  blank frame.

## ES modules

The main process may be ESM (Electron 28+), but a top-level `await app.whenReady()` never
resolved; use `app.whenReady().then(...)`. A sandboxed preload cannot be an ES module ("Cannot use
import statement outside a module"): keep preloads CommonJS, or bundle them.

## Running and testing

- Test through the real bridge with Playwright: `_electron.launch({ args: ['.'] })`, then call
  `window.api` from the page and assert on the reply, and on the refusal from an untrusted page.
  It cannot attach to a build with the `EnableNodeCliInspectArguments` fuse off; run it against the
  development app, and smoke-test the packaged build by launching it.
- A crashed renderer leaves a blank window and says nothing: listen for `render-process-gone` on
  each `webContents`, log the reason, and reload or recreate the window.
