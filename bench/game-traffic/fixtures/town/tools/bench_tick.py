"""Rush hour in a grid town: python3 -m tools.bench_tick [cars_per_tick] [game_speed]"""

import sys
import time

from sim.traffic import Town


def main():
    rate = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    speed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    town = Town(size=8, seed=5)
    town.game_speed = speed
    rng = town.rng
    worst = 0.0
    min_gap = float("inf")
    start = time.perf_counter()
    for t in range(1200):
        for _ in range(rate):
            west = town.node_at(0, rng.randrange(town.size))
            east = town.node_at(town.size - 1, rng.randrange(town.size))
            town.spawn(west, east)
        t0 = time.perf_counter()
        town.tick()
        worst = max(worst, time.perf_counter() - t0)
        min_gap = min(min_gap, town.min_gap())
    total = time.perf_counter() - start
    active = len(town.cars)
    inside = sum(len(n.inside) for n in town.nodes)
    avenue = sum(len(l.cars) for r in town.roads if r.lane_count == 2 for l in r.lanes)
    print(f"ticks=1200 speed={speed}x total_ms={total*1000:.0f} worst_tick_ms={worst*1000:.1f} "
          f"spawned={town.spawned} arrived={town.arrived} active={active} "
          f"unaccounted={town.spawned - town.arrived - active} stuck_in_junctions={inside} "
          f"on_avenue={avenue} min_gap_m={min_gap:.1f}")


if __name__ == "__main__":
    main()
