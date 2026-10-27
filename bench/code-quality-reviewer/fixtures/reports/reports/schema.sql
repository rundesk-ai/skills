CREATE TABLE customers (id INTEGER PRIMARY KEY, email TEXT NOT NULL);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(id),
                     currency TEXT NOT NULL, total_cents INTEGER NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE order_items (id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES orders(id),
                          sku TEXT NOT NULL, qty INTEGER NOT NULL, price_cents INTEGER NOT NULL);
CREATE INDEX order_items_order ON order_items(order_id);
