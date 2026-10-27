from typing import Dict

from .api import parse_order
from .stock import Stock


def place_order(stock: Stock, body: Dict) -> bool:
    return stock.reserve(parse_order(body))


def accept_return(stock: Stock, body: Dict) -> None:
    for line in parse_order(body):
        stock.restock(line["sku"], line["qty"])


def availability(stock: Stock, sku: str) -> str:
    qty = stock.find(sku.strip().upper())
    if qty is None:
        return "unknown product"
    return "in stock" if qty > 0 else "sold out"
