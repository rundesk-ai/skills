# AGENTS

`invoicing` computes tax on invoices for an accounting product. Python 3.9+, standard library only.
Every invoice our customers send to their own clients is priced here.

## Rules

- **Money is integer cents.**
- **Tests state the behaviour the requirement asks for.** Changing a test to match new output needs
  the requirement to say so.

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
