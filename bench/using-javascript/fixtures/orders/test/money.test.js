import test from 'node:test';
import assert from 'node:assert/strict';
import { orderTotals } from '../src/money.js';

test('totals with tax', () => {
  assert.deepEqual(orderTotals([{ price: 10, qty: 2 }], 0.1), { subtotal: '20.00', tax: '2.00', total: '22.00' });
});
