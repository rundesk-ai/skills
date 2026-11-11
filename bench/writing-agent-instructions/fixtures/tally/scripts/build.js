// Checks that the package can be loaded and its entry point runs. Writes nothing.
import { count } from "../src/count.js";

if (count("ok\n").lines !== 1) {
  console.error("build check failed: count is broken");
  process.exit(1);
}
console.log("build ok");
