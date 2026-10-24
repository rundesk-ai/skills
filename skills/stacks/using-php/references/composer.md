# Composer, autoloading and layout

Read this before adding or upgrading a dependency, editing `composer.json`, changing namespaces or
directories, or building for production.

## Resolve for production's PHP

The `require.php` range does not stop the solver choosing package versions that need the developer's
PHP. A lock made on 8.4 for a range of `>=8.2` picked a dependency release that needs 8.4, and the
generated `vendor/composer/platform_check.php` then throws on the 8.3 server at the first request.

```sh
composer config platform.php 8.3.0      # production's version
composer update --lock                  # re-resolve without upgrading anything else
composer check-platform-reqs --lock     # run on the target host: checks that PHP against the lock
```

`check-platform-reqs` checks the PHP that runs it, so run it where the code will run.

## Change the lock deliberately

- `composer require vendor/pkg` or `composer update vendor/pkg` changes one package. A bare
  `composer update` upgrades everything the constraints allow, which turns a one-package fix into a
  forty-package change.
- `composer.json` edited by hand without updating the lock makes `composer install` fail (exit 4: "The
  lock file is not up to date"). `composer validate --no-check-publish` catches it in CI (exit 2); without
  `--no-check-publish` it also fails an application for fields only a published package needs.
- On a lock merge conflict, take one side's lock and re-run the `composer require` or `update` that the
  other side made.
- Commit the lock for an application. For a library it has no effect on consumers; test the library with
  `composer update --prefer-lowest` as well.

## Advisories

- `composer update` and `require` refuse versions with known advisories (Composer 2.9 and later). On 2.10
  the setting is `policy.advisories`; the older `audit.block-insecure` is deprecated, and ignored once
  `policy.advisories` exists. When something is blocked, ignore the one advisory id with a reason, never
  the whole package or the feature.
- `composer install` from a lock neither blocks nor warns; a vulnerable lock installs with exit 0. Add a
  CI step: `composer audit --locked` exits 1 on an advisory and, by default, on an abandoned package.
- `composer why vendor/pkg` names who pulled a package in; `composer why-not vendor/pkg 2.0` names what
  blocks an upgrade.

## Code that runs on install

- Plugins run code on every Composer command. Since 2.2 only packages listed in `allow-plugins` load; in a
  non-interactive run an unlisted plugin is skipped with no message (only `-vvv` shows it), so a
  code-generating plugin that works on a laptop silently does nothing in CI. List each plugin by name;
  never set `"allow-plugins": true`.
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
- One class per file: a second class in a file loads only if the first one happened to be loaded,
  an order-dependent bug.
- Production install: `composer install --no-dev --prefer-dist --optimize-autoloader --classmap-authoritative`.
  The authoritative classmap changes behaviour as well as speed: a class missing from the map is not found
  even if its file exists.

## Style

Follow the project's existing formatter configuration and do not reformat unrelated files. Where none
exists, PER Coding Style (the successor to PSR-12) is the common one; `php-cs-fixer fix --dry-run --diff`
proves a change conforms without rewriting anything.
