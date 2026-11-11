# AGENTS

`shipments` books parcels for a regional courier: the booking desk and the customer website both
call `shipments.api`. Python 3.9+, standard library only. Four people work in this package every
week, and the website team reads `api.py` to learn what to send.

## Rules

- **Money is integer cents.**
- **`store.py` is the only module that reads or writes the data file.**

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
