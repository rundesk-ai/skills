from typing import Dict, Tuple

# (sku, region) -> price in cents
PRICES: Dict[Tuple[str, str], int] = {}
# sku -> units on hand
STOCK: Dict[str, int] = {}
# sku -> product record; "weight" is in grams
PRODUCTS: Dict[str, Dict] = {}
