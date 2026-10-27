# AGENTS

`clinic` books appointments and renews memberships for a small group of physiotherapy clinics.
Python 3.9+, standard library only.

## Rules

- **A membership renews on the same day of the month**, or on the month's last day when that month
  is shorter (January 31 renews on February 28 or 29).
- **Only admins and owners may cancel another person's appointment.**

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
