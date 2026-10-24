import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { expect, test } from 'vitest';
import { Dashboard } from '../src/Dashboard.jsx';

const products = Array.from({ length: 50 }, (_, i) => ({ id: i, name: `Product ${i}`, cents: 1000 + i }));

test('filters products', async () => {
  const user = userEvent.setup();
  render(<Dashboard products={products} />);
  await user.type(screen.getByLabelText('Filter products'), 'Product 4');
  expect(screen.getAllByRole('row')).toHaveLength(11);
});
