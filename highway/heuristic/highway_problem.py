import random

from simanneal import Annealer

from highway.model import model
from highway.visualization import show_model


class HighwayProblem(Annealer):
    """Test annealer with a highway problem.
    """

    # pass extra data (the distance matrix) into the constructor
    def __init__(self, state: model):
        super(HighwayProblem, self).__init__(state)  # important!

    def move(self):
        """Chooses new point for highway"""
        point_to_move = random.randint(0, len(self.state.highway) - 1)
        self.state.randomize_highway_point(point_to_move)
        self.state.calculate_exits()

        show_model(self.state)

    def energy(self):
        """Calculates the length of the route."""
        energy = 0

        """Highway cost"""
        for highway_point in self.state.highway:
            if highway_point.next is not None:
                energy += self.state.highway_cost(highway_point.distance)

        """Exits cost"""
        for highway_exit in self.state.exits:
            energy += self.state.exit_cost(highway_exit.distance)

        return energy
