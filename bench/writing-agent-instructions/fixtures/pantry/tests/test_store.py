import unittest

from pantry import store


class StoreTest(unittest.TestCase):
    def setUp(self):
        self.conn = store.connect(":memory:")
        store.migrate(self.conn)
        store.add_item(self.conn, "rice", "kg", 3, low_at=1)

    def tearDown(self):
        self.conn.close()

    def test_use_takes_stock_out(self):
        store.use(self.conn, 1, 2)
        self.assertEqual(store.all_items(self.conn)[0]["quantity"], 1)

    def test_use_refuses_more_than_is_there(self):
        with self.assertRaises(ValueError):
            store.use(self.conn, 1, 4)
        self.assertEqual(store.all_items(self.conn)[0]["quantity"], 3)

    def test_running_low_includes_the_threshold(self):
        store.use(self.conn, 1, 2)
        self.assertEqual([i["name"] for i in store.running_low(self.conn)], ["rice"])

    def test_migrate_twice_is_harmless(self):
        store.migrate(self.conn)
        self.assertEqual(len(store.all_items(self.conn)), 1)
