"""A* over the tile grid, 8-connected."""

import heapq
import math

DIRS = {(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)}


def heuristic(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


def step_cost(dx, dy):
    return math.sqrt(2) if dx and dy else 1.0


def find_path(world, start, goal):
    if not world.walkable(*goal):
        return None
    open_heap = [(heuristic(start, goal), start)]
    came_from = {}
    g = {start: 0.0}
    visited = set()
    while open_heap:
        _, cur = heapq.heappop(open_heap)
        if cur == goal:
            path = [cur]
            while cur in came_from:
                cur = came_from[cur]
                path.append(cur)
            path.reverse()
            return path
        visited.add(cur)
        for dx, dy in DIRS:
            nxt = (cur[0] + dx, cur[1] + dy)
            if not world.walkable(*nxt) or nxt in visited:
                continue
            if nxt not in g:
                g[nxt] = g[cur] + step_cost(dx, dy)
                came_from[nxt] = cur
                heapq.heappush(open_heap, (g[nxt] + heuristic(nxt, goal), nxt))
    return None
