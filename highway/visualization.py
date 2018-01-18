import matplotlib.pyplot as plt

from highway.model.Model import Model


def show_model(model: Model):
    plt.axis([0, model.MAX_X, 0, model.MAX_Y])

    cities_x = [city.x for city in model.cities]
    cities_y = [city.y for city in model.cities]

    plt.plot(cities_x, cities_y, 'ro')

    highway_x = [highway_point.position.x for highway_point in model.highway]
    highway_y = [highway_point.position.y for highway_point in model.highway]
    plt.plot(highway_x, highway_y, 'bo')

    for highway_point in model.highway:
        if highway_point.next:
            p1 = highway_point.position
            p2 = highway_point.next.position
            plt.plot([p1.x, p2.x], [p1.y, p2.y], 'k-')
    plt.draw()
    plt.pause(0.5)
    plt.clf()
