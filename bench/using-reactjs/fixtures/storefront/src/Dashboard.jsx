import { createContext, useContext, useEffect, useState } from 'react';
import { priceStore } from './prices.js';

const ShopContext = createContext(null);

function formatPrice(cents, currency) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency }).format(cents / 100);
}

function ProductRow({ product }) {
  const { currency, prices } = useContext(ShopContext);
  const cents = prices[product.id] ?? product.cents;
  return (
    <tr>
      <td>{product.name}</td>
      <td>{formatPrice(cents, currency)}</td>
    </tr>
  );
}

function Clock() {
  const { now } = useContext(ShopContext);
  return <p>Updated {new Date(now).toLocaleTimeString('en-US')}</p>;
}

export function Dashboard({ products, currency = 'USD' }) {
  const [filter, setFilter] = useState('');
  const [now, setNow] = useState(Date.now());
  const [prices, setPrices] = useState(priceStore.get());

  useEffect(() => {
    const id = setInterval(() => setNow(Date.now()), 250);
    return () => clearInterval(id);
  }, []);

  useEffect(() => priceStore.subscribe(() => setPrices({ ...priceStore.get() })), []);

  const visible = products.filter((p) => p.name.toLowerCase().includes(filter.toLowerCase()));

  return (
    <ShopContext.Provider value={{ currency, prices, now }}>
      <Clock />
      <input aria-label="Filter products" value={filter} onChange={(e) => setFilter(e.target.value)} />
      <table>
        <tbody>
          {visible.map((p) => (
            <ProductRow key={p.id} product={p} />
          ))}
        </tbody>
      </table>
    </ShopContext.Provider>
  );
}
