+++
skill = "using-electron"
cases_version = 1
kind = "quality"
difficulty = "easy"
fixture = "inkpad"
rubric = """
result.1  Names the cause: the window has no `will-navigate` handler (and no `setWindowOpenHandler`), so clicking a link navigates the app's own window to the site.
result.2  Fixes it in the main process: prevents navigation away from the app's own pages, and opens allowed links in the system browser through `shell.openExternal`, for every window (e.g. `web-contents-created`) or the one window that exists.
result.3  Validates the URL before `shell.openExternal` (parsed with `new URL`, `https:`/`http:`/`mailto:` only), and applies the same check to the existing `app:open-link` handler, rather than opening any string.
result.4  Notes the security consequence, or fixes it: the navigated page keeps the preload's bridge, so a remote site could call every IPC handler.
conduct.1 Verifies by running or testing the change (an Electron run, a scripted check of the handler, or Playwright), not only by reading it.
"""
+++
If you click a link inside a note in Inkpad, the website opens inside our app window and replaces
the app — there's no back button, so people have to quit and restart. Links should open in the
normal browser instead.
