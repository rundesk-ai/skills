# Versions and tooling

Read this before an upgrade, before using a function or syntax newer than the lowest version the code
must run on, or when choosing the checks that prove a change. Deprecations and behaviour changes per
version are in [Types and errors](types-and-errors.md).

## Prove a change runs on the lowest target

`php -l` with the lowest supported binary catches newer syntax, not newer functions: on 8.3,
`array_find()` lints clean and fails at run time. PHPStan with `phpVersion` set catches the functions but
not the syntax. Run both.

```sh
php8.3 -l src/Billing.php                # syntax, per file, with the oldest binary you support
vendor/bin/phpstan analyse               # phpstan.neon: parameters: phpVersion: 80300
```

PHPStan reads `config.platform.php` from `composer.json` but not the `require.php` range, so a project
with only a range is analysed for the PHP running PHPStan. Set `phpVersion` explicitly.

Code using 8.5 syntax (the pipe operator `|>`, `clone($object, [...])`) does not parse on 8.4. `str_split('')`
returns `[]` from 8.2, where it used to return `['']`.

## Upgrading

Rector with `withPhpSets(php84: true)` applies the mechanical fixes (explicit nullable types,
`isset() ?:` to `??`). Run it as a dry run and read the diff before applying; it leaves loose comparisons
alone. Then run the suite with every notice visible and make the `Deprecated:` lines zero: today's
deprecation is the next version's error.

## Read the configuration that actually runs

The command line and the web server (FPM) load different ini files, so check the one that serves
requests (`php-fpm -i`, or `phpinfo()` behind authentication) before concluding a setting is on.
