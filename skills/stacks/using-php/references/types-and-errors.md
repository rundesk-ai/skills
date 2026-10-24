# Types and errors

Read this when a value changes type on its way through the code, when strict types does not behave as
expected, or when a failure is a warning that carried on instead of an exception.

## Loose comparison after PHP 8

Everything involving two numeric strings, booleans or `null` still juggles:

```php
var_dump("1" == "01", "10" == "1e1", "1e3" == "1000", " 1" == 1, "0.0" == "0"); // all true
var_dump(in_array(null, [0]), in_array('a', [true]), in_array('1e1', ['10']));  // all true
var_dump(array_search('1', [0, '01', '1']));                                    // int(1): matched "01"
```

`sort()` on mixed types has no total order: `['b', 'a', '10', '9']` sorts to `9, 10, a, b` by default and
`10, 9, a, b` with `SORT_STRING`, so pass a flag or a `<=>` comparator.

Enums compare silently false against their backing value: `Status::Active == 'active'` and
`in_array('active', [Status::Active])` are both false. Compare `->value`, or turn input into an enum with
`tryFrom` first. A pure (unbacked) enum makes `json_encode` return `false`.

## Strict types beyond the basics

- A return value is checked by the declaring file's mode: a strict `function f(): int { return "5"; }`
  throws even when called from a non-strict file.
- Operators ignore strict types: `1 + "1"` is `2`; `1 + "1 apple"` is `2` with a warning; `1 + "apple"`
  throws `TypeError`.
- `int` still widens to `float`.
- The declaration must be the first statement. A namespace before it, or a single space before `<?php`
  (which is output), is a fatal error at load time, so a whitespace slip ships as a deploy failure.

## Casts

Beyond `(int)"12abc"`: `(int)"0x1A"` is 0 and `(int)"9999999999999999999"` is `PHP_INT_MAX`. A
non-strict `int` parameter rejects `"12abc"` with a `TypeError` but accepts `" 5"` and `"1e3"`.
`ctype_digit()` on an int is deprecated and reads small ints as character codes; pass it strings only.

## Warnings that carry on

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

`assert()` is compiled out in production (`zend.assertions=-1`), and since 8.0 a string passed to it is
not evaluated, so an old `assert('$x > 0')` always passes. Never validate input with `assert`.

## Deprecations that change correct code

| Since | Change | Symptom |
|---|---|---|
| 8.1 | passing `null` to a non-nullable internal parameter is deprecated and still returns a value (`strlen(null)` is 0) | `Deprecated:` notices now, errors later |
| 8.4 | implicitly nullable parameters (`function f(Type $x = null)`) | reported at compile time; `php -l` shows it |
| 8.4 | `round()` edge cases: `round(0.49999999999999994)` is 1 on 8.3 and 0 on 8.4; an invalid mode throws | rounding tests change |
| 8.5 | out-of-range float to int casts, `NAN` casts and destructuring a non-array warn; `null` as an array offset is deprecated | new warnings in logs |

A readonly property is assigned once, not deeply immutable: an object held in one is still mutable, and
appending to a readonly array throws `Cannot indirectly modify readonly property`.
