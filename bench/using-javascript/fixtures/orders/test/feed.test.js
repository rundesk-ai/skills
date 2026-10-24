import test from 'node:test';
import assert from 'node:assert/strict';
import { parseFeed, indexById, findOrder } from '../src/feed.js';

test('finds an order by id', () => {
  const orders = parseFeed('{"orders":[{"id":81234,"sku":"mug","qty":1,"total":9}]}');
  assert.equal(findOrder(indexById(orders), '81234').sku, 'mug');
});
