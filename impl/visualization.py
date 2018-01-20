import matplotlib.pyplot as plt

import config
from model.model import Model


def init_visualisation():
    plt.ion()
    plt.figure(figsize=(6, 5))
    plt.gcf().canvas.set_window_title('Highway System')


def show_model(model: Model, wait_for_action=False):
    plt.axis([0, config.MAX_X, 0, config.MAX_Y])
    plt.title('{} cities, {} highway points, {} iterations'.format(
        len(model.cities), len(model.highway), config.STEPS)
    )
    cities_x = [city.x for city in model.cities]
    cities_y = [city.y for city in model.cities]

    plt.plot(cities_x, cities_y, 'ro', label="cities")

    highway_x = [highway_point.position.x for highway_point in model.highway]
    highway_y = [highway_point.position.y for highway_point in model.highway]
    plt.plot(highway_x, highway_y, 'bo', label="highway point")

    exits_x = [highway_exit.position.x for highway_exit in model.exits]
    exits_y = [highway_exit.position.y for highway_exit in model.exits]
    plt.plot(exits_x, exits_y, 'go', label="exit point")

    for highway_point in model.highway:
        if highway_point.next:
            p1 = highway_point.position
            p2 = highway_point.next.position
            plt.plot([p1.x, p2.x], [p1.y, p2.y], 'k-', label="highway")

    for highway_exit in model.exits:
        p1 = highway_exit.position
        p2 = highway_exit.city
        plt.plot([p1.x, p2.x], [p1.y, p2.y], 'k--', label="exit")

    ax = plt.gca()
    box = ax.get_position()
    ax.set_position([box.x0 - 0.05, box.y0, box.width * 5 / 6., box.height])

    plt.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.)

    if wait_for_action:
        plt.draw()
        plt.waitforbuttonpress()
    else:
        plt.pause(0.000001)
        plt.clf()
