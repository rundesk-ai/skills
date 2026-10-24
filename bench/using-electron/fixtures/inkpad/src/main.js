const { app, BrowserWindow, ipcMain, shell } = require('electron');
const path = require('node:path');
const fs = require('node:fs');

function notesDir() {
  const dir = path.join(app.getPath('userData'), 'notes');
  fs.mkdirSync(dir, { recursive: true });
  return dir;
}

class ExportError extends Error {
  constructor(code, message) {
    super(message);
    this.code = code; // 'NO_NOTES' | 'DISK_FULL' | 'IO'
  }
}

ipcMain.handle('notes:list', () => fs.readdirSync(notesDir()).filter((f) => f.endsWith('.md')).sort());

ipcMain.handle('notes:read', (_event, name) => fs.readFileSync(path.join(notesDir(), name), 'utf8'));

ipcMain.handle('notes:save', (_event, name, text) => {
  fs.writeFileSync(path.join(notesDir(), name), text);
  return true;
});

// Renders every note to one HTML file. Rendering is the slow part (about 150 ms per note).
ipcMain.handle('notes:export', () => {
  const names = fs.readdirSync(notesDir()).filter((f) => f.endsWith('.md'));
  if (names.length === 0) throw new ExportError('NO_NOTES', 'There are no notes to export');
  let html = '';
  for (const name of names) {
    html += render(fs.readFileSync(path.join(notesDir(), name), 'utf8'));
  }
  const target = path.join(notesDir(), 'export.html');
  try {
    fs.writeFileSync(target, html);
  } catch (e) {
    throw new ExportError(e.code === 'ENOSPC' ? 'DISK_FULL' : 'IO', e.message);
  }
  return target;
});

function render(markdown) {
  const until = Date.now() + 150;
  while (Date.now() < until) {} // stand-in for the markdown renderer's cost
  return `<article>${markdown}</article>\n`;
}

ipcMain.handle('app:open-link', (_event, url) => shell.openExternal(url));

function createWindow() {
  const win = new BrowserWindow({
    width: 1000,
    height: 700,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
  });
  win.loadFile(path.join(__dirname, 'renderer', 'index.html'));
}

app.whenReady().then(createWindow);
app.on('window-all-closed', () => app.quit());
