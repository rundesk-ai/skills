"""Run a large settlement and report work done, deaths and time: python3 -m tools.bench_tick [workers]"""

import sys
import time

from sim.settlement import Settlement


def build(n, seed=11):
    s = Settlement(seed=seed)
    size = 200
    for _ in range(n * 2):
        s.add_tree((s.rng.randrange(size), s.rng.randrange(size)))
    for _ in range(max(1, n // 20)):
        s.add_food((s.rng.randrange(size), s.rng.randrange(size)), portions=200)
    for _ in range(n):
        s.add_worker((s.rng.randrange(size), s.rng.randrange(size)))
    return s


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    s = build(n)
    worst = 0.0
    start = time.perf_counter()
    for t in range(600):
        if t == 100:
            for w in s.workers[: n // 10]:
                if w.task and w.task[0] == "chop":
                    s.kill(w)
        t0 = time.perf_counter()
        s.tick()
        worst = max(worst, time.perf_counter() - t0)
    total = time.perf_counter() - start
    wood = sum(w.wood for w in s.workers)
    stuck = sum(1 for t in s.trees if t.taken and not t.felled)
    idle = sum(1 for w in s.workers if w.alive and w.task is None)
    switches = sum(w.task_switches for w in s.workers)
    print(f"workers={n} ticks=600 total_ms={total*1000:.0f} worst_tick_ms={worst*1000:.1f} "
          f"wood={wood} deaths={s.deaths} trees_taken_but_unworked={stuck} idle_now={idle} task_switches={switches}")


if __name__ == "__main__":
    main()
