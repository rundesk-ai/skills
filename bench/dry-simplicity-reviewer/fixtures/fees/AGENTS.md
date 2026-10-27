# AGENTS

`fees` prices quotes and invoices for a B2B software reseller and exports its ledgers to the
accountants. Python 3.12, standard library only.

## Rules

- **Money is integer cents**, and every percentage goes through `fees.money.percent_of`.
- **VAT is 21%** (2,100 basis points) since 1 January 2026. A quote and the invoice for it must show
  the same VAT.
- **The late fee and the card surcharge are separate decisions.** The late fee is set by our finance
  terms; the card surcharge by the card networks' rules. Both are 2.5% today, and either can change
  without the other.
- **Sign-up and billing addresses follow different rules.** Sign-ups must use a company domain;
  billing contacts may use any address, including plus-addressing.

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
