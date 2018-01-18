import math
import random as rnd

import numpy as np


class Point:
    def __init__(self, x_: int = 0, y_: int = 0):
        self.x = x_
        self.y = y_

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)


class HighwayPoint:
    def __init__(self, position_: Point = None, next_: 'HighwayPoint' = None):
        self.position = position_ or Point()
        self.next = next_

    def __repr__(self):
        next_position = self.next.position if self.next else None

        return '[{} -> {}]'.format(self.position, next_position)


class HighwayExit:
    def __init__(self, position_: Point = None, city_: Point = None):
        self.position = position_ or Point()
        self.city = city_ or Point()

    @property
    def distance(self):
        return math.hypot(self.position.x - self.city.x, self.position.y - self.city.y)

    def __repr__(self):
        return '{{} - {}}'.format(self.position, self.city)


class Model:
    MAX_X = 1000
    MAX_Y = 1000
    MAX_DISTANCE = math.sqrt(MAX_Y ** 2 + MAX_X ** 2)

    def __init__(self, cities, highway_size, exit_distance):
        self.cities = cities
        self.exit_distance = exit_distance

        self.highway = [HighwayPoint() for _ in range(highway_size)]
        self.exits = []

    def randomize_highway_point(self, i):
        highway_point = self.highway[i]
        highway_point.position.x = rnd.randint(0, self.MAX_X)
        highway_point.position.y = rnd.randint(0, self.MAX_X)

        allowed_indices = list(range(-1, len(self.highway)))
        allowed_indices.remove(i)
        random_highway_point = rnd.choice(allowed_indices)

        if random_highway_point != -1:
            highway_point.next = self.highway[random_highway_point]

        else:
            highway_point.next = None

    def randomize(self):
        for i, highway_point in enumerate(self.highway):
            self.randomize_highway_point(i)

    def calculate_exits(self):
        self.exits = list()

        lines = []
        for highway_point in self.highway:
            if highway_point.next:
                p1 = highway_point.position
                p2 = highway_point.next.position
                lines.append((p1, p2))

        for city in self.cities:
            min_distance = self.MAX_DISTANCE
            highway_exit = HighwayExit(Point(), city)

            for line in lines:
                tmp_point = self.closest_point_on_line(city, line)
                distance = math.hypot(tmp_point.x - city.x, tmp_point.y - city.y)
                if distance < min_distance:
                    min_distance = distance
                    highway_exit.position = tmp_point

            self.exits.append(highway_exit)

    def closest_point_on_line(self, point, line):
        p1 = np.array([line[0].x, line[0].y])
        p2 = np.array([line[1].x, line[1].y])
        p3 = np.array([point.x, point.y])

        n = p2 - p1
        v = p3 - p1
        z = p1 + n * (np.dot(v, n) / np.dot(n, n))

        new_point = Point(z[0], z[1])

        if new_point.x < min(p1[0], p2[0]):
            new_point = Point(*min(p1, p1, key=lambda p: p[0]))

        if new_point.x > max(p1[0], p2[0]):
            new_point = Point(*max(p1, p1, key=lambda p: p[0]))

        return new_point

    @staticmethod
    def parse_file_with_cities(filename):
        cities = list()

        with open(filename, 'r') as file:
            for line in file.readlines():
                x, y = map(int, line.split())
                cities.append(Point(x, y))

        return cities

    def __str__(self):
        return 'Cities: {}\nHighway: {}'.format(self.cities, self.highway)
