+++
skill = "using-electron"
cases_version = 1
kind = "quality"
difficulty = "complex"
fixture = "inkpad"
rubric = """
result.1  Replaces the generic `invoke(channel, ...args)` bridge with one named function per operation, channels fixed in the preload.
result.2  Validates every handler's input in the main process: `notes:read` and `notes:save` refuse names that escape the notes directory (`../`, absolute paths), with a demonstrated refusal.
result.3  Checks the sender in handlers (`event.senderFrame` present and from the app's own origin, compared by scheme/host, not by `URL.origin` for file: pages) or explains why the navigation guard plus named bridge suffices.
result.4  Adds navigation and new-window guards and validates URLs before `shell.openExternal` (the `app:open-link` handler opens any string, including `file:` URLs).
result.5  Adds a Content Security Policy to the page.
result.6  Addresses the packaged build: serving the app from a custom protocol rather than `file://` and/or turning on fuses (RunAsNode off, NODE_OPTIONS and inspect off, ASAR integrity, OnlyLoadAppFromAsar) in the electron-builder config — or lists them as open with the reason.
result.7  Reports what was changed and what remains open (e.g. code signing, notarization, auto-update), separating fixed from not fixed.
conduct.1 Runs the app or a script against the changed code to show at least one fix works.
"""
+++
We're about to ship Inkpad 1.0. Do a security pass on the Electron app — fix what you find, and
tell me what you changed and what's still open.
