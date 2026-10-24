export async function searchProducts(query) {
  const res = await fetch(`/api/products?q=${encodeURIComponent(query)}`);
  if (!res.ok) throw new Error(`search failed: ${res.status}`);
  return res.json();
}
