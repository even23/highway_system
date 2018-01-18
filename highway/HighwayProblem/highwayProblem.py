from __future__ import print_function

import random

from simanneal import Annealer

from highway.model import Model


class HighwayProblem(Annealer):
    """Test annealer with a highway problem.
    """

    # pass extra data (the distance matrix) into the constructor
    def __init__(self, state: Model):
        super(HighwayProblem, self).__init__(state)  # important!

    def move(self):
        """Chooses new point for highway"""
        i = random.randint(0, len(self.state.highway) - 1)
        self.state.randomize_highway_point(self, i)

    def energy(self):
        """Calculates the length of the route."""

        """TODO"""
