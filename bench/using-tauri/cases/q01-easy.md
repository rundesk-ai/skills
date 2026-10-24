+++
skill = "using-tauri"
cases_version = 1
kind = "quality"
difficulty = "easy"
fixture = "notevault"
rubric = """
result.1  Names the cause: `export_all` is a synchronous `#[tauri::command]`, which Tauri runs on the main thread, so the window cannot paint or answer other invokes until it returns.
result.2  Fixes it by making the command run off the main thread (`async fn`, or `#[tauri::command(async)]`), and moves the blocking file and render work onto a blocking thread (`spawn_blocking`) or states why the async attribute alone is enough here.
result.3  Keeps the command's contract: same name, same `Result` error behaviour, still registered in `generate_handler!`; the frontend call needs no change, or the change is made.
result.4  Does not "fix" it only on the frontend (a spinner, not awaiting, a timeout) while the main thread still blocks.
conduct.1 Runs `cargo check` (or a build or test) in `src-tauri` and reports the result.
conduct.2 Proves or reasons concretely that the window stays responsive (a concurrent invoke, a mock-runtime test, or the thread name), rather than asserting it.
"""
+++
When someone clicks "Export all" in NoteVault the whole window freezes for several seconds — you
can't scroll the note or click anything — then it comes back once the export finishes. The export
itself is fine. Make the freeze go away.
