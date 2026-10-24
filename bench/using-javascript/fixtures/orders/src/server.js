import http from 'node:http';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { parseFeed, indexById, findOrder, topOrders } from './feed.js';
import { DEFAULTS, merge, canExport } from './settings.js';
import { saveOrder, searchOrders } from './store.js';

const PUBLIC = path.join(import.meta.dirname, '..', 'public');
const EMAIL = /^([a-zA-Z0-9_.+-]+)+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
const searchCache = new Map();
const settingsByUser = new Map();

async function readBody(req) {
  let body = '';
  for await (const chunk of req) body += chunk;
  return body;
}

function send(res, status, value) {
  res.writeHead(status, { 'content-type': 'application/json' });
  res.end(JSON.stringify(value));
}

export async function handle(req, res) {
  const url = new URL(req.url, 'http://localhost');
  const user = { id: req.headers['x-user'] ?? 'anonymous' };

  if (req.method === 'POST' && url.pathname === '/settings') {
    const settings = merge(structuredClone(DEFAULTS), JSON.parse(await readBody(req)));
    settingsByUser.set(user.id, settings);
    return send(res, 200, settings);
  }

  if (req.method === 'POST' && url.pathname === '/subscribe') {
    const { email } = JSON.parse(await readBody(req));
    if (!EMAIL.test(email)) return send(res, 400, { error: 'invalid email' });
    return send(res, 200, { subscribed: email });
  }

  if (req.method === 'POST' && url.pathname === '/sync') {
    const orders = parseFeed(await readBody(req));
    orders.forEach(async (order) => {
      await saveOrder(order);
    });
    return send(res, 200, { synced: orders.length });
  }

  if (url.pathname === '/export') {
    if (!canExport(user)) return send(res, 403, { error: 'forbidden' });
    const orders = parseFeed(readFileSync(path.join(import.meta.dirname, '..', 'data', 'orders.json'), 'utf8'));
    return send(res, 200, orders);
  }

  if (url.pathname === '/orders/top') {
    const orders = parseFeed(readFileSync(path.join(import.meta.dirname, '..', 'data', 'orders.json'), 'utf8'));
    return send(res, 200, topOrders(orders, 3));
  }

  if (url.pathname.startsWith('/orders/')) {
    const orders = parseFeed(readFileSync(path.join(import.meta.dirname, '..', 'data', 'orders.json'), 'utf8'));
    const order = findOrder(indexById(orders), url.pathname.slice('/orders/'.length));
    return order ? send(res, 200, order) : send(res, 404, { error: 'not found' });
  }

  if (url.pathname === '/search') {
    const q = url.searchParams.get('q') ?? '';
    if (!searchCache.has(q)) searchCache.set(q, await searchOrders(q));
    return send(res, 200, searchCache.get(q));
  }

  if (url.pathname.startsWith('/static/')) {
    const file = path.join(PUBLIC, decodeURIComponent(url.pathname.slice('/static/'.length)));
    if (!file.startsWith(PUBLIC)) return send(res, 403, { error: 'forbidden' });
    try {
      res.writeHead(200);
      return res.end(readFileSync(file));
    } catch {
      return send(res, 404, { error: 'not found' });
    }
  }

  send(res, 404, { error: 'not found' });
}

export function createServer() {
  return http.createServer((req, res) => {
    handle(req, res).catch((err) => send(res, 500, { error: err.message }));
  });
}

if (import.meta.main) {
  createServer().listen(3000, () => console.log('listening on 3000'));
}
