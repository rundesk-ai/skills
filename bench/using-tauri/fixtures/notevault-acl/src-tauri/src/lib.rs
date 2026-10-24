use std::fs;
use std::path::PathBuf;
use std::process::Command;
use std::time::Duration;

use tauri::{AppHandle, Manager};

#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error(transparent)]
    Io(#[from] std::io::Error),
    #[error("{0}")]
    Tauri(#[from] tauri::Error),
}

impl serde::Serialize for AppError {
    fn serialize<S: serde::Serializer>(&self, s: S) -> Result<S::Ok, S::Error> {
        s.serialize_str(&self.to_string())
    }
}

fn notes_dir(app: &AppHandle) -> Result<PathBuf, AppError> {
    let dir = app.path().app_data_dir()?.join("notes");
    fs::create_dir_all(&dir)?;
    Ok(dir)
}

#[tauri::command]
fn list_notes(app: AppHandle) -> Result<Vec<String>, AppError> {
    let mut names = Vec::new();
    for entry in fs::read_dir(notes_dir(&app)?)? {
        names.push(entry?.file_name().to_string_lossy().into_owned());
    }
    names.sort();
    Ok(names)
}

#[tauri::command]
fn read_note(app: AppHandle, name: String) -> Result<String, AppError> {
    Ok(fs::read_to_string(notes_dir(&app)?.join(name))?)
}

/// Renders every note and writes one export file next to the notes.
#[tauri::command]
fn export_all(app: AppHandle) -> Result<String, AppError> {
    let dir = notes_dir(&app)?;
    let mut out = String::new();
    for entry in fs::read_dir(&dir)? {
        let path = entry?.path();
        if path.extension().is_some_and(|e| e == "md") {
            out.push_str(&render(&fs::read_to_string(&path)?));
        }
    }
    let target = dir.join("export.html");
    fs::write(&target, out)?;
    Ok(target.display().to_string())
}

/// Stand-in for the HTML renderer, which takes about 200 ms per note.
fn render(markdown: &str) -> String {
    std::thread::sleep(Duration::from_millis(200));
    format!("<article>{}</article>\n", markdown)
}

/// Runs the user's post-export hook, e.g. `rsync -a ~/Notes /Volumes/Backup`.
#[tauri::command]
fn run_hook(cmd: String) -> Result<String, AppError> {
    let out = Command::new("sh").arg("-c").arg(&cmd).output()?;
    Ok(String::from_utf8_lossy(&out.stdout).into_owned())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![list_notes, read_note, export_all, run_hook])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
