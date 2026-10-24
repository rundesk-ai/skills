# Security

Read this before changing authentication, sessions, SQL, file handling, uploads, shell calls, XML
parsing, outbound requests or output escaping. Each section names the default that fails and the proof
that the fix holds; write that proof as a test that fails on the old code.

## Passwords

- `password_hash($pw, PASSWORD_DEFAULT)` is bcrypt; PHP 8.4 raised its default cost from 10 to 12, about
  four times slower (190 ms against 47 ms per hash on one machine). That is login latency and a
  denial-of-service budget: rate-limit the login.
- `password_needs_rehash($hash, PASSWORD_DEFAULT)` is true for old cost-10 hashes after an upgrade, so
  rehash on the next successful login. Pass the same algorithm you hash with: an application hashing
  with `PASSWORD_ARGON2ID` that checks against `PASSWORD_DEFAULT` silently converts every hash back to
  bcrypt. Argon2id exists only if the build has it; check `defined('PASSWORD_ARGON2ID')` on the server.
- Bcrypt truncates input at 72 bytes without warning, so two long passphrases sharing a prefix both
  verify; a NUL byte throws `ValueError`. Pre-hashing with raw binary output therefore fails for some
  passwords; encode it: `password_hash(base64_encode(hash_hmac('sha384', $pw, $pepper, true)), PASSWORD_DEFAULT)`.
- Migrating from `md5`/`sha1` without locking anyone out: on login, if the stored value is a legacy hash,
  compare `hash_equals($stored, md5($pw))`, and on success replace it with `password_hash($pw, …)`. Users
  who never return keep a weak hash; wrapping (`password_hash($legacyHash)`) protects them too, at the cost
  of a second verification path.

## Comparisons on secrets

`md5('240610708') == md5('QNKCDZO')` is true, and `true == 'any string'` is true, so a JSON body with
`"password": true` or a digest starting `0e` passes a loose check. `strcmp` with an array argument now
throws `TypeError`, so it crashes instead of bypassing, but the request still controls that path. Use
`password_verify` for passwords, `hash_equals($known, $given)` for tokens and signatures (both strings,
known first), and check the type of every decoded field.

## Tokens and randomness

`mt_rand`, `rand`, `uniqid`, `str_shuffle`, `shuffle` and `array_rand` are predictable: `mt_srand(42)`
repeats, and `uniqid()` is the clock. For tokens, reset links and codes use `bin2hex(random_bytes(32))`,
`random_int`, or `(new Random\Randomizer())->getBytesFromString($alphabet, $length)`.

## Deserialization

`unserialize` instantiates any class named in the payload and runs `__wakeup`, `__unserialize` and
`__destruct`; public gadget chains exist for common Composer packages. php.net says not to pass untrusted
input to it whatever `allowed_classes` says. Cookies, hidden fields, and cache or queue rows an attacker
can write are untrusted. Use JSON with `JSON_THROW_ON_ERROR`, and sign a value that must round-trip with
`hash_hmac` and check it with `hash_equals`. Prove it: a test that sends a serialized object must not
instantiate it.

`phar://` paths no longer unserialize metadata on file access since 8.0, but `Phar::getMetadata()` still
does, and user-supplied paths still reach the `phar://`, `data://` and `php://filter` wrappers.

## SQL through PDO

- Since 8.0 PDO throws by default, and the exception message carries the SQL and schema. With
  `display_errors=1`, the built-in default, an uncaught one prints them to the visitor.
- The MySQL driver emulates prepares by default. Set `PDO::ATTR_EMULATE_PREPARES => false`, and the
  charset in the DSN (`charset=utf8mb4`), never with `SET NAMES`.
- `exec()` runs every statement in a string (`select 1; delete from users` deletes); emulated MySQL
  prepares allow stacked statements too.
- An identifier cannot be a bound parameter: `ORDER BY ?` sorts by a constant string and raises nothing,
  so a test that checks for no exception passes. Map input to fixed SQL:

```php
$columns = ['name' => 'name', 'price' => 'price_cents', 'added' => 'created_at'];
$order = $columns[$_GET['sort'] ?? ''] ?? 'created_at';
$direction = strtolower($_GET['dir'] ?? '') === 'desc' ? 'DESC' : 'ASC';
$rows = $db->query("SELECT id, name, price_cents FROM products ORDER BY $order $direction")->fetchAll();
```

- Binding prevents injection, not wildcards: a search term of `%` matches every row. Escape with
  `addcslashes($term, '%_\\')` and add `ESCAPE '\'`.
- One placeholder binds one value: `IN (?)` with `"1,3"` matches nothing, or on MySQL silently matches
  id 1. Build one `?` per element, and skip the query for an empty list (`IN ()` is a syntax error on
  MySQL and PostgreSQL).

