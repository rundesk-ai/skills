import csv
import io
from typing import Dict, List

CUSTOMER_COLUMNS = ["id", "name", "country", "vat_number"]
INVOICE_COLUMNS = ["id", "customer_id", "issued", "net", "vat", "gross"]
PAYMENT_COLUMNS = ["id", "invoice_id", "paid", "amount", "method"]


def customers_csv(rows: List[Dict]) -> str:
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(CUSTOMER_COLUMNS)
    for row in rows:
        writer.writerow([row[c] for c in CUSTOMER_COLUMNS])
    return out.getvalue()


def invoices_csv(rows: List[Dict]) -> str:
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(INVOICE_COLUMNS)
    for row in rows:
        writer.writerow([row[c] for c in INVOICE_COLUMNS])
    return out.getvalue()


def payments_csv(rows: List[Dict]) -> str:
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(PAYMENT_COLUMNS)
    for row in rows:
        writer.writerow([row[c] for c in PAYMENT_COLUMNS])
    return out.getvalue()
