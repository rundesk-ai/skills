---
name: using-php
description: Use when writing, reviewing, debugging, upgrading, or securing PHP outside a framework's own APIs — a plain PHP application or script, a Composer package, a CMS plugin, or the language underneath a framework — including loose comparison and type juggling, strict types, arrays and references, dates, money, UTF-8 and JSON, errors and deprecations across PHP 8 versions, password hashing, PDO queries, deserialization, file inclusion, uploads and shell calls, sessions, Composer dependencies and autoloading, and memory in long-running workers. It supplies PHP defaults, the failure each one prevents, and command-line proof. Do not use it for Laravel framework behavior such as routing, Eloquent, queues or Blade.
---

# Use PHP

Make every comparison strict, every date immutable, and every value from outside checked where it
enters. PHP's defaults coerce quietly, so the first symptom is a wrong row or an open door, not an error.

## Establish the target before changing code

```sh
php -v && php --ini && php -m
grep -n -A3 -E '"php"|"platform"' composer.json
```

- `require.php` in `composer.json` is a range, not the version the code runs on. `config.platform.php`
  is what the lock was resolved for, and production's `php -v` is the truth. Code that passes on a local
  8.4 fails on an 8.3 server with a parse error (`new Foo()->bar()`) or an undefined function
  (`array_find`).
- `php --ini` names the ini files loaded; a host ini can hide deprecations or raise `memory_limit`. Run
  with `php -n` when a result must not depend on the machine, and with
  `-d error_reporting=-1 -d display_errors=1` to see every deprecation.
- Read [Versions and tooling](references/versions-and-tooling.md) before an upgrade, or before using a
  function newer than the lowest version the code must run on.

## Comparisons coerce: make them strict

PHP 8 stopped `0 == "a"` from being true. Two numeric strings still compare as numbers, and the loose
defaults below are unchanged.

| Code | What happens | Instead |
|---|---|---|
| `$a == $b` on numeric strings | `"1e3" == "1000"` is true, and so is `md5('240610708') == md5('QNKCDZO')`: both digests are `0e` followed by digits | `===`; `hash_equals($known, $given)` for anything secret |
| `true == "any string"` | true, so a JSON body `{"token": true}` passes a loose token check | check that decoded fields are strings, then compare strictly |
| `in_array`, `array_search`, `array_keys($a, $v)` | loose: `in_array(true, ['admin'])` is true | pass `true` as the strict argument |
| `switch` | loose | `match`, which is strict and throws `UnhandledMatchError` when no arm matches |
| `if (strpos($s, $x))` | a match at offset 0 reads as not found | `str_contains`, and reject an empty needle: `str_contains($s, '')` is true |
| `empty($qty)`, `$qty ?: 1` | the string `"0"` is empty | compare with `''` or `null` |
| `isset($a['k'])` | false when the key holds `null` | `array_key_exists` when null means something |
| `(int)"12abc"` | 12, silently; `(int)"abc"` is 0 | `filter_var($s, FILTER_VALIDATE_INT)`, and handle `false` |

`declare(strict_types=1)` governs calls made from the file that declares it, and the return values of
functions declared there. It does not reach callers in other files, callbacks the engine invokes
(`array_map(fn (int $i) => $i, ['4'])` still coerces), or operators. Declare it first in every file and
still validate input. Read [Types and errors](references/types-and-errors.md) for casts, enums,
warnings and the error handler.

## Security defaults

Each row runs correctly until someone sends a hostile value. Read [Security](references/security.md)
before touching authentication, sessions, SQL, uploads, file paths, shell calls, XML, or outbound URLs.

