const { contextBridge, ipcRenderer } = require('electron');

// One generic entry point so new features don't need preload changes.
contextBridge.exposeInMainWorld('inkpad', {
  invoke: (channel, ...args) => ipcRenderer.invoke(channel, ...args),
});
