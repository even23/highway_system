class Point:
    def __init__(self, x_: int = 0, y_: int = 0):
        self.x = x_
        self.y = y_


class HighwayPoint:
    def __init__(self, position_: Point = None, next_: 'HighwayPoint' = None):
        self.position = position_ or Point()
        self.next = next_


class HighwayExit:
    def __init__(self, position_: Point = None, city_: Point = None):
        self.position = position_ or Point()
        self.city = city_ or Point()


class Model:
    def __init__(self, n, k, d):
        self.n = n
        self.k = k
        self.d = d

        self.cities = [Point() for _ in range(n)]
        self.highway = [HighwayPoint() for _ in range(k)]
        self.exits = []
