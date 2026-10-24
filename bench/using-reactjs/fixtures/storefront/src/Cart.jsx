import { useState } from 'react';

function CartRow({ item, onRemove }) {
  const [qty, setQty] = useState(item.qty);
  return (
    <li>
      <span>{item.name}</span>
      <label>
        Quantity for {item.name}
        <input type="number" min="1" value={qty} onChange={(e) => setQty(Number(e.target.value))} />
      </label>
      <button onClick={onRemove}>Remove {item.name}</button>
    </li>
  );
}

export function Cart({ initialItems }) {
  const [items, setItems] = useState(initialItems);
  return (
    <ul>
      {items.map((item, i) => (
        <CartRow key={i} item={item} onRemove={() => setItems(items.filter((_, j) => j !== i))} />
      ))}
    </ul>
  );
}
