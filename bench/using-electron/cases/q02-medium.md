+++
skill = "using-electron"
cases_version = 1
kind = "quality"
difficulty = "medium"
fixture = "inkpad"
rubric = """
result.1  Names why the whole app stalls: the export runs synchronous file I/O and CPU-bound rendering in the main process, which serves every window's IPC, so other calls (e.g. `notes:list`) wait for it (measured here: about 1.9 s).
result.2  Moves the work off the main process's event loop: a `utilityProcess`, a worker thread, or at minimum async I/O with the rendering chunked or offloaded, and says which and why.
result.3  Names why the friendly messages never show: an error thrown from `ipcMain.handle` reaches the renderer as a plain Error whose message is prefixed "Error invoking remote method..." and whose `code` property is gone.
result.4  Fixes the error path so the renderer can branch on the code: return a result object such as `{ ok: false, code }`, or encode the code in a way the renderer parses, and updates the renderer to match.
result.5  Keeps the existing behaviour otherwise (export file location, NO_NOTES / DISK_FULL / IO cases).
conduct.1 Demonstrates both fixes by running something (an Electron run, a script that calls the handlers, or a test), not only by reading.
"""
+++
Two complaints about Export in Inkpad. While it's running, the whole app stops responding — even
switching notes hangs until it finishes. And when something goes wrong, people never see the nice
messages we wrote ("Nothing to export yet.", "Your disk is full."); they get a long "Export failed:
Error invoking remote method..." line instead. Fix both.
