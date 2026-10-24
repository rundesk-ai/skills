// The warehouse feed: { "orders": [{ "id": 81234, "sku": "...", "qty": 1, "total": 12.5 }, ...] }
export function parseFeed(text) {
  return JSON.parse(text).orders;
}

export function indexById(orders) {
  return new Map(orders.map((order) => [String(order.id), order]));
}

// id comes from the URL, so it is a string.
export function findOrder(index, id) {
  return index.get(id);
}

export function topOrders(orders, n) {
  return [...orders].sort((a, b) => a.total < b.total).slice(0, n);
}
