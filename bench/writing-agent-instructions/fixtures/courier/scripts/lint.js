// Fails on `console.log` in src/: request data must not reach the logs by accident. Reads only.
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

function files(dir) {
  return readdirSync(dir).flatMap((name) => {
    const path = join(dir, name);
    return statSync(path).isDirectory() ? files(path) : [path];
  });
}

const bad = files("src").filter((path) => /console\.log\(/.test(readFileSync(path, "utf8")));
bad.forEach((path) => console.error(`${path}: console.log`));
process.exit(bad.length ? 1 : 0);
