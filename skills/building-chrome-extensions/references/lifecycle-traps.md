# Lifecycle traps

The failure modes a test suite will not catch. Every one of these fails **silently** — no
exception, no console error, just behaviour that quietly stops happening.

## The service worker stops, constantly

Three timers run at once:

| Limit                   | Value                                                  |
| ----------------------- | ------------------------------------------------------ |
| Idle before termination | **30 seconds**; any event or `chrome.*` call resets it |
| One request             | 5 minutes maximum                                      |
| One `fetch()` response  | 30 seconds maximum                                     |

**Module-scope state does not survive.** A variable set on one wake is `undefined` on the next,
with no error. This is the single most common Manifest V3 production bug. Persist anything that
must outlive one event to `chrome.storage` before the next `await`.

**There is no DOM.** No `window`, no `document`, no `localStorage` in the worker; use an offscreen
document for DOM-only work.

**Distrust older keepalive advice:** from Chrome 110 every event and API call resets the idle
timer, and from Chrome 114 opening a port no longer keeps the worker alive — only **messages**
through it do.

## Listeners must register synchronously

Register every listener in global scope, on first script evaluation. A listener added after an
`await`, or inside an async callback, misses events dispatched in that window — silently.

```js
// ✅ top level, synchronous
chrome.runtime.onInstalled.addListener(handleInstall);

// ❌ registered too late; the event that woke the worker is already gone
(async () => {
  await something();
  chrome.runtime.onInstalled.addListener(handleInstall);
})();
```

**Registration failure kills everything quietly.** A script evaluation error means the worker never
registers, `onInstalled` never fires, and DevTools cannot attach to show you why.

## DevTools hides the bug

**Opening the service worker in DevTools keeps it alive.** A termination bug is not reproducible
while you are inspecting the worker. To test it, terminate deliberately — Puppeteer ≥22.1.0 can
`waitForTarget(t => t.type() === 'service_worker')` then `worker.close()`.

## Storage limits

| Area      | Limit                                                                         |
| --------- | ----------------------------------------------------------------------------- |
| `local`   | 10 MB, lifted by `unlimitedStorage`                                           |
| `sync`    | 100 KB total, **8 KB per item**, 512 items, **120 writes/minute**, 1,800/hour |
| `session` | 10 MB, not exposed to content scripts by default                              |

`unlimitedStorage` lifts `local` only. Quota counts the JSON stringification of every value **plus
the length of every key**.

A write that exceeds a quota **fails immediately** and sets `runtime.lastError`, or rejects. A
settings panel wired to an input event blows the 120-writes-a-minute ceiling trivially, and the
failure is an unawaited rejected promise nobody sees. Debounce, and `await` every write before the
worker can idle — a fire-and-forget `set()` is a real data-loss path.

## Alarms, not timers

`setTimeout` lives in the worker and dies with it. A 45-second timer in a worker that idles at 30
never fires. `chrome.alarms` is owned by the browser, survives eviction, and **wakes the worker**.

The floor is 30 seconds (one minute before Chrome 120). **Unpacked builds have no floor at all**,
so alarm timing tested from a loaded directory does not hold once packaged.

## Messaging

`return true` must be the **synchronous** return value of the listener. An `async` listener returns
a promise, so by the time it resolves Chrome has already closed the port. Never mark an
`onMessage` listener `async`; do the async work in an inner function and return `true` on the last
synchronous line.

Three error strings, three different causes:

| String                                                         | Cause                                                                                                                                |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| "The message port closed before a response was received"       | The listener claimed it would respond and did not, or the worker was torn down                                                       |
| "Could not establish connection. Receiving end does not exist" | Content scripts are **not** re-injected into already-open tabs on install or update. Inject over open tabs yourself in `onInstalled` |
| "Extension context invalidated"                                | An update, reload or disable severed a content script's handle; every `chrome.*` call from it now throws                             |

## Remote code and the Vite trap

The content security policy cannot be relaxed. `'unsafe-eval'` is an **installation error**.
Localhost sources are permitted **for unpacked extensions only** — which is exactly why hot module
replacement works from the dev server and dies the moment the extension is packed. Verify against a
packed build, never the dev server.

**Vue's runtime compiler uses `new Function()` and cannot run in an extension page.** Single-file
components must be precompiled and the runtime-only build used. Never alias to the full build,
never pass a `template:` string at runtime, and audit dependencies for anything reaching for
`new Function`.

A remote JSON configuration file is allowed; a remote script is not, including one pulled by a
transitive dependency — which is the usual cause of a rejection on this ground. Libraries that
inject remote scripts at runtime, such as Google Analytics' `gtag.js` or a sign-in flow that loads
a provider script, are rejected for this reason; use a build that bundles everything, or a
server-side API such as the analytics measurement protocol.
