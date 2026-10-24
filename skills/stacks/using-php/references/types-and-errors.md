# Types and errors

Read this when a value changes type on its way through the code, when strict types does not behave as
expected, or when a failure is a warning that carried on instead of an exception.

## Loose comparison after PHP 8

PHP 8 compares a number with a non-numeric string as strings, so `0 == "a"` and `in_array('abc', [0])`
became false. Everything involving two numeric strings, booleans or `null` still juggles:

```php
var_dump("1" == "01", "10" == "1e1", "1e3" == "1000", " 1" == 1, "0.0" == "0"); // all true
var_dump(in_array(null, [0]), in_array('a', [true]), in_array('1e1', ['10']));  // all true
var_dump(array_search('1', [0, '01', '1']));                                    // int(1): matched "01"
```

Tokens, phone numbers, postcodes and digests are numeric strings often enough to matter. `match` is
strict; `switch` and `sort` without a flag are not. `sort()` on mixed types has no total order:
`['b', 'a', '10', '9']` sorts to `9, 10, a, b` by default and `10, 9, a, b` with `SORT_STRING`, so pass a
flag or a `<=>` comparator. A comparator returning a bool still works but is deprecated.

Enums compare silently false against their backing value: `Status::Active == 'active'` and
`in_array('active', [Status::Active])` are both false. Compare `->value`, or turn input into an enum with
`tryFrom` first. A pure (unbacked) enum makes `json_encode` return `false`.

## What strict types covers

| Situation | Strict file | Proof |
|---|---|---|
| A call made from the strict file | arguments are not coerced: `strlen(123)` throws | `TypeError` |
| A function declared in a strict file, called from a non-strict file | the caller's mode wins: `"5"` arrives as `5` | no error |
| A return value | checked by the declaring file's mode | strict `fn(): int { return "5"; }` throws |
| A callback invoked by an internal function (`array_map`, `usort`) | coerced, because the engine is the caller | `array_map(fn (int $i) => $i, ['4'])` gives `[4]` |
| Operators | unaffected: `1 + "1"` is `2`; `1 + "1 apple"` is `2` with a warning; `1 + "apple"` throws | |
| `int` to `float` | still widened | |

The declaration must be the first statement. A namespace before it, or a single space before `<?php`
(which is output), is a fatal error at load time, so a whitespace slip ships as a deploy failure.

## Casts never fail; validation does

`(int)"12abc"` is 12, `(int)"abc"` is 0, `(int)"0x1A"` is 0, `(int)"9999999999999999999"` is
`PHP_INT_MAX`. A non-strict `int` parameter rejects `"12abc"` with a `TypeError` but accepts `" 5"` and
`"1e3"`. To accept a number from outside, validate it:

```php
$qty = filter_var($input, FILTER_VALIDATE_INT, ['options' => ['min_range' => 1]]);
if ($qty === false) {
    throw new InvalidArgumentException('quantity must be a positive integer');
}
```

`ctype_digit()` on an int is deprecated and reads small ints as character codes; pass it strings only.

## Warnings that carry on

An undefined array key or variable is a warning that yields `null`, and execution continues with the
wrong value. Internal functions throw `TypeError` and `ValueError` for bad arguments, but passing `null`
to a non-nullable internal parameter is only deprecated and still returns a value (`strlen(null)` is 0).

The `@` operator does not stop exceptions, and it does not stop a custom error handler: a handler that
converts warnings to `ErrorException` throws inside `@`-suppressed code unless it checks the reporting
level first.

```php
set_error_handler(function (int $errno, string $message, string $file, int $line): bool {
    if (!(error_reporting() & $errno)) {
        return false; // suppressed with @, or below the reporting level
    }
    throw new ErrorException($message, 0, $errno, $file, $line);
});
```

Prefer checking return values (`false`, `null`) over `@`. Several functions report failure only that
way: `json_encode` returns `false` on invalid UTF-8, `preg_replace` returns `null`, `file_get_contents`
returns `false`.

`assert()` is compiled out in production (`zend.assertions=-1`), and a string passed to it is no longer
evaluated, so `assert('$x > 0')` always passes. Never validate input with `assert`.

## Deprecations that change correct code

| Since | Deprecated or changed | Symptom |
|---|---|---|
| 8.1 | `null` to a non-nullable internal parameter; float to int with precision loss | `Deprecated:` notices, later errors |
| 8.2 | dynamic properties (`$obj->typo = 1`) unless the class has `#[AllowDynamicProperties]` | a typo'd property is now a notice instead of a silent new field |
| 8.4 | implicitly nullable parameters (`function f(Type $x = null)`) | reported at compile time; `php -l` shows it |
| 8.4 | `round()` edge cases: `round(0.49999999999999994)` is 1 on 8.3 and 0 on 8.4; an invalid mode throws | rounding tests change |
| 8.5 | out-of-range float to int casts, `NAN` casts and destructuring a non-array warn; `null` as an array offset is deprecated | new warnings in logs |

Read readonly properties as "assigned once", not "deep immutable": an object held in one is still
mutable, and appending to a readonly array throws `Cannot indirectly modify readonly property`.
