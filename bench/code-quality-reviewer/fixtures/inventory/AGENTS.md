# AGENTS

`inventory` tracks stock for a warehouse that ships to several online stores at once. Python 3.9+,
standard library only. Requests arrive on many threads; overselling stock means a customer is
charged for something that is not on the shelf.

## Rules

- **Stock never goes below zero.**
- **Quantities are positive integers** wherever an order or a return enters the system.

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