## Includes, paths and uploads

- `include` executes PHP inside any file, whatever its extension: an uploaded `avatar.jpg` containing
  `<?php` runs when included. `allow_url_include` is off by default, which blocks remote includes, not
  local ones. Never build an include path from input; map a page name to a file through an allow-list.
- `str_starts_with(realpath($path), $base)` passes for the sibling directory `$base . '_private'`. Compare
  with `$base . DIRECTORY_SEPARATOR`, and reject `realpath() === false` (it returns `false` for a path
  that does not exist, so check the directory of a file about to be written).
- `basename('..')` is `..`, and on Linux `basename('..\\x.php')` keeps the backslashes: reject `.`, `..`
  and empty names after it.
- `$_FILES[...]['type']` and `['name']` are chosen by the client, and a file can be a valid image and
  valid PHP at once, so `finfo` and `getimagesize` both accept it. Store uploads outside the web root under
  a generated name, take the extension from an allow-list keyed on the detected type, and serve them
  through a script with `Content-Type` and `X-Content-Type-Options: nosniff`. `.phtml`, `.phar` and
  `.php5` execute on many server configurations.
- The web root is `public/` with one front controller; with the project root as web root, `vendor/`,
  `.env`, `composer.json` and `.git/` become URLs. Prove it: `curl -I` on `/vendor/autoload.php` and
  `/.env` answers 404.

## Shell and code execution

- A command string goes through `/bin/sh`. `escapeshellarg` stops `; rm …` but not an argument starting
  with `-`, which the program reads as an option (the real bug in git, tar and curl wrappers).
  `escapeshellcmd` does not separate arguments at all.
- `proc_open(['git', 'log', '--', $path], $descriptors, $pipes)` takes an argument array and runs no
  shell; put `--` before user operands.
- `$fn = $_GET['f']; $fn()` and `call_user_func($_GET['f'])` call any function, `system` included.
  `extract($_POST)` overwrites local variables such as `$isAdmin`.
- `mail()` with string headers accepts injected `\r\nBcc:` lines; array headers throw `ValueError` on
  CRLF. Never put input in its fifth argument. `header()` drops a value containing a newline with only a
  warning, so the redirect you meant to send silently does not happen.

## Output escaping

- `htmlspecialchars()` with no flags escapes both quote types and substitutes invalid UTF-8 (the 8.1
  defaults). Code that passes `ENT_QUOTES` alone loses `ENT_SUBSTITUTE`, and invalid UTF-8 then returns an
  empty string. Quote every attribute: an unquoted `value=<?= … ?>` is open to `x onmouseover=…`.
- `href` needs a scheme allow-list: `htmlspecialchars('javascript:alert(1)')` is unchanged,
  `FILTER_VALIDATE_URL` accepts `javascript://comment%0aalert(1)`, and `parse_url` returns no scheme for a
  leading space that browsers strip.
- JSON inside a `<script>`: `json_encode($v, JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT | JSON_THROW_ON_ERROR)`.
  `JSON_UNESCAPED_SLASHES` lets `</script>` through.

## Sessions and configuration

The built-in defaults accept an attacker-chosen session id and send the cookie without `HttpOnly`,
`Secure` or `SameSite`; they also display errors and advertise the PHP version.

```php
session_start([
    'use_strict_mode' => 1,
    'cookie_httponly' => 1,
    'cookie_secure' => 1,
    'cookie_samesite' => 'Lax',
]);
// after a successful login or a privilege change:
session_regenerate_id(true);
```

Prove it: send `Cookie: PHPSESSID=chosen123` and expect a new `Set-Cookie` carrying `secure; HttpOnly;
SameSite`. In production set `display_errors=Off`, `expose_php=Off`, and log errors instead.

## Outbound requests and XML

- `file_get_contents($url)` with a user URL reads `file://`, `php://` and `phar://` too, and follows up to
  20 redirects, so validating the first URL does not stop a redirect to an internal address.
  `FILTER_VALIDATE_URL` accepts `file:///etc/passwd` and `http://127.0.0.1:6379/`. Allow-list the scheme,
  resolve the host and check the address with `FILTER_VALIDATE_IP` and
  `FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE`, disable redirects (`follow_location => 0`, or
  re-check each hop), and connect to the address you checked.
- libxml no longer loads external entities by default. `LIBXML_NOENT`, often copied to "make entities
  work", turns XXE back on and reads local files; leave it and `LIBXML_DTDLOAD` off for untrusted XML.
  `libxml_disable_entity_loader()` is deprecated and can be deleted.
