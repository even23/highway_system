import math
import random

from simanneal import Annealer

from highway.model import Model
from highway.visualization import show_model


def distance(a, b):
    return math.hypot(a.position.x - b.position.x, a.position.y - b.position.y)


class HighwayProblem(Annealer):
    """Test annealer with a highway problem.
    """

    # pass extra data (the distance matrix) into the constructor
    def __init__(self, state: Model):
        super(HighwayProblem, self).__init__(state)  # important!

    def move(self):
        """Chooses new point for highway"""
        i = random.randint(0, len(self.state.highway) - 1)
        self.state.randomize_highway_point(i)
        self.state.calculate_exits()
        # print(self.state)
        show_model(self.state)

    def energy(self):
        """Calculates the length of the route."""
        e = 0
        """Highway cost"""
        for i, highway_point in enumerate(self.state.highway):
            if highway_point.next is not None:
                e += distance(highway_point, highway_point.next)

        return e
