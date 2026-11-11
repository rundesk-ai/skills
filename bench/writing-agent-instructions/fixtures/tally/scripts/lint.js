// Fails on tabs and trailing spaces in src/ and test/. Reads only; changes nothing.
import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

let bad = 0;
for (const dir of ["src", "test"]) {
  for (const name of readdirSync(dir)) {
    readFileSync(join(dir, name), "utf8").split("\n").forEach((line, i) => {
      if (/\t|[ ]+$/.test(line)) {
        console.error(`${dir}/${name}:${i + 1}: tab or trailing space`);
        bad += 1;
      }
    });
  }
}
process.exit(bad ? 1 : 0);
