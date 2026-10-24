# Using Electron validation

The current record for `using-electron`; the method is `prompts/benchmark-skill.md`, and the latest
result is in `bench/results/using-electron/`.

`inkpad` is an Electron 45 notes app without `node_modules`. Its defects were reproduced in a headless
run before the rubrics were written: the preload's generic `invoke(channel, ...args)` let the page
write a file outside the notes directory through `notes:save`; `notes:read` read `/etc/hosts` through
`../`; after the page navigated to `https://example.com/` the bridge was still exposed (no
`will-navigate` or window-open handler); `notes:export` runs synchronous rendering in the main process,
and a `notes:list` sent during it waited 1.9 s; its thrown `ExportError` reached the page as
`Error invoking remote method 'notes:export': Error: There are no notes to export` without `code`, so
the renderer's friendly messages never show; `app:open-link` passes any string to
`shell.openExternal`; the page is loaded from `file://` with no CSP and no fuses configured.

`csvtotal` (routing near miss) is a plain Node CLI whose `reduce` concatenates strings.

2026-10-24: see `bench/results/using-electron/2026-10-24.json`.
