import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { expect, test } from 'vitest';
import { Cart } from '../src/Cart.jsx';

test('removes an item', async () => {
  const user = userEvent.setup();
  render(<Cart initialItems={[{ id: 'a', name: 'Mug', qty: 1 }, { id: 'b', name: 'Tote', qty: 2 }]} />);
  await user.click(screen.getByRole('button', { name: 'Remove Mug' }));
  expect(screen.queryByText('Mug')).toBeNull();
  expect(screen.getByText('Tote')).toBeTruthy();
});
