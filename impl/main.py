#!/usr/bin/env python
import argparse

import config
from metaheuristic.simulated_annealing import SimulatedAnnealing
from model.model import Model, parse_file_with_cities, generate_random_cities
from visualization import init_visualisation, show_model


def main():
    parser = argparse.ArgumentParser(description='Highway system')
    parser.add_argument('cities', type=str, help='filename with cities positions, "random" for random cities')
    parser.add_argument('k', type=int, help='number of highway points')
    parser.add_argument('d', type=float, help='minimal distance between exits')
    parser.add_argument('-s', '--steps', type=int, help='steps to perform')
    parser.add_argument('--show', action='store_true', help='show model through iterations')

    args = parser.parse_args()

    if args.show:
        config.SHOW_ITERATIONS = args.show
        init_visualisation()
    if args.steps:
        config.STEPS = args.steps

    if args.cities == 'random':
        cities = generate_random_cities()
    else:
        cities = parse_file_with_cities(args.cities)

    run_algorithm(cities, args.k, args.d)


def run_algorithm(cities, k, d):
    model = Model(cities, k, d)
    model.randomize()

    algorithm = SimulatedAnnealing(model)
    state, energy = algorithm.run()

    show_results(energy, state)


def show_results(energy, state):
    print(state)
    print('Total cost: {}'.format(energy))

    if not config.SHOW_ITERATIONS:
        init_visualisation()

    show_model(state, True)


if __name__ == '__main__':
    main()
