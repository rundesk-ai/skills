# AGENTS

`billing` computes what a subscriber owes when they join, leave or change plan mid-month. Python
3.9+, standard library only. Every amount on an invoice comes from here.

## Rules

- **A billing period includes both its first and last day.** March 1 to March 31 is 31 days.
- **Money is integer cents, rounded half up** to the cent (2.5 cents is 3).
- **Discounts apply percentage first, then the fixed amount.** 10% and $5 off $100 is $85.
- **Tests state the behaviour these rules require.** A test that disagrees with a rule is wrong.

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
