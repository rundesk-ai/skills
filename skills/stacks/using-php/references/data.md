# Data: arrays, numbers, strings, JSON

Read this when an array, an amount, a string or a JSON document comes out subtly different from what
went in.

## Arrays and references

- A reference to an element survives a copy of the array: after `$ref = &$a[0]; $b = $a;`, writing
  `$b[0]` changes `$a[0]`. A `foreach` by reference that is not `unset` afterwards is the usual source.
- Arrays are copied on write. Assigning a million-element array or passing it to a function costs no
  memory until one side writes; the first write copies all of it (16 MB for `range(1, 1e6)`, measured).
  Passing by reference "for speed" saves nothing on a read and can force that copy.
- Objects are handles. A function can mutate the caller's object; copying an array of objects shares
  the objects.
- `sort()` renumbers, `asort()` keeps keys. Sorting has been stable since 8.0.
- `array_merge` renumbers integer keys and lets the right side win string keys; `+` keeps the left
  side's keys and values. For a map keyed by id, use `+` or `array_replace`.
- `explode(',', '')` is `['']`, one empty element, not an empty array.

## Numbers and money

| Code | Result | Why it matters |
|---|---|---|
| `0.1 + 0.2 == 0.3` | false, yet `echo` shows `0.3` | `echo` uses 14 digits; `var_dump` and `json_encode` show `0.30000000000000004` |
| `(int)(19.99 * 100)` | `1998` | truncation of `1998.9999999999998`; `(int)round(19.99 * 100)` is `1999` |
| `PHP_INT_MAX + 1` | a float, and `PHP_INT_MAX + 1 == PHP_INT_MAX` is true | silent overflow; counters and ids stop changing |
| `(int)(PHP_INT_MAX + 1)` | `PHP_INT_MIN` | an out-of-range cast wraps silently (8.5 warns) |
| `(string)1e15` | `"1.0E+15"` | an amount concatenated into SQL, CSV or a URL becomes exponent notation |
| `sprintf('%.2f', 1.5)` under a German locale | `"1,50"` | `%F` is locale-independent: use it for machine output |
| `intdiv(-7, 2)`, `-7 % 2` | `-3`, `-1` | both truncate toward zero; floor yourself for grid or bucket maths |
| `bcadd('1.239', '0', 2)` | `"1.23"` | bcmath truncates; `bcround('1.235', 2)` (8.4) gives `"1.24"` |

Hold money as integer minor units, or as decimal strings through bcmath (`BcMath\Number` on 8.4
supports operators). bcmath is an optional extension: check `php -m` on the server. Do not compare floats
with `PHP_FLOAT_EPSILON`; it is relative to 1.0 and wrong for any other magnitude. `number_format` is
display text: never parse it back.

## Strings and UTF-8

- `strlen('Café 👍')` is 10 bytes; `mb_strlen` is 6 code points; a family emoji is several code points
  and one grapheme (`grapheme_strlen`, from the optional intl extension).
- `substr`, `str_pad`, `strrev`, `wordwrap` and `ucfirst` work on bytes and can split a character.
  `mb_substr`, `mb_str_pad` (8.3), `mb_ucfirst` and `mb_trim` (8.4) do not. `trim` leaves non-breaking and
  ideographic spaces.
- `strtolower` lowers ASCII only, and has ignored the locale since 8.2; `mb_strtolower` handles the rest.
- Without the `/u` flag, `\w` does not match `é`. With it, invalid UTF-8 makes `preg_*` return `null` or
  `false`; read `preg_last_error_msg()`.
- Validate encoding where text enters (`mb_check_encoding`), because the failure shows up later as a
  `false` from `json_encode` written into a cache or a response body.

## JSON

```php
$data = json_decode($body, true, 512, JSON_THROW_ON_ERROR | JSON_BIGINT_AS_STRING);
$out = json_encode($payload, JSON_THROW_ON_ERROR);
```

- Without `JSON_THROW_ON_ERROR`, `json_decode` returns `null` for a syntax error, for the document
  `null`, and for nesting deeper than its depth argument: three different situations, one value.
- An integer above 2^53 decodes as a float and loses its last digits; `JSON_BIGINT_AS_STRING` keeps it.
- An empty PHP array encodes as `[]` whether it meant a list or an object; `json_decode('{}', true)`
  comes back as `[]`. Use `new stdClass` or `JSON_FORCE_OBJECT` where the consumer needs `{}`.
- `json_encode(10.0)` is `10`; `JSON_PRESERVE_ZERO_FRACTION` keeps `10.0` for a typed consumer.
- Before encoding a list, `array_is_list($rows)` proves it will be a JSON array.
