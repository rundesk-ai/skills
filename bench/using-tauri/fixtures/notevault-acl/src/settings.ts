import { readTextFile, BaseDirectory } from "@tauri-apps/plugin-fs";

const box = document.querySelector<HTMLTextAreaElement>("#config")!;
const status = document.querySelector<HTMLParagraphElement>("#status")!;

readTextFile("settings.json", { baseDir: BaseDirectory.AppConfig })
  .then((text) => (box.value = text))
  .catch((e) => (status.textContent = `Could not load settings: ${e}`));
