# Composer, autoloading and layout

Read this before adding or upgrading a dependency, editing `composer.json`, changing namespaces or
directories, or building for production.

## Resolve for production's PHP

A lock made on 8.4 for a range of `>=8.2` picked a dependency release that needs 8.4, and the generated
`vendor/composer/platform_check.php` then throws on the 8.3 server at the first request.

```sh
composer config platform.php 8.3.0         # production's version
composer update --minimal-changes          # re-resolve, changing only what the platform forces
composer check-platform-reqs --lock        # on the target host: checks that PHP against the lock
```

`composer update --lock` does not help here: it keeps every locked version, so the solver fails.
`check-platform-reqs` checks the PHP that runs it, so run it where the code will run.

## Change the lock deliberately

- `composer require vendor/pkg` or `composer update vendor/pkg` changes one package. A bare
  `composer update` upgrades everything the constraints allow, which turns a one-package fix into a
  forty-package change.
- A `composer.json` edited by hand without updating the lock fails `composer install` (exit 4) only when a
  required package is missing from the lock; a changed constraint the locked version still satisfies just
  warns and exits 0. `composer validate --no-check-publish` exits 2 in both cases, so it is the CI gate;
  without `--no-check-publish` it also fails an application for fields only a published package needs.
- On a lock merge conflict, take one side's lock and re-run the `composer require` or `update` that the
  other side made.
- Commit the lock for an application. For a library it has no effect on consumers; test the library with
  `composer update --prefer-lowest` as well.

## Advisories

- `composer update` and `require` refuse versions with known advisories (Composer 2.9 and later). On 2.10
  the setting is `policy.advisories`; the older `audit.block-insecure` is deprecated, and ignored once
  `policy.advisories` exists. When something is blocked, ignore the one advisory id with a reason, never
  the whole package or the feature.
- `composer audit --locked` exits 1 on an advisory and, by default, on an abandoned package.

## Code that runs on install

- Plugins run code on every Composer command. Since 2.2 only packages listed in `allow-plugins` load: in
  a non-interactive run an unlisted plugin fails the command ("blocked by your allow-plugins config"),
  while one listed as `false`, or one that marks itself optional, is skipped without a word. List each
  plugin by name after reading what it does; never set `"allow-plugins": true`.
- The root package's `scripts` run on `composer install`; a pull request that changes `scripts` or
  `allow-plugins` is code that runs on every developer's machine and in CI. Review it as code. Install an
  untrusted repository with `--no-scripts --no-plugins`.

## Constraints

`^1.2` allows anything below 2.0, but `^0.3` allows only 0.3.x and `^0.0.3` only 0.0.3, because before
1.0 the minor version is treated as breaking. `>=1.0` and `*` accept every future major. Lowering
`minimum-stability` to `dev` without `"prefer-stable": true` pulls development branches of every
dependency.

## Autoloading follows the file system

- PSR-4 maps the namespace to the directory, case included. On macOS the file system ignores case, so
  `App\Models\User` in `src/models/User.php` loads in development and fails in production on Linux.
  `composer dump-autoload --optimize --strict-psr` reports it and exits non-zero locally, and
  `--classmap-authoritative` reproduces the failure on macOS. To rename a directory by case only:
  `git mv src/models src/tmp && git mv src/tmp src/Models`.
- Production install: `composer install --no-dev --prefer-dist --optimize-autoloader --classmap-authoritative`.
  The authoritative classmap changes behaviour as well as speed: a class missing from the map is not found
  even if its file exists.
