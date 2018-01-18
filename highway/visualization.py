import matplotlib.pyplot as plt

from model.model import Model


def init_visualisation():
    plt.ion()
    plt.figure(figsize=(5, 5))


def show_model(model: Model):
    plt.axis([0, model.MAX_X, 0, model.MAX_Y])
    cities_x = [city.x for city in model.cities]
    cities_y = [city.y for city in model.cities]

    plt.plot(cities_x, cities_y, 'ro')

    highway_x = [highway_point.position.x for highway_point in model.highway]
    highway_y = [highway_point.position.y for highway_point in model.highway]
    plt.plot(highway_x, highway_y, 'bo')

    exits_x = [highway_exit.position.x for highway_exit in model.exits]
    exits_y = [highway_exit.position.y for highway_exit in model.exits]
    plt.plot(exits_x, exits_y, 'go')

    for highway_point in model.highway:
        if highway_point.next:
            p1 = highway_point.position
            p2 = highway_point.next.position
            plt.plot([p1.x, p2.x], [p1.y, p2.y], 'k-')

    for highway_exit in model.exits:
        p1 = highway_exit.position
        p2 = highway_exit.city
        plt.plot([p1.x, p2.x], [p1.y, p2.y], 'k--')

    plt.pause(0.1)
    plt.clf()
