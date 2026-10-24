# Commands and IPC

Read this when writing or changing a command, managed state, events or channels, when moving
binary data between the page and Rust, or when testing commands.

## Errors the frontend can read

Define one error enum and serialize it as its message:

```rust
#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error(transparent)]
    Io(#[from] std::io::Error),
    #[error("invalid input: {0}")]
    Invalid(String),
}

impl serde::Serialize for AppError {
    fn serialize<S: serde::Serializer>(&self, s: S) -> Result<S::Ok, S::Error> {
        s.serialize_str(&self.to_string())
    }
}

#[tauri::command]
fn read_note(app: tauri::AppHandle, name: String) -> Result<String, AppError> {
    use tauri::Manager;
    let base = app.path().app_data_dir().map_err(|e| AppError::Invalid(e.to_string()))?.join("notes");
    let path = base.join(&name).canonicalize()?; // resolves `..` and symlinks; fails if missing
    if !path.starts_with(base.canonicalize()?) {
        return Err(AppError::Invalid(name));
    }
    Ok(std::fs::read_to_string(path)?)
}
```

In JavaScript the rejection value is that string. Serialize a `{ kind, message }` object instead
when the page must branch on the kind.

## Threads

| Command | Runs on | Effect of 1 s of work |
|---|---|---|
| `#[tauri::command] fn` | the main thread | the window stops painting; other invokes queue behind it |
| `#[tauri::command] async fn` | the async runtime | the window keeps painting; a concurrent invoke returned in 1 ms |
| `#[tauri::command(async)] fn` | the async runtime | as above, for a sync body |

Inside an `async` command, blocking calls (`std::fs`, `std::thread::sleep`, CPU-heavy work) still
hold a runtime worker: put them in `tauri::async_runtime::spawn_blocking`.

## State

Manage the wrapper you read (`Mutex<T>`, `RwLock<T>`), and lock for the shortest scope: a std `Mutex` guard held across `.await` in an async
command does not compile, and a Tokio mutex held across a slow call serializes every caller.

## Arguments

Struct arguments do not get the camelCase conversion that top-level parameters get; they follow serde:
a `#[derive(Deserialize)]` struct takes its field names as written unless it has
`#[serde(rename_all = "camelCase")]`.

## Events, channels and bytes

- **`listen` returns a promise of the unlisten function.** A component that registers in an effect
  must await that promise in its cleanup, or React's StrictMode double-run leaves duplicate
  listeners and every event fires twice.
- **Events are untyped broadcasts.** `emit` reaches every listener in every window, and a payload
  that fails to deserialize on the listener's side fails there, silently for the emitter. Use
  `emit_to` for one window, and prefer a command's return value for request and reply.
- **Stream with a `Channel`, not events.** A `tauri::ipc::Channel<T>` argument is ordered and scoped
  to one call; send `Response` chunks through it for binary streams.
- **Binary data goes raw.** `Vec<u8>` serializes to a JSON array of numbers.

| 10 MiB | Time |
|---|---|
| return `Vec<u8>` | 97 ms |
| return `tauri::ipc::Response::new(bytes)` | 5 ms |
| `Channel<Response>` in 64 KiB chunks | 13 ms |
| send `Array.from(bytes)` to a `Vec<u8>` parameter | 544 ms |
| send the `Uint8Array` itself; read `request.body()` as `InvokeBody::Raw` | 2 ms |

```rust
use tauri::ipc::{InvokeBody, Request, Response};

#[tauri::command]
fn upload(request: Request<'_>) -> Result<usize, AppError> {
    match request.body() {
        InvokeBody::Raw(bytes) => Ok(bytes.len()),
        InvokeBody::Json(_) => Err(AppError::Invalid("expected raw bytes".into())),
    }
}

#[tauri::command]
fn thumbnail(id: u32) -> Response {
    Response::new(render_png(id))
}
```

In JavaScript, `invoke('upload', bytes)` sends a `Uint8Array` raw, and a `Response` arrives as an
`ArrayBuffer` (an `Array` means the CSP is forcing the slow fallback; see the security reference).

## Test commands without a window

The `test` feature of `tauri` runs commands through the real IPC and ACL on a mock runtime, in
milliseconds. Share the builder setup between the app and the tests:

```rust
pub fn configure<R: tauri::Runtime>(b: tauri::Builder<R>) -> tauri::Builder<R> {
    b.manage(std::sync::Mutex::new(0u32))
        .invoke_handler(tauri::generate_handler![read_note, upload, thumbnail])
}

pub fn run() {
    configure(tauri::Builder::default())
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

#[cfg(test)]
mod tests {
    use tauri::ipc::{CallbackFn, InvokeBody};
    use tauri::test::{get_ipc_response, mock_builder, INVOKE_KEY};
    use tauri::webview::InvokeRequest;

    #[test]
    fn read_note_rejects_escaping_name() {
        let app = super::configure(mock_builder())
            .build(tauri::generate_context!(test = true))
            .unwrap();
        let w = tauri::WebviewWindowBuilder::new(&app, "main", Default::default()).build().unwrap();
        let res = get_ipc_response(&w, InvokeRequest {
            cmd: "read_note".into(),
            callback: CallbackFn(0),
            error: CallbackFn(1),
            url: "tauri://localhost".parse().unwrap(),
            body: InvokeBody::Json(serde_json::json!({ "name": "../../etc/hosts" })),
            headers: Default::default(),
            invoke_key: INVOKE_KEY.to_string(),
        });
        assert!(res.is_err());
    }
}
```

A command that takes `AppHandle`, `Window`, `WebviewWindow` or `State` without a runtime parameter
is bound to the real runtime, and `generate_handler!` inside `configure` fails with
`AppHandle: CommandArg<'_, R> is not satisfied`. Make such commands generic:
`fn list_notes<R: tauri::Runtime>(app: tauri::AppHandle<R>)`.
Add `tauri = { version = "2", features = ["test"] }` under `[dev-dependencies]`. Use
`generate_context!(test = true)` in tests only: a second plain `generate_context!()` in the same
crate fails to link (`_EMBED_INFO_PLIST is already defined`). The request's `url` decides which
capabilities apply, so a remote URL tests the remote rules. End-to-end tests drive the real app
through `tauri-driver` (WebDriver), which supports Windows and Linux, not macOS.
