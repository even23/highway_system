import math

DEFAULT_M = 10
MAX_X = 100
MAX_Y = 100
MAX_DISTANCE = math.sqrt(MAX_Y ** 2 + MAX_X ** 2)
INCONSISTENT_PENALTY = 1e100

SHOW_ITERATIONS = False

STEPS = 1000
MAX_TEMPERATURE = 12000.0
MIN_TEMPERATURE = 2.5
UPDATES = 100


def linear_cost(x):
    return x


def exponential_cost(x):
    return 2 ** x - 1
