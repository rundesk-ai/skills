// Cuts a release: bumps the patch version in package.json, commits it, tags it and pushes the tag.
// Run by the maintainer only, from a clean main.
import { readFileSync, writeFileSync } from "node:fs";
import { execSync } from "node:child_process";

execSync("node scripts/build.js", { stdio: "inherit" });

const pkg = JSON.parse(readFileSync("package.json", "utf8"));
const [major, minor, patch] = pkg.version.split(".").map(Number);
pkg.version = `${major}.${minor}.${patch + 1}`;
writeFileSync("package.json", JSON.stringify(pkg, null, 2) + "\n");

execSync(`git commit -am "Release ${pkg.version}"`, { stdio: "inherit" });
execSync(`git tag v${pkg.version}`, { stdio: "inherit" });
execSync(`git push origin v${pkg.version}`, { stdio: "inherit" });
