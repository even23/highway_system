import math
import random as rnd

import numpy as np

import config


def parse_file_with_cities(filename):
    cities = list()

    with open(filename, 'r') as file:
        for line in file.readlines():
            x, y = map(int, line.split())
            cities.append(Point(x, y))

    return cities


def generate_cities(m=config.DEFAULT_M):
    cities = list()

    for i in range(m):
        x = rnd.randint(0, config.MAX_X)
        y = rnd.randint(0, config.MAX_Y)
        cities.append(Point(x, y))

    return cities


class Point:
    def __init__(self, x_=.0, y_=.0):
        self.x = x_
        self.y = y_

    def distance(self, point):
        return math.hypot(self.x - point.x, self.y - point.y)

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)


class HighwayPoint:
    def __init__(self, position_: Point = None, next_: 'HighwayPoint' = None):
        self.position = position_ or Point()
        self.next = next_
        self.connections = set()

    @property
    def distance(self):
        return self.position.distance(self.next.position)

    def __repr__(self):
        next_position = self.next.position if self.next else None

        return '[{} -> {}]'.format(self.position, next_position)


class HighwayExit:
    def __init__(self, position_: Point, city_: Point, highway_point_: HighwayPoint = None):
        self.position = position_
        self.city = city_
        self.highway_point = highway_point_

    @property
    def distance(self):
        return self.position.distance(self.city)

    def __repr__(self):
        return '{{} - {}}'.format(self.position, self.city)


class Model:
    @property
    def highway_cost(self):
        return config.linear_cost

    @property
    def exit_cost(self):
        return config.exponential_cost

    def __init__(self, cities, highway_size, exit_distance):
        self.cities = cities
        self.exit_distance = exit_distance

        self.highway = [HighwayPoint() for _ in range(highway_size)]
        self.exits = []

    def move(self):
        point_to_move = rnd.randint(0, len(self.highway) - 1)
        self.randomize_highway_point(point_to_move)
        self.calculate_exits()
        self.update_highway_points_connections()

    def calculate_cost(self):
        cost = .0

        # Highway cost
        for highway_point in self.highway:
            if highway_point.next is not None:
                cost += self.highway_cost(highway_point.distance)

        # Exits cost
        for highway_exit in self.exits:
            cost += self.exit_cost(highway_exit.distance)

        # Inconsistent highway penalty
        cost += self.calculate_inconsistent_penalty()

        return cost

    def randomize(self):
        for i, highway_point in enumerate(self.highway):
            self.randomize_highway_point(i)

        self.calculate_exits()
        self.update_highway_points_connections()

    def randomize_highway_point(self, i):
        highway_point = self.highway[i]
        highway_point.position.x = rnd.randint(0, config.MAX_X)
        highway_point.position.y = rnd.randint(0, config.MAX_X)

        allowed_indices = list(range(-1, len(self.highway)))
        allowed_indices.remove(i)
        random_highway_point = rnd.choice(allowed_indices)

        if random_highway_point != -1:
            highway_point.next = self.highway[random_highway_point]

        else:
            highway_point.next = None

    def calculate_exits(self):
        self.exits = list()

        highway_parts = self.__get_highway_parts()

        for city in self.cities:
            min_distance = config.MAX_DISTANCE
            highway_exit = HighwayExit(Point(), city, None)

            for line, highway_point in highway_parts:
                tmp_point = self.__closest_point_on_line(city, line)
                distance = math.hypot(tmp_point.x - city.x, tmp_point.y - city.y)
                if distance < min_distance:
                    min_distance = distance
                    highway_exit.position = tmp_point
                    highway_exit.highway_point = highway_point

            self.exits.append(highway_exit)

        self.__check_exits()

    def __get_highway_parts(self):
        parts = []

        for highway_point in self.highway:
            if highway_point.next:
                p1 = highway_point.position
                p2 = highway_point.next.position
                parts.append(((p1, p2), highway_point))

        return parts

    def __closest_point_on_line(self, point, line):
        p1 = np.array([line[0].x, line[0].y])
        p2 = np.array([line[1].x, line[1].y])
        p3 = np.array([point.x, point.y])

        n = p2 - p1
        v = p3 - p1
        z = p1 + n * (np.dot(v, n) / np.dot(n, n))

        new_point = Point(z[0], z[1])

        # replace new point if it is outside segment
        if new_point.x < min(p1[0], p2[0]):
            new_point = Point(*min(p1, p2, key=lambda p: p[0]))
        elif new_point.x > max(p1[0], p2[0]):
            new_point = Point(*max(p1, p2, key=lambda p: p[0]))
        elif new_point.y < min(p1[1], p2[1]):
            new_point = Point(*max(p1, p2, key=lambda p: p[1]))
        elif new_point.y > max(p1[1], p2[1]):
            new_point = Point(*max(p1, p2, key=lambda p: p[1]))

        return new_point

    def __check_exits(self):
        for exit1 in self.exits:
            for exit2 in self.exits:
                if (
                        exit1.position.distance(exit2.position) < self.exit_distance
                        and exit1.highway_point == exit2.highway_point
                ):
                    avq_position = Point(
                        (exit1.position.x + exit2.position.x) / 2.0,
                        (exit1.position.y + exit2.position.y) / 2.0
                    )
                    exit1.position = exit2.position = avq_position

    def update_highway_points_connections(self):
        for highway_point in self.highway:
            highway_point.connections = set()

        for highway_point_1 in self.highway:
            for highway_point_2 in self.highway:
                if highway_point_1.next == highway_point_2:
                    highway_point_1.connections.add(highway_point_2)
                    highway_point_2.connections.add(highway_point_1)

    def calculate_inconsistent_penalty(self):
        penalty = .0
        checked_pairs = []

        for highway_point1 in self.highway:
            for highway_point2 in self.highway:
                if (
                        {highway_point1, highway_point2} not in checked_pairs
                        and not self.__check_if_path_exists(highway_point1, highway_point2, set())
                ):
                    penalty += config.INCONSISTENT_PENALTY
                checked_pairs.append({highway_point2, highway_point1})

        return penalty

    def __check_if_path_exists(self, highway_point1, highway_point2, used_points=set()):
        used_points.add(highway_point1)

        if highway_point1 == highway_point2:
            return True
        if not highway_point1.connections:
            return False
        if highway_point2 in highway_point1.connections:
            return True
        for connected_point in highway_point1.connections - used_points:
            if self.__check_if_path_exists(connected_point, highway_point2, used_points):
                return True

        return False

    def __str__(self):
        return 'Cities: {}\nHighway: {}'.format(self.cities, self.highway)
