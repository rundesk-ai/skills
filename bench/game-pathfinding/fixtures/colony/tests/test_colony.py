import unittest

from sim.colony import Colony
from sim.pathfind import find_path
from sim.world import World

MAP = [
    "..........",
    "..####....",
    ".....#....",
    ".....#....",
    "..........",
]


class PathfindTest(unittest.TestCase):
    def test_finds_a_path(self):
        world = World.from_rows(MAP)
        path = find_path(world, (0, 0), (9, 4))
        self.assertIsNotNone(path)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (9, 4))

    def test_path_steps_are_walkable_neighbours(self):
        world = World.from_rows(MAP)
        path = find_path(world, (0, 0), (9, 4))
        for a, b in zip(path, path[1:]):
            self.assertTrue(world.walkable(*b))
            self.assertLessEqual(max(abs(a[0] - b[0]), abs(a[1] - b[1])), 1)


class ColonyTest(unittest.TestCase):
    def test_colonist_arrives(self):
        world = World.from_rows(MAP)
        colony = Colony(world)
        c = colony.add_colonist((0, 0))
        c.order_move((9, 4))
        for _ in range(40):
            colony.tick()
        self.assertEqual(c.pos, (9, 4))


if __name__ == "__main__":
    unittest.main()
