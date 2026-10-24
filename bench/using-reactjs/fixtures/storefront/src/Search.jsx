import { useEffect, useState } from 'react';
import { searchProducts } from './api.js';

export function Search() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [count, setCount] = useState(0);

  useEffect(() => {
    if (!query) return;
    searchProducts(query).then(setResults);
  }, [query]);

  useEffect(() => {
    setCount(results.length);
  }, [results]);

  return (
    <div>
      <input aria-label="Search products" value={query} onChange={(e) => setQuery(e.target.value)} />
      <p>{count} results</p>
      <ul>
        {results.map((p) => (
          <li key={p.id}>{p.name}</li>
        ))}
      </ul>
    </div>
  );
}
