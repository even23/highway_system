#!/usr/bin/env python
import argparse

from heuristic.highway_problem import HighwayProblem
from model.model import Model
from visualization import init_visualisation


def main():
    parser = argparse.ArgumentParser(description='Highway system')
    parser.add_argument('cities', type=str, help='filename with cities positions')
    parser.add_argument('k', type=int, help='number of highway points')
    parser.add_argument('d', type=float, help='minimal distance between exits')

    args = parser.parse_args()

    cities = Model.parse_file_with_cities(args.cities)
    model = Model(cities, args.k, args.d)

    init_visualisation()

    model.randomize()
    model.calculate_exits()

    run_algorithm(model)


def run_algorithm(model):
    hp = HighwayProblem(model)
    hp.steps = 10
    hp.Tmax = 12000.0
    hp.Tmin = 2.5
    hp.updates = 100
    state, e = hp.anneal()
    print(state)
    print(e)


if __name__ == '__main__':
    main()
