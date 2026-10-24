# Using React validation

The current record for `using-reactjs`; the method is `prompts/benchmark-skill.md`, and the latest result
is in `bench/results/using-reactjs/`.

The `storefront` fixture is a React 19.3 front end tested with Vitest, jsdom and Testing Library; the
benchmark copies a pre-installed `node_modules` into each run. Its seeded defects were each reproduced
before the cases were written: cart rows keyed by index with local quantity state (removing the first
item moves its typed quantity to the next row); a search effect with no cleanup (a stale response
overwrites a newer one), a result count copied into state by an effect, and stale results left after the
box is cleared; and a dashboard whose clock state ticks every 250 ms through a shared context value and
whose price-store subscriber stores a fresh copy on every unchanged rebroadcast (22 commits and about
0.9 s of rendering in 5 idle seconds at 2,000 products), plus a new `Intl.NumberFormat` per row.

The routing cases deploy both this skill and the JavaScript skill; the near miss is a plain module change
(`src/api.js` retry) that touches no component.

2026-10-24, Claude only: routing 2/3 (the indirect question was answered without loading the skill),
near miss not fired. The skill did not load on the easy case; the medium case was mixed; on the complex
case both skilled runs measured before and after and added an idle-render regression test, and neither
unskilled run measured. See the result's notes.
