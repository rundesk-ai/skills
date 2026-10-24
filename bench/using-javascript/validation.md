# Using JavaScript validation

The current record for `using-javascript`; the method is `prompts/benchmark-skill.md`, and the latest
result is in `bench/results/using-javascript/`.

The `orders` fixture is a dependency-free Node HTTP service with `node --test` tests, run in UTC by its
`npm test` script. Its seeded defects were each reproduced before the cases were written: money in floats
rounded with `toFixed` (13.40 at 7.5% shows 1.00 tax and a 14.41 total); a date-only string parsed as UTC
and read in local time (due dates a day early in New York, hidden by the UTC test run); 64-bit warehouse
ids losing precision in `JSON.parse`; a boolean sort comparator; a recursive merge open to prototype
pollution that turns on an export permission; a nested-quantifier email regex (26 characters took 92 ms,
doubling per character); `forEach(async …)` whose rejection exited the process; a `startsWith` path check
that served a file from the sibling `public-drafts` directory; and an unbounded search cache.

The near-miss routing case uses the React fixture from `bench/using-reactjs/fixtures/storefront`, with
both this skill and the React skill deployed.
