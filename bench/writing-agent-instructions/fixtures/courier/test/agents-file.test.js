// Every service repository in the group carries the same three headings in its rules file, in this
// order, so the group's onboarding script can find them. Do not rename them here alone.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

test("AGENTS.md keeps the group's headings, in order", () => {
  const text = readFileSync("AGENTS.md", "utf8");
  const at = ["## Ground rules", "## Commands", "## Done means"].map((h) => text.indexOf("\n" + h + "\n"));
  assert.ok(at.every((i) => i >= 0), "a group heading is missing");
  assert.deepEqual([...at].sort((a, b) => a - b), at, "the group headings are out of order");
});
