// Counting is pure: text in, numbers out, so the CLI and the tests share one implementation.
export function count(text) {
  const bytes = Buffer.byteLength(text, "utf8");
  const lines = text === "" ? 0 : text.split("\n").length - (text.endsWith("\n") ? 1 : 0);
  const words = text.split(/\s+/).filter(Boolean).length;
  return { lines, words, bytes };
}
