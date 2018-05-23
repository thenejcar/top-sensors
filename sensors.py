import os
import dionysus
import numpy as np

from miniball import miniball
from components import findComponents
from visualisations import plot_points, plot_r


def optimal_r(points, range_min, range_max):
    """
    Computes the optimal Vietoris-Rips parameter r for the given list of points.
    Parameter needs to be as small as possible and VR complex needs to have 1 component

    :param points: list of tuples
    :return: the optimal r parameter and list of (r, n_components) tuples
    """

    step = (range_max - range_min) / 100
    components_for_r = []

    r = range_min
    while r < range_max:
        vr = dionysus.fill_rips(np.array(points), 2, r)

        V, E = [], []  # list of vertices and edges in the complex
        for s in vr:
            if len(s) == 1:
                V.append(int(list(s)[0]))
            elif len(s) == 2:
                E.append(tuple(s))

        comps = findComponents(V, E)

        components_for_r.append((r, len(comps)))
        r += step
    # find the smallest r that has 1 component
    min_r = min(components_for_r, key=lambda x: x[0] if x[1] == 1 else 100 + range_max)[0]

    return min_r, components_for_r


def cech(S, R):
    """
    Computes the cech complex for the given point cloud S with radius parameter R

    :param S: list of points
    :param R: radius parameter for the complex
    :return: dictionary: dimension -> list of simplices
    """
    vr = dionysus.fill_rips(np.array(S), 3, R * 2)
    vr_complex = [list(s) for s in vr]
    ch_complex = []

    for simplex in vr_complex:
        r, c = miniball([tuple(S[x]) for x in simplex], [])
        if r <= R:
            ch_complex.append(simplex)

    result = {}
    for s in ch_complex:
        dim = len(s) - 1
        if dim in result:
            result[dim].append(tuple(s))
        else:
            result[dim] = [tuple(s)]

    return result


def load_points(filename):
    """
    Splits the contents of the sensors data file into a list of tuples (points)
    :param filename: relative path to the datafile
    :return: list of tuples of floats (coordinates)
    """
    with open(filename, "r") as file:
        # read the whole file (1 line) without the first 2 and last 2 brackets
        string = file.readline()[2:-3]

        # split by points and split each point into 3 numbers
        return [tuple([float(x) for x in point.split(",")]) for point in string.split("},{")]


if __name__ == "__main__":
    for file in os.listdir("data/"):
        print("Computing optimal r and R for coordinates in", file)
        points = load_points("data/" + file)
        plot_points(points)

        r, components = optimal_r(points, 0, 1)
        print("Optimal r for VR complex is %f" % r)
        plot_r(components)
