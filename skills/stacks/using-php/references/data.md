# Data: arrays, numbers, strings, JSON, files

Read this when an array, an amount, a string, a JSON document or a file comes out subtly different from
what went in.

## Arrays and references

- A reference to an element survives a copy of the array: after `$ref = &$a[0]; $b = $a;`, writing
  `$b[0]` changes `$a[0]`. A `foreach` by reference that is not `unset` afterwards is the usual source.
- `explode(',', '')` is `['']`, one empty element, not an empty array.

## Numbers and money

| Code | Result | Why it matters |
|---|---|---|
| `PHP_INT_MAX + 1` | a float, and `PHP_INT_MAX + 1 == PHP_INT_MAX` is true | silent overflow; counters and ids stop changing |
| `(int)(PHP_INT_MAX + 1)` | `PHP_INT_MIN` | an out-of-range cast wraps silently (8.5 warns) |
| `(string)1e15` | `"1.0E+15"` | an amount concatenated into SQL, CSV or a URL becomes exponent notation |
| `sprintf('%.2f', 1.5)` under a German locale | `"1,50"` | `%F` is locale-independent: use it for machine output |
| `intdiv(-7, 2)`, `-7 % 2` | `-3`, `-1` | both truncate toward zero; floor yourself for grid or bucket maths |

Hold money as integer minor units, or as decimal strings through bcmath (`BcMath\Number` on 8.4
supports operators). bcmath is an optional extension: check `php -m` on the server. Do not compare floats
with `PHP_FLOAT_EPSILON`; it is relative to 1.0 and wrong for any other magnitude.

## Strings and UTF-8

- `mb_str_pad` arrived in 8.3, and `mb_ucfirst` and `mb_trim` in 8.4; on older targets the byte versions
  split characters. `trim` leaves non-breaking and ideographic spaces.
- Without the `/u` flag, `\w` does not match `é`. With it, invalid UTF-8 makes `preg_*` return `null` or
  `false`; read `preg_last_error_msg()`.
- Validate encoding where text enters (`mb_check_encoding`), because the failure shows up later as a
  `false` from `json_encode` written into a cache or a response body.

## JSON

- An empty PHP array encodes as `[]` whether it meant a list or an object; `json_decode('{}', true)`
  comes back as `[]`. Use `new stdClass` or `JSON_FORCE_OBJECT` where the consumer needs `{}`.
- `json_encode(10.0)` is `10`; `JSON_PRESERVE_ZERO_FRACTION` keeps `10.0` for a typed consumer.
- Before encoding a list, `array_is_list($rows)` proves it will be a JSON array.

## Files written while others read

`file_put_contents($path, …)` from concurrent requests or a cron job lets a reader see a half-written
file: a corrupt cache or config. Write to a temporary file in the same directory, then `rename()` it over
the target, which replaces it in one step. `LOCK_EX` does not protect readers that do not take the lock.
