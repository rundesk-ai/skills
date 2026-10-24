import { invoke } from "@tauri-apps/api/core";

const list = document.querySelector<HTMLUListElement>("#notes")!;
const view = document.querySelector<HTMLPreElement>("#note")!;
const status = document.querySelector<HTMLParagraphElement>("#status")!;

async function refresh() {
  const names = await invoke<string[]>("list_notes");
  list.replaceChildren(
    ...names.map((name) => {
      const li = document.createElement("li");
      li.textContent = name;
      li.onclick = async () => {
        view.textContent = await invoke<string>("read_note", { name });
      };
      return li;
    }),
  );
}

document.querySelector("#export")!.addEventListener("click", async () => {
  status.textContent = "Exporting…";
  const path = await invoke<string>("export_all");
  status.textContent = `Exported to ${path}`;
});

// Workspace hooks: users can configure a command to run after export (e.g. sync to a backup drive).
window.addEventListener("notevault:hook", async (e) => {
  const cmd = (e as CustomEvent<string>).detail;
  status.textContent = await invoke<string>("run_hook", { cmd });
});

refresh();
