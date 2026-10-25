"""Tile world: walkability and the edits the player makes."""


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.blocked = [[False] * width for _ in range(height)]
        self.revision = 0

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def walkable(self, x, y):
        return self.in_bounds(x, y) and not self.blocked[y][x]

    def set_blocked(self, x, y, value=True):
        self.blocked[y][x] = value
        self.revision += 1

    def build_wall(self, cells):
        for x, y in cells:
            self.set_blocked(x, y, True)

    @classmethod
    def from_rows(cls, rows):
        world = cls(len(rows[0]), len(rows))
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch == "#":
                    world.blocked[y][x] = True
        return world
