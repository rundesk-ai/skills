import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { expect, test, vi } from 'vitest';
import { Search } from '../src/Search.jsx';
import * as api from '../src/api.js';

test('shows results for the query', async () => {
  vi.spyOn(api, 'searchProducts').mockResolvedValue([{ id: 1, name: 'Blue mug' }]);
  const user = userEvent.setup();
  render(<Search />);
  await user.type(screen.getByLabelText('Search products'), 'mug');
  expect(await screen.findByText('Blue mug')).toBeTruthy();
  expect(screen.getByText('1 results')).toBeTruthy();
});
