import { invoke } from "@tauri-apps/api/core";

const status = document.querySelector<HTMLParagraphElement>("#status")!;
document.querySelector("#go")!.addEventListener("click", async () => {
  status.textContent = await invoke<string>("export_all");
});
