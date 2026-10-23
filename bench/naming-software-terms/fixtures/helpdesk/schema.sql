CREATE TABLE cust (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL
);

CREATE TABLE tickets (
  id INTEGER PRIMARY KEY,
  cust_id INTEGER NOT NULL REFERENCES cust(id),
  subject TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'open',  -- open | pending | closed
  flg_2 INTEGER NOT NULL DEFAULT 0,     -- 1 when the customer must not be emailed
  created_at TEXT NOT NULL,
  closed_at TEXT
);
