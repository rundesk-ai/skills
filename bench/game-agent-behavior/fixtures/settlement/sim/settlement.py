"""A settlement of workers who chop trees and eat. One tick is one game minute."""

import random

HUNGER_PER_TICK = 0.004
EAT_THRESHOLD = 0.6
STARVE_AT = 1.0
CHOP_TICKS = 20


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def step_toward(pos, target):
    x, y = pos
    if x != target[0]:
        x += 1 if target[0] > x else -1
    elif y != target[1]:
        y += 1 if target[1] > y else -1
    return (x, y)


class Tree:
    def __init__(self, tid, pos):
        self.id = tid
        self.pos = pos
        self.taken = False
        self.felled = False


class Food:
    def __init__(self, fid, pos, portions):
        self.id = fid
        self.pos = pos
        self.portions = portions


class Worker:
    def __init__(self, wid, pos, rng):
        self.id = wid
        self.pos = pos
        self.hunger = rng.random() * 0.5
        self.alive = True
        self.task = None          # ("chop", tree) or ("eat", food)
        self.progress = 0
        self.wood = 0
        self.task_switches = 0


class Settlement:
    def __init__(self, seed=1):
        self.rng = random.Random(seed)
        self.trees = []
        self.food = []
        self.workers = []
        self.tick_count = 0
        self.deaths = 0

    def add_tree(self, pos):
        self.trees.append(Tree(len(self.trees), pos))

    def add_food(self, pos, portions):
        self.food.append(Food(len(self.food), pos, portions))

    def add_worker(self, pos):
        w = Worker(len(self.workers), pos, self.rng)
        self.workers.append(w)
        return w

    def tick(self):
        for w in self.workers:
            if w.alive:
                self.think(w)
                self.act(w)
        self.tick_count += 1

    def think(self, w):
        old = w.task
        if w.hunger > EAT_THRESHOLD and any(f.portions > 0 for f in self.food):
            food = min((f for f in self.food if f.portions > 0), key=lambda f: dist(w.pos, f.pos))
            w.task = ("eat", food)
        else:
            open_trees = [t for t in self.trees if not t.felled and not t.taken]
            if w.task and w.task[0] == "chop" and not w.task[1].felled:
                pass
            elif open_trees:
                w.task = ("chop", min(open_trees, key=lambda t: dist(w.pos, t.pos)))
            else:
                w.task = None
        if w.task != old:
            w.task_switches += 1
            w.progress = 0

    def act(self, w):
        w.hunger += HUNGER_PER_TICK
        if w.hunger >= STARVE_AT:
            w.alive = False
            self.deaths += 1
            return
        if w.task is None:
            return
        kind, target = w.task
        if w.pos != target.pos:
            w.pos = step_toward(w.pos, target.pos)
            return
        if kind == "chop":
            if target.taken and w.progress == 0:
                w.task = None          # somebody else got here first
                return
            target.taken = True
            w.progress += 1
            if w.progress >= CHOP_TICKS:
                target.felled = True
                target.taken = False
                w.wood += 1
                w.task = None
        else:
            if target.portions > 0:
                target.portions -= 1
                w.hunger = max(0.0, w.hunger - 0.5)
            w.task = None

    def kill(self, w):
        w.alive = False
        self.deaths += 1
