+++
subject = "dry-simplicity-reviewer"
kind = "quality"
difficulty = "complex"
trap = "real duplication beside code that only looks duplicated and must stay apart"
fixture = "fees"
cases_version = 1
key = """
must:
  M1 drift  the VAT rate is written twice: invoices.VAT_BP = 2100 and the literal 2000 in quotes.quote_totals. The copies already disagree: a quote shows VAT 2000 where its invoice shows 2100 (reproduced), against "VAT is 21%" and "A quote and the invoice for it must show the same VAT". Consolidate into one constant both import; 2100 is right.
  M2 dup    customers_csv, invoices_csv and payments_csv are the same seven lines with a different column list; a change to the export format (delimiter, encoding, a BOM for the accountants' Excel) must be made three times. Consolidate into one export_csv(rows, columns), keeping the three column lists.
good code:
  G1 money.percent_of is the one place percentages are computed; every caller uses it.
  G2 addresses._well_formed is already the shared part of the two email checks.
decoys (each looks duplicated; merging it is a false positive):
  D1 LATE_FEE_BP and CARD_SURCHARGE_BP are both 250 and late_fee and card_surcharge have the same body, but AGENTS.md says they are separate decisions owned by different contracts that change independently. Merging them into one constant or one function is the failure this case measures.
  D2 valid_signup_email and valid_billing_email look alike, but they enforce different rules (company domain vs any address). Merging them into one function with a flag is a false positive; they already share _well_formed.
  D3 the tests repeat a few setup values; each test reads alone.
taste:
  T1 typing List/Dict imports on Python 3.12; T2 the FREE_MAIL set as a module constant; T3 test names.
extras:
  X1 invoice_totals and quote_totals both compute net as the same sum over lines; a shared lines_net() is a fair small consolidation once M1 is done.
  X2 the email is normalized (strip, lower) in both checks; harmless, each function is used alone.
"""
+++
Look for duplication, redundancy and needless complexity in the `fees` package, and tell me what is worth consolidating or simplifying.