| Work | Default that fails | Do |
|---|---|---|
| Passwords | `md5` or `sha1`, compared with `==` | `password_hash($pw, PASSWORD_DEFAULT)` and `password_verify`; `password_needs_rehash` with the same algorithm; move legacy hashes over on the next successful login rather than forcing resets |
| Secrets and tokens | `==` or `strcmp`; `uniqid`, `mt_rand`, `rand` | `hash_equals`; `random_bytes`, `random_int` |
| Data a client can send back | `unserialize`, which instantiates any class and runs its magic methods; `allowed_classes` is not a security boundary | `json_decode($s, true, flags: JSON_THROW_ON_ERROR)`, signed with `hash_hmac` when it must round-trip |
| SQL | values or identifiers concatenated into the query | bound parameters for values; an allow-list for column names and `ASC`/`DESC`, since an identifier cannot be bound (binding one sorts by a constant, silently) |
| Includes and paths | `include $dir . $_GET['page']`; `str_starts_with(realpath($p), $base)` | an allow-list of pages; containment checked against `$base . DIRECTORY_SEPARATOR`, rejecting `realpath() === false` |
| Shell | a command string, even with `escapeshellarg`, which stops injection but not a `-option` | `proc_open([...])` with an argument array, which runs no shell, and `--` before user operands |
| Sessions | `use_strict_mode=0` and `httponly` off: an attacker-chosen session id is accepted | strict mode and secure cookie flags; `session_regenerate_id(true)` on login and privilege change |
| HTML | explicit flags to `htmlspecialchars` drop `ENT_SUBSTITUTE`, so invalid UTF-8 renders as an empty string | the default flags; quote every attribute; allow-list URL schemes in `href` |

## Data traps that never throw

- **`foreach ($rows as &$row)` leaves `$row` bound to the last element.** A later
  `foreach ($rows as $row)` writes each row into it: the last row is lost and the one before it appears
  twice. `unset($row)` straight after the loop, or write by key.
- **`array_filter`, `array_unique` and `unset` keep keys**, so `json_encode` emits an object
  (`{"0":1,"2":3}`) where the client expected a list. `array_values` before encoding.
- **Numeric-string keys become ints.** `array_merge` renumbers an id-keyed map (use `+` or
  `array_replace`), and a key read back and passed to a `string` parameter throws under strict types.
- **`DateTime::modify()` mutates and returns the same object**: `$end = $start->modify('+1 day')`
  moves `$start` too. Type dates as `DateTimeImmutable`.
- **`'+1 month'` overflows**: 31 January becomes 3 March. Clamp to the month's last day yourself and keep
  the anchor day for the month after.
- **Money in floats**: `(int)(19.99 * 100)` is `1998`. Integer minor units; `bcmath` truncates to the
  scale rather than rounding (`bcround`, from 8.4, rounds).
- **`json_decode` returns `null` for invalid input and for `"null"` alike**, and turns ids above 2^53 into
  floats: `JSON_THROW_ON_ERROR`, `JSON_BIGINT_AS_STRING`.
- **`strlen`, `substr` and `strtolower` work on bytes.** A cut UTF-8 string makes `json_encode` return
  `false` and `preg_replace` return `null`, silently. `mb_*`, the `/u` regex flag, `JSON_THROW_ON_ERROR`.

Read [Data](references/data.md) for numbers, strings and JSON, and [Dates](references/dates.md) for
parsing, time zones and daylight saving.

## Composer decides what runs in production

- Set `config.platform.php` to production's version. Without it the lock can pick packages that need the
  local PHP, and the deploy fails on its first request in `vendor/composer/platform_check.php`.
- `composer install` never checks advisories; only `update` and `require` can block a vulnerable
  version. Run `composer audit --locked` as its own CI step.
- A PSR-4 case mismatch works on macOS and fails on Linux; `composer dump-autoload --optimize --strict-psr`
  exits non-zero on it locally.

Read [Composer](references/composer.md) before adding a dependency, changing autoloading, or building
for production.

## Long-running PHP keeps state

Under a queue worker or an application server that keeps workers alive (Swoole, RoadRunner, FrankenPHP
worker mode), one process serves many jobs. A `static` or global cache grows without end (about 16 MB per
10,000 cached 1 KB entries, measured), and state set for one request is still there for the next. Bound
or reset caches per job, use a `WeakMap` for per-object data, and restart workers after a fixed number of
jobs. Read [Performance and memory](references/performance-and-memory.md) before optimizing anything.

## Prove it

```sh
php -l src/File.php                                       # with the lowest PHP the code must run on
php -d error_reporting=-1 -d display_errors=1 vendor/bin/phpunit
vendor/bin/phpstan analyse                                # with phpVersion set explicitly
composer validate --no-check-publish && composer audit --locked
```

PHPStan at its strictest level flags none of the loose comparisons above; the phpstan-strict-rules
package does. Report the behaviour, the file, and the command whose output proves it.
[Sources](references/sources.md) holds the evidence behind each rule.
