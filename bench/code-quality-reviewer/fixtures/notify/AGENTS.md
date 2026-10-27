# AGENTS

`notify` sends account emails (welcome, password reset) for a multi-tenant booking platform. Python
3.9+, standard library only. Each tenant is a separate business with its own customers.

## Rules

- **Each tenant's mail goes out from that tenant's own address.** A customer must never receive mail
  from another business.

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
