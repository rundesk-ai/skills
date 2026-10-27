# AGENTS

Signup is the account service for a small online course site. Python 3.9+, standard library only,
SQLite for storage.

## Rules

- **Passwords are stored only as `hashlib.scrypt` hashes** with a per-user random salt, via
  `signup.passwords.hash_password`. A leaked database must not reveal a password.
- **SQL takes parameters.** Every query passes values as `?` parameters, never by formatting them
  into the string.

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
