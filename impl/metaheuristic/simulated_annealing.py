from simanneal import Annealer

import config
from model import model
from visualization import show_model


class SimulatedAnnealing(Annealer):
    """Annealer with a highway problem"""

    def __init__(self, state: model):
        super(SimulatedAnnealing, self).__init__(state)

    def run(self):
        self.steps = config.STEPS
        self.Tmax = config.MAX_TEMPERATURE
        self.Tmin = config.MIN_TEMPERATURE
        self.updates = config.UPDATES

        return self.anneal()

    def move(self):
        """Chooses new point for highway"""

        self.state.move()

    def energy(self):
        """Calculates the length of the route"""

        return self.state.calculate_cost()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

        if config.SHOW_ITERATIONS:
            show_model(self.state)
