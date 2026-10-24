// Catalog prices arrive in dollars, for example { price: 4.99, qty: 2 }.
export function orderTotals(lines, taxRate) {
  const subtotal = lines.reduce((sum, line) => sum + line.price * line.qty, 0);
  const tax = subtotal * taxRate;
  return {
    subtotal: subtotal.toFixed(2),
    tax: tax.toFixed(2),
    total: (subtotal + tax).toFixed(2),
  };
}
