import unittest

from sim.traffic import Town


class TrafficTest(unittest.TestCase):
    def test_a_car_arrives(self):
        town = Town(size=4)
        car = town.spawn(town.node_at(0, 0), town.node_at(3, 0))
        self.assertIsNotNone(car)
        for _ in range(200):
            town.tick()
        self.assertEqual(town.arrived, 1)

    def test_route_is_connected(self):
        town = Town(size=4)
        roads = town.route(town.node_at(0, 0), town.node_at(3, 3))
        for a, b in zip(roads, roads[1:]):
            self.assertEqual(town.roads[a].b, town.roads[b].a)


if __name__ == "__main__":
    unittest.main()
