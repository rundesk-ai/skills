# Language: numbers, dates, strings, collections

Read this when a value comes out subtly different from what went in. Each item was reproduced on Node;
browsers use the same language rules.

## Numbers and money

- `Math.round(-2.5)` is `-2` (it rounds half toward +∞), and `Math.round(-0.4)` is `-0`.
  `Intl.NumberFormat` prints `-0` as `-$0.00` unless you pass `signDisplay: 'negative'`.
- `Intl.NumberFormat` rounds half away from zero by default; `roundingMode: 'halfEven'` gives banker's
  rounding. It also accepts a decimal string (`format('1.005')` gives `1.01` exactly), which avoids the
  binary error `toFixed` exposes.
- Intl output contains non-breaking spaces (U+00A0 before `€` in German, U+202F as the French group
  separator) and changes when ICU updates, so a test comparing it with a typed string fails. Build the
  expected value with the same formatter, or compare parts from `formatToParts`.
- `%` is a remainder: `-7 % 3` is `-1`. To wrap an index use `((i % n) + n) % n`.
- `parseInt` converts to a string first: `parseInt(0.0000005)` is `5`, and
  `['1', '2', '3'].map(parseInt)` is `[1, NaN, NaN]` because the index arrives as the radix.
  `Number('')` and `Number(' ')` are `0`, so an empty form field becomes zero, not an error; reject empty
  input before converting.
- `BigInt` and `number` do not mix (`1n + 1` throws), and `JSON.stringify` throws on a `BigInt`; give the
  type a `toJSON` or convert to a string at the edge.
- `Math.max()` is `-Infinity`; `[].reduce(fn)` without an initial value throws.

## Dates

- A date-only ISO string (`'2026-03-08'`) parses as UTC; a date-time without an offset
  (`'2026-03-08T00:00'`) parses as local; other formats (`'2026/03/08'`, a space instead of `T`) are
  engine-defined.
- `toISOString().slice(0, 10)` turns a local date into the UTC date: east of UTC, local midnight is the
  previous day. `new Intl.DateTimeFormat('en-CA', { timeZone }).format(d)` gives `YYYY-MM-DD` in a named
  zone.
- Months are zero-based and overflow silently: `new Date(2026, 1, 31)` is 3 March, and
  `setMonth(month + 1)` on 31 January lands in March. Clamp the day yourself.
- Adding `86400000` ms is not "next day" across a daylight-saving change (23 or 25 hours that day);
  `setDate(d.getDate() + 1)` keeps the wall-clock time. Decide whether the rule is elapsed time or
  calendar time.
- An invalid date throws only when serialized: `new Date('garbage').toISOString()` raises
  `RangeError: Invalid time value` far from where the bad string came in.
- `Temporal` is built in from Node 26 and in recent browsers, and missing on older lines: feature-detect
  (`typeof Temporal !== 'undefined'`) or use the polyfill. `Temporal.PlainDate` is the type for a
  calendar date, and `{ overflow: 'reject' }` rejects 30 February.

## Strings

- `.length` counts UTF-16 code units: an emoji is 2, a family emoji is 8 code units and one visible
  character. Count and truncate user-visible text with `Intl.Segmenter` (grapheme granularity).
  `slice` can cut a surrogate pair in half, and `encodeURIComponent` then throws `URIError`;
  `isWellFormed()` checks first.
- Two strings that look identical can differ in normalization (`'é'` as one code point or two): normalize
  with `normalize('NFC')` before comparing, hashing, or using text as a unique key.
- `toUpperCase` and `toLowerCase` are locale-independent; `toLocaleUpperCase('tr')` turns `i` into `İ`.
  Use the plain forms for identifiers and protocol strings, and `Intl.Collator(locale, { sensitivity:
  'base' })` to compare words a person typed (`'ß'.toUpperCase()` is `'SS'`, so lowering both sides is not
  a case-insensitive comparison).
- Reuse one `Intl.Collator`: `localeCompare` with options builds a new one per call.
- A regex with the `g` flag keeps `lastIndex` between `test()` calls: the same `/a/g` returns `true`,
  `false`, `true`. Without `/u`, `.` matches half an emoji.

## Objects, collections and copies

- Integer-like keys come first, in ascending order: `Object.keys({ b: 1, 2: 1, a: 1, 1: 1 })` is
  `['1', '2', 'b', 'a']`. Object keys are strings, so `o[1]` and `o['1']` are one entry and every object
  used as a key becomes `'[object Object]'`.
- `Map` keys compare by identity and type: `map.get('1')` misses a key stored as `1`, and an array key is
  never found again by a new array with the same contents. Key on a string such as `` `${x},${y}` ``.
- `JSON.parse(JSON.stringify(x))` turns `Date` into a string, drops `undefined`, turns `NaN` into `null`,
  and turns `Map` and `Set` into `{}`. `structuredClone` keeps those but drops class identity, getters and
  methods, throws on functions, and was 1.8 times slower than the JSON round trip on plain data. Pick by
  what must survive, and do not deep-clone in a hot path.
- Spread and `Object.assign` copy one level. `Array(3).fill([])` puts one shared array in every slot; use
  `Array.from({ length: 3 }, () => [])`.
- `map` and `forEach` skip holes: `new Array(3).map((_, i) => i)` is still three holes.
- `for...in` over an array also visits added properties; use `for...of`.
- `Array.prototype.sort` has been stable since ES2019, so sorting by a secondary key and then a primary
  key is safe.

## Performance claims to check before acting on

Measured on Node 25 (V8 14), each variant in its own process, median of several runs:

| Claim | Result |
|---|---|
| String `+=` in a loop is quadratic | a myth on V8: within 1.5 times of `join` for a million pieces |
| `delete` makes objects slow | true in a hot loop: reads 6.4 times slower after `delete`; setting `undefined` is not |
| Objects of many shapes are slower | true in a hot loop: 4.5 times slower past four shapes at one call site |
| Arrays with holes are slow | about 7%; the real trap is that iteration skips them |

Apply the two real ones only where a profile shows the loop is hot; build hot objects with one factory
and a fixed key order.
