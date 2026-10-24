// Stand-in for the database client.
const saved = new Map();

export async function saveOrder(order) {
  if (!order.sku) throw new Error(`order ${order.id} has no sku`);
  saved.set(String(order.id), order);
}

export async function searchOrders(q) {
  return [...saved.values()].filter((order) => order.sku.includes(q));
}
