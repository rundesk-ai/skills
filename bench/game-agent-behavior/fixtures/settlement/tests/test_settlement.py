import unittest

from sim.settlement import Settlement


class SettlementTest(unittest.TestCase):
    def test_a_worker_fells_a_tree(self):
        s = Settlement(seed=3)
        s.add_tree((5, 0))
        s.add_food((0, 5), portions=10)
        s.add_worker((0, 0))
        for _ in range(60):
            s.tick()
        self.assertTrue(s.trees[0].felled)

    def test_a_hungry_worker_eats(self):
        s = Settlement(seed=3)
        s.add_food((2, 0), portions=10)
        w = s.add_worker((0, 0))
        w.hunger = 0.7
        for _ in range(5):
            s.tick()
        self.assertLess(w.hunger, 0.6)


if __name__ == "__main__":
    unittest.main()
