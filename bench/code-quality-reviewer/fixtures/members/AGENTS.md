# AGENTS

`members` manages accounts for a community site: password resets, roles, and saved lists. PHP 8.4,
no Composer packages. Input arrives as JSON from the site's API.

## Rules

- **Only `admin` and `editor` may publish.**
- **A reset token is accepted only when it is exactly the one that was issued.**

## Build, test & run

```sh
php tests/run.php
```
