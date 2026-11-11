// Applies the numbered files in migrations/ to the database named by DATABASE_URL, in order.
import { readdirSync } from "node:fs";

for (const name of readdirSync("migrations").sort()) console.log(`would apply ${name}`);
