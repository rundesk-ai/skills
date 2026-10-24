# PHP source basis

The evidence behind the claims in this skill. Status: **observed** means reproduced on PHP 8.4.15 and
Composer 2.10.2 (October 2026), with 8.3.28 and 7.4.33 binaries for comparisons; **documented** means a
primary source; **community** means a widely cited write-up. Measured numbers are single-machine runs on
arm64 macOS with OPcache off unless stated; read them as ratios.

## Comparisons, types and errors

| Claim | Status | Source |
|---|---|---|
| PHP 8 compares a number and a non-numeric string as strings; numeric strings still compare numerically | observed, documented | [Saner string to number comparisons RFC](https://wiki.php.net/rfc/string_to_number_comparison), [PHP 8.0 incompatible changes](https://www.php.net/manual/en/migration80.incompatible.php) |
| Magic hashes (`md5('240610708') == md5('QNKCDZO')`) and `true == 'string'` | observed | [OWASP: PHP magic tricks, type juggling](https://owasp.org/www-pdf-archive/PHPMagicTricks-TypeJuggling.pdf) |
| `in_array`, `array_search`, `array_keys`, `switch` are loose; `match` is strict | observed | [match](https://www.php.net/manual/en/control-structures.match.php) |
| Strict types: calling file decides, return types by declaring file, callbacks from internal functions coerced | observed, documented | [Strict typing](https://www.php.net/manual/en/language.types.declarations.php#language.types.declarations.strict) |
| Operators and numeric strings: `"1 apple"` warns, `"apple"` throws | observed | [Saner numeric strings RFC](https://wiki.php.net/rfc/saner-numeric-strings) |
| Numeric-string array keys become ints; float keys deprecated | observed, documented | [Arrays](https://www.php.net/manual/en/language.types.array.php), [Implicit float to int deprecation RFC](https://wiki.php.net/rfc/implicit-float-int-deprecate) |
| Stable sorting since 8.0; bool comparators deprecated | observed, documented | [Stable sorting RFC](https://wiki.php.net/rfc/stable_sorting) |
| `@` does not stop exceptions or custom handlers | observed, documented | [Error control operator](https://www.php.net/manual/en/language.operators.errorcontrol.php) |
| Implicitly nullable parameters deprecated in 8.4 | observed | [RFC](https://wiki.php.net/rfc/deprecate-implicitly-nullable-types) |
| Dynamic properties deprecated in 8.2 | observed | [RFC](https://wiki.php.net/rfc/deprecate_dynamic_properties) |
| `round()` changes in 8.4 | observed (8.3 against 8.4), documented | [8.4 other changes](https://www.php.net/manual/en/migration84.other-changes.php), [php-src issue 12143](https://github.com/php/php-src/issues/12143) |
| 8.5 warnings and new syntax | documented, not run | [PHP 8.5 release](https://www.php.net/releases/8.5/en.php), [8.5 incompatible changes](https://www.php.net/manual/en/migration85.incompatible.php) |

## Data and dates

| Claim | Status | Source |
|---|---|---|
| `foreach` by reference corrupts a later by-value loop | observed, documented | [foreach](https://www.php.net/manual/en/control-structures.foreach.php) |
| Copy-on-write: a 1M-int array costs nothing to assign until written (16 MB on write) | observed | `memory_get_usage()` deltas |
| `array_filter` keeps keys, so `json_encode` emits an object | observed | [array_is_list](https://www.php.net/manual/en/function.array-is-list.php) |
| Float to int truncation, silent int overflow and wrapping casts, exponent notation in string conversion | observed | [Integers](https://www.php.net/manual/en/language.types.integer.php), [Floats](https://www.php.net/manual/en/language.types.float.php) |
| bcmath truncates; `bcround` and `BcMath\Number` in 8.4 | observed | [BcMath object RFC](https://wiki.php.net/rfc/support_object_type_in_bcmath) |
| Byte functions split UTF-8; `json_encode` returns `false`, `preg_*` returns `null`; `mb_trim` in 8.4 | observed | [mb_trim RFC](https://wiki.php.net/rfc/mb_trim) |
| Case functions ignore the locale since 8.2 | observed, documented | [RFC](https://wiki.php.net/rfc/strtolower-ascii) |
| `DateTime::modify` mutates; `+1 month` overflows; `createFromFormat` without `!` uses the current time and rolls impossible dates | observed, documented | [createFromFormat](https://www.php.net/manual/en/datetime.createfromformat.php) |
| Relative hour arithmetic across a DST change is off by an hour; `DateInterval('PT24H')` is correct | observed on 8.4.15 | community reports [54799](https://bugs.php.net/bug.php?id=54799), [51051](https://bugs.php.net/bug.php?id=51051), [75167](https://bugs.php.net/75167) |
| No warning without a configured time zone; default UTC | observed with `php -n` | |

## Security

| Claim | Status | Source |
|---|---|---|
| Bcrypt default cost 12 in 8.4; 72-byte truncation; NUL bytes throw | observed, documented | [password_hash](https://www.php.net/manual/en/function.password-hash.php), [Password FAQ](https://www.php.net/manual/en/faq.passwords.php), [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) |
| `password_needs_rehash` with a different algorithm downgrades argon2id | observed | |
| `hash_equals` argument order and types | observed, documented | [hash_equals](https://www.php.net/manual/en/function.hash-equals.php) |
| `mt_rand` and `uniqid` are predictable | observed | community: [php_mt_seed](https://github.com/openwall/php_mt_seed) |
| `unserialize` runs magic methods; `allowed_classes` is not a boundary; gadget chains | observed, documented | [unserialize](https://www.php.net/manual/en/function.unserialize.php), community: [phpggc](https://github.com/ambionics/phpggc) |
| Phar metadata no longer unserialized on stream access; `getMetadata()` still does | observed, documented | [PHP 8.0 incompatible changes](https://www.php.net/manual/en/migration80.incompatible.php) |
| PDO exceptions by default; identifiers cannot bind; `exec` runs stacked statements; LIKE and IN behaviour | observed (sqlite) | [PDO MySQL](https://www.php.net/manual/en/ref.pdo-mysql.php) |
| MySQL emulated prepares by default; charset belongs in the DSN | documented, community; not run | [PDO MySQL](https://www.php.net/manual/en/ref.pdo-mysql.php), [canonical answer on PDO and injection](https://stackoverflow.com/questions/134099/are-pdo-prepared-statements-sufficient-to-prevent-sql-injection) |
| `include` executes PHP in any file; realpath sibling-prefix bypass; `basename` edge cases | observed | |
| Polyglot uploads pass `finfo` and `getimagesize` | observed | [OWASP File Upload](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) |
| `escapeshellarg` does not stop option injection; `proc_open` with an array runs no shell | observed, documented | [proc_open](https://www.php.net/manual/en/function.proc-open.php), community: [Composer argument injection write-up](https://sonarsource.com/blog/php-supply-chain-attack-on-composer/) |
| `mail()` string headers accept CRLF; array headers throw; `header()` warns and drops | observed | |
| `htmlspecialchars` 8.1 defaults; explicit flags return `""` on invalid UTF-8; context escaping | observed, documented | [htmlspecialchars](https://www.php.net/manual/en/function.htmlspecialchars.php), [OWASP XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) |
| Session defaults accept a chosen id and omit cookie flags | observed (built-in server, `php -n`) | [OWASP PHP Configuration](https://cheatsheetseries.owasp.org/cheatsheets/PHP_Configuration_Cheat_Sheet.html) |
| `file_get_contents` wrappers and redirects (20 by default) enable SSRF | observed, documented | [HTTP context options](https://www.php.net/manual/en/context.http.php), [OWASP SSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) |
| XXE off by default; `LIBXML_NOENT` re-enables it | observed (libxml 2.12), documented | [libxml_disable_entity_loader](https://www.php.net/manual/en/function.libxml-disable-entity-loader.php), [OWASP XXE Prevention](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html#php) |
| Exposed `vendor/` is exploited in the wild | community | [CVE-2017-9841](https://nvd.nist.gov/vuln/detail/CVE-2017-9841) |

## Composer and layout

| Claim | Status | Source |
|---|---|---|
| Lock resolved for local PHP fails in `platform_check.php`; `config.platform.php` fixes it | observed | [platform](https://getcomposer.org/doc/06-config.md#platform) |
| Advisory blocking on update since 2.9; `policy` config in 2.10; install does not audit | observed, documented | [Composer 2.9](https://blog.packagist.com/composer-2-9/), [Composer 2.10.0 release](https://github.com/composer/composer/releases/tag/2.10.0), [policy](https://getcomposer.org/doc/06-config.md#policy) |
| Stale lock: install exit 4, validate exit 2 | observed | [Resolving merge conflicts](https://getcomposer.org/doc/articles/resolving-merge-conflicts.md) |
| Non-interactive runs skip unlisted plugins silently; root scripts run on install | observed, documented | [allow-plugins](https://getcomposer.org/doc/06-config.md#allow-plugins), [Scripts](https://getcomposer.org/doc/articles/scripts.md) |
| Constraint meanings, `minimum-stability` | observed (composer/semver), documented | [minimum-stability](https://getcomposer.org/doc/04-schema.md#minimum-stability) |
| Lock files for applications, not libraries | documented | [Libraries: lock file](https://getcomposer.org/doc/02-libraries.md#lock-file) |
| PSR-4 case mismatch: `--strict-psr` exits 1, authoritative classmap misses the class on macOS | observed | [Autoloader optimization](https://getcomposer.org/doc/articles/autoloader-optimization.md) |
| `strict_types` placement is fatal when not first | observed | |
| PER Coding Style supersedes PSR-12 | documented | [PER Coding Style](https://www.php-fig.org/per/coding-style/), [php-cs-fixer PER-CS](https://cs.symfony.com/doc/ruleSets/PER-CS.html) |
| Supply-chain incidents on Packagist | community | [Packagist maintainer account takeover](https://blog.packagist.com/packagist-org-maintainer-account-takeover/) |

## Tooling, versions and performance

| Claim | Status | Source |
|---|---|---|
| Supported versions and their end dates | documented | [Supported versions](https://www.php.net/supported-versions.php) |
| `php -l` on an old binary catches syntax, not functions; PHPStan `phpVersion` catches functions, ignores the `require.php` range | observed (8.3 binary, PHPStan 2.3.1) | [PHPStan config reference](https://phpstan.org/config-reference) |
| Strictest PHPStan misses loose comparisons; phpstan-strict-rules reports them | observed | [phpstan-strict-rules](https://github.com/phpstan/phpstan-strict-rules), [rule levels](https://phpstan.org/user-guide/rule-levels) |
| Rector PHP sets fix implicit nullable, not loose comparisons | observed (Rector 2.7.0) | [Rector documentation](https://getrector.com/documentation) |
| `array_merge` in a loop is quadratic; `in_array` against a flipped set; generators against arrays; namespaced `array_key_exists` | observed (`hrtime`, `memory_get_peak_usage`) | |
| `.=` is not slower than `implode` | observed | |
| Static caches grow in workers; `WeakMap` releases; cycle collector | observed | [WeakMap](https://www.php.net/manual/en/class.weakmap.php) |
| OPcache off on CLI; JIT disabled by default; JIT gains on numeric loops only | observed, documented | [JIT config defaults RFC](https://wiki.php.net/rfc/jit_config_defaults) |

## Judgments not stated by the sources

- Computing each renewal from the anchor date and a count, rather than from the previous renewal, is the
  skill's own rule for "same day next month".
- Choosing between moving legacy hashes on next login and wrapping them is a trade-off the skill states;
  OWASP describes both.
