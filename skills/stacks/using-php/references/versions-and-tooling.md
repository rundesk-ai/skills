# Versions and tooling

Read this before an upgrade, before using a function or syntax newer than the lowest version the code
must run on, or when choosing the checks that prove a change.

## Which versions are alive

Check https://www.php.net/supported-versions.php at the time of the work rather than trusting a list
here. Each branch gets two years of active support and two more of security fixes; a project on an
end-of-life branch gets no security patches, which is worth saying in a review.

## What changed correct code

The deprecations and behaviour changes per version are in [Types and errors](types-and-errors.md). Those
that silently change a result rather than warning:

- 8.0: a number compared with a non-numeric string compares as strings; sorting became stable; PDO
  throws by default; `assert()` stopped evaluating strings.
- 8.1: `htmlspecialchars` defaults include single quotes and `ENT_SUBSTITUTE`.
- 8.2: `strtolower` and friends ignore the locale; `str_split('')` returns `[]`.
- 8.4: `round()` edge cases; bcrypt's default cost rose to 12.
- 8.5 adds the pipe operator `|>`, `clone($object, [...])`, `#[\NoDiscard]` and a built-in URI
  extension; code using them does not parse on 8.4.

## Prove a change runs on the lowest target

`php -l` with the lowest supported binary catches newer syntax, not newer functions: on 8.3,
`new Foo()->bar()` is a parse error, while `array_find()` lints clean and fails at run time. PHPStan with
`phpVersion` set catches the functions but not the syntax. Run both.

```sh
php8.3 -l src/Billing.php                # syntax, per file, with the oldest binary you support
vendor/bin/phpstan analyse               # phpstan.neon: parameters: phpVersion: 80300
```

PHPStan reads `config.platform.php` from `composer.json` but not the `require.php` range, so a project
with only a range is analysed for the PHP running PHPStan. Set `phpVersion` explicitly.

## What static analysis catches

PHPStan at its strictest level reports no loose `==`, no `in_array` without the strict flag, and no
`if (strpos(...))`. The phpstan-strict-rules package adds those. Neither catches a mutable `DateTime`
shared between two variables, or money held in floats: those need a test.

## Upgrading

1. Read the migration guide for every version crossed (php.net "Migrating from PHP x.y").
2. Run the suite with every notice visible:
   `php -d error_reporting=-1 -d display_errors=1 vendor/bin/phpunit`, and make the `Deprecated:` lines
   zero; today's deprecation is the next version's error.
3. Rector with `withPhpSets(php84: true)` applies the mechanical fixes (explicit nullable types,
   `isset() ?:` to `??`) as a dry run you read before applying. It leaves loose comparisons alone.
4. Update `config.platform.php` and re-resolve the lock (see [Composer](composer.md)).

## Read the configuration that actually runs

`php --ini` names the loaded ini files, `php -m` the extensions, `php -i | grep <setting>` a value. The
command line and the web server (FPM) load different ini files, so check the one that serves requests.
OPcache is off on the command line by default; see [Performance and memory](performance-and-memory.md).
