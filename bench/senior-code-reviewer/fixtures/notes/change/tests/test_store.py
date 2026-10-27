import unittest

from notes import store


class StoreTest(unittest.TestCase):
    def setUp(self):
        self.db = store.connect()
        self.a = store.add_note(self.db, "ada", "buy tea")
        self.b = store.add_note(self.db, "bob", "call mum")

    def test_owner_reads_own_note(self):
        self.assertEqual(store.get_note(self.db, "ada", self.a)["body"], "buy tea")

    def test_other_user_cannot_read(self):
        with self.assertRaises(store.NotFound):
            store.get_note(self.db, "ada", self.b)

    def test_list_is_per_owner(self):
        self.assertEqual([n["id"] for n in store.list_notes(self.db, "ada")], [self.a])

    def test_delete_own_note(self):
        store.delete_note(self.db, "ada", self.a)
        self.assertEqual(store.list_notes(self.db, "ada"), [])

    def test_search(self):
        self.assertEqual([n["id"] for n in store.search_notes(self.db, "ada", "tea")], [self.a])
