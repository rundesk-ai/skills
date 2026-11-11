#!/usr/bin/env node
import { readFileSync } from "node:fs";
import { count } from "./count.js";

const args = process.argv.slice(2);
const json = args.includes("--json");
const files = args.filter((a) => !a.startsWith("--"));

if (files.length === 0) {
  console.error("usage: tally [--json] <file>...");
  process.exit(2);
}

const rows = files.map((file) => ({ file, ...count(readFileSync(file, "utf8")) }));
if (json) {
  // Scripts parse this: the keys and their order are a published contract.
  console.log(JSON.stringify(rows));
} else {
  for (const r of rows) console.log(`${r.lines}\t${r.words}\t${r.bytes}\t${r.file}`);
}
