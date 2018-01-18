import random as rnd


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

    def __repr__(self):
        return '{{} - {}}'.format(self.position, self.city)


class Model:
    MAX_X = 1000
    MAX_Y = 1000

    def __init__(self, cities, highway_size, exit_distance):
        self.cities = cities
        self.exit_distance = exit_distance

        self.highway = [HighwayPoint() for _ in range(highway_size)]
        self.exits = []

    def randomize(self):
        for i, highway_point in enumerate(self.highway):
            highway_point.position.x = rnd.randint(0, self.MAX_X)
            highway_point.position.y = rnd.randint(0, self.MAX_X)

            allowed_indices = list(range(-1, len(self.highway)))
            allowed_indices.remove(i)
            random_highway_point = rnd.choice(allowed_indices)

            if random_highway_point != -1:
                highway_point.next = self.highway[random_highway_point]

            else:
                highway_point.next = None

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
