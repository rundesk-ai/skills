import { test } from "node:test";
import assert from "node:assert/strict";
import { count } from "../src/count.js";

test("counts lines, words and bytes", () => {
  assert.deepEqual(count("one two\nthree\n"), { lines: 2, words: 3, bytes: 14 });
});

test("an empty file has no lines", () => {
  assert.deepEqual(count(""), { lines: 0, words: 0, bytes: 0 });
});

test("a last line without a newline still counts", () => {
  assert.equal(count("a\nb").lines, 2);
});
