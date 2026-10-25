"""Colonists walking the tile world. One tick moves each colonist one tile."""

from sim.pathfind import find_path


class Colonist:
    def __init__(self, cid, pos):
        self.id = cid
        self.pos = pos
        self.goal = None
        self.path = None
        self.searches = 0

    def order_move(self, goal):
        self.goal = goal
        self.path = None


class Colony:
    def __init__(self, world):
        self.world = world
        self.colonists = {}
        self.tick_count = 0
        self._seen_revision = world.revision

    def add_colonist(self, pos):
        c = Colonist(len(self.colonists), pos)
        self.colonists[c.id] = c
        return c

    def tick(self):
        if self.world.revision != self._seen_revision:
            self._seen_revision = self.world.revision
            for c in self.colonists.values():
                c.path = None
        for c in self.colonists.values():
            self._update(c)
        self.tick_count += 1

    def _update(self, c):
        if c.goal is None or c.pos == c.goal:
            return
        if not c.path:
            c.searches += 1
            c.path = find_path(self.world, c.pos, c.goal)
            if not c.path:
                return
            c.path.pop(0)
        nxt = c.path[0]
        if not self.world.walkable(*nxt):
            c.path = None
            return
        c.pos = c.path.pop(0)

    def digest(self):
        return hash(tuple((c.id, c.pos) for c in self.colonists.values()))
