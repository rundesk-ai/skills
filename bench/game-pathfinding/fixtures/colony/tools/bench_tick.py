"""Time colony ticks on a large map: python3 -m tools.bench_tick [colonists]"""

import random
import sys
import time

from sim.colony import Colony
from sim.world import World


def build(n, size=256, seed=7):
    rng = random.Random(seed)
    world = World(size, size)
    for _ in range(size * size // 12):
        world.blocked[rng.randrange(size)][rng.randrange(size)] = True
    for y in range(size):                      # a river with no bridge splits the map
        world.blocked[y][size // 2] = True
    colony = Colony(world)
    for _ in range(n):
        while True:
            p = (rng.randrange(size // 2), rng.randrange(size))
            if world.walkable(*p):
                break
        c = colony.add_colonist(p)
        if rng.random() < 0.05:                # a few are ordered across the river
            c.order_move((size // 2 + 1 + rng.randrange(size // 2 - 1), rng.randrange(size)))
        else:
            c.order_move((rng.randrange(size // 2), rng.randrange(size)))
    return world, colony, rng


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    world, colony, rng = build(n)
    worst = 0.0
    start = time.perf_counter()
    for t in range(30):
        if t == 10:
            world.build_wall([(x, 60) for x in range(20, 80)])
        t0 = time.perf_counter()
        colony.tick()
        worst = max(worst, time.perf_counter() - t0)
    total = time.perf_counter() - start
    searches = sum(c.searches for c in colony.colonists.values())
    print(f"colonists={n} ticks=30 total_ms={total*1000:.1f} worst_tick_ms={worst*1000:.1f} searches={searches}")


if __name__ == "__main__":
    main()
