"""Road traffic on a grid town. Lengths in metres, speeds in m/s, one tick is BASE_DT seconds."""

import heapq
import random

BASE_DT = 0.5
CAR_LENGTH = 5.0
SAFE_GAP = 10.0
JUNCTION_TICKS = 4
STUCK_TICKS = 30


class Lane:
    def __init__(self, lid, road, index):
        self.id = lid
        self.road = road
        self.index = index            # 0 = rightmost
        self.cars = []                # front first


class Road:
    def __init__(self, rid, a, b, length, speed, lanes):
        self.id = rid
        self.a = a
        self.b = b
        self.length = length
        self.speed = speed
        self.lanes = []
        self.lane_count = lanes


class Node:
    def __init__(self, nid, x, y):
        self.id = nid
        self.x = x
        self.y = y
        self.out = []                 # roads leaving this node
        self.inside = []              # cars crossing the junction: [car, ticks_left, next_road]


class Car:
    def __init__(self, cid, route):
        self.id = cid
        self.route = route            # list of road ids still to drive, current first
        self.lane = None
        self.s = 0.0
        self.v = 0.0
        self.stopped_ticks = 0


class Town:
    def __init__(self, size=6, spacing=100.0, seed=1):
        self.rng = random.Random(seed)
        self.nodes = []
        self.roads = []
        self.lanes = []
        self.cars = {}
        self.next_car = 0
        self.game_speed = 1
        self.spawned = 0
        self.arrived = 0
        self.tick_count = 0
        for y in range(size):
            for x in range(size):
                self.nodes.append(Node(len(self.nodes), x, y))
        avenue_y = size // 2
        for n in self.nodes:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                x, y = n.x + dx, n.y + dy
                if 0 <= x < size and 0 <= y < size:
                    m = self.nodes[y * size + x]
                    lanes = 2 if (n.y == avenue_y and m.y == avenue_y) else 1
                    self._add_road(n, m, spacing, 14.0 if lanes == 2 else 11.0, lanes)
        self.size = size

    def _add_road(self, a, b, length, speed, lanes):
        r = Road(len(self.roads), a.id, b.id, length, speed, lanes)
        for i in range(lanes):
            lane = Lane(len(self.lanes), r, i)
            self.lanes.append(lane)
            r.lanes.append(lane)
        self.roads.append(r)
        a.out.append(r)

    # --- routing: shortest distance, computed once at spawn ---
    def route(self, src, dst):
        dist = {src: 0.0}
        prev = {}
        heap = [(0.0, src)]
        while heap:
            d, n = heapq.heappop(heap)
            if n == dst:
                break
            if d > dist[n]:
                continue
            for r in self.nodes[n].out:
                nd = d + r.length
                if nd < dist.get(r.b, float("inf")):
                    dist[r.b] = nd
                    prev[r.b] = r.id
                    heapq.heappush(heap, (nd, r.b))
        if dst not in prev:
            return None
        roads = []
        n = dst
        while n != src:
            rid = prev[n]
            roads.append(rid)
            n = self.roads[rid].a
        roads.reverse()
        return roads

    def spawn(self, src, dst):
        roads = self.route(src, dst)
        if not roads:
            return None
        car = Car(self.next_car, roads)
        self.next_car += 1
        lane = self.roads[roads[0]].lanes[0]
        if lane.cars and lane.cars[-1].s < SAFE_GAP + CAR_LENGTH:
            return None
        car.lane = lane
        lane.cars.append(car)
        self.cars[car.id] = car
        self.spawned += 1
        return car

    # --- stepping ---
    def tick(self):
        dt = BASE_DT * self.game_speed
        for node in self.nodes:
            self._step_junction(node)
        for lane in self.lanes:
            self._step_lane(lane, dt)
        self.tick_count += 1

    def _step_lane(self, lane, dt):
        road = lane.road
        for car in list(lane.cars):
            if car.id not in self.cars or car not in lane.cars:
                continue
            i = lane.cars.index(car)
            if i == 0:
                gap = float("inf")
            else:
                lead = lane.cars[i - 1]
                gap = lead.s - CAR_LENGTH - car.s
            car.v = 0.0 if gap < SAFE_GAP else road.speed
            if i == 0 and car.s >= road.length - 1.0:
                car.v = 0.0
                self._at_lane_end(car, lane)
            car.s = min(car.s + car.v * dt, road.length)
            self._lane_choice(car, lane)
            if car.v == 0.0:
                car.stopped_ticks += 1
                if car.stopped_ticks > STUCK_TICKS:
                    self._remove(car)
            else:
                car.stopped_ticks = 0

    def _lane_choice(self, car, lane):
        road = lane.road
        if road.lane_count < 2 or car.s < road.length - 10.0:
            return
        want = self._lane_for_next_turn(car)
        if want != lane.index:
            target = road.lanes[want]
            if all(abs(o.s - car.s) > CAR_LENGTH + 2 for o in target.cars):
                lane.cars.remove(car)
                target.cars.append(car)
                target.cars.sort(key=lambda c: -c.s)
                car.lane = target
            else:
                car.v = 0.0

    def _lane_for_next_turn(self, car):
        if len(car.route) < 2:
            return 0
        here = self.roads[car.route[0]]
        nxt = self.roads[car.route[1]]
        a, b, c = self.nodes[here.a], self.nodes[here.b], self.nodes[nxt.b]
        cross = (b.x - a.x) * (c.y - b.y) - (b.y - a.y) * (c.x - b.x)
        return 1 if cross > 0 else 0

    def _at_lane_end(self, car, lane):
        node = self.nodes[lane.road.b]
        if len(car.route) == 1:
            lane.cars.remove(car)
            del self.cars[car.id]
            self.arrived += 1
            return
        if node.inside:                    # one car at a time crosses
            return
        lane.cars.remove(car)
        node.inside.append([car, JUNCTION_TICKS, car.route[1]])

    def _step_junction(self, node):
        for entry in list(node.inside):
            car, left, next_road = entry
            if left > 0:
                entry[1] -= 1
                continue
            lane = self.roads[next_road].lanes[0]
            if lane.cars and lane.cars[-1].s < CAR_LENGTH + 1.0:
                car.stopped_ticks += 1     # waits inside the junction for room
                continue
            node.inside.remove(entry)
            car.route.pop(0)
            car.lane = lane
            car.s = 0.0
            car.stopped_ticks = 0
            lane.cars.append(car)

    def _remove(self, car):
        if car.lane and car in car.lane.cars:
            car.lane.cars.remove(car)
        self.cars.pop(car.id, None)

    def node_at(self, x, y):
        return self.nodes[y * self.size + x].id

    def min_gap(self):
        worst = float("inf")
        for lane in self.lanes:
            for a, b in zip(lane.cars, lane.cars[1:]):
                worst = min(worst, a.s - CAR_LENGTH - b.s)
        return worst
