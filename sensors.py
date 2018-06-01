import os
from collections import defaultdict
import dionysus
import numpy as np
import random

from miniball import miniball
from components import findComponents
from visualisations import plot_r, plot_R_euler, plot_R_homology, show, plot_R_barcode
from visualisations_vpython import plot_points
from homology import homology, homology_d


def optimal_r(points, range_min, range_max):
    """
    Computes the optimal Vietoris-Rips parameter r for the given list of points.
    Parameter needs to be as small as possible and VR complex needs to have 1 component

    :param points: list of tuples
    :return: the optimal r parameter and list of (r, n_components) tuples
    """

    step = (range_max - range_min) / 80
    components_for_r = []

    r = range_min
    while r < range_max:
        V, E = vietoris(points, r)

        comps = findComponents(V, E)

        components_for_r.append((r, len(comps)))
        if (len(comps) == 1):
            # we found the solution with smallest r
            print("Stopping the loop, r=", r, "n components=", len(comps))
            break

        r += step
    # find the smallest r that has 1 component
    min_r = min(components_for_r, key=lambda x: x[0] if x[1] == 1 else 100 + range_max)[0]

    return min_r, components_for_r


def vietoris(points, r):
    vr = dionysus.fill_rips(np.array(points), 2, r)

    V, E = [], []  # list of vertices and edges in the complex
    for s in vr:
        if len(s) == 1:
            V.append(int(list(s)[0]))
        elif len(s) == 2:
            E.append(tuple(s))
    return V, E


def optimal_R(points, range_min, range_max):
    """
    Computes the optimal Cech parameter R for the given list of points.
    Parameter needs to be as small as possible and Cech complex needs to have Euler characteristic of 0

    :param points: list of tuples
    :return: the optimal r parameter and list of (r, n_components) tuples
    """

    step = (range_max - range_min) / 80
    homologies = []



    R = range_min
    filtration = dionysus.Filtration()
    simplex_radius = {}
    while R < range_max:
        c, flat = cech(points, R)

        for simplex in flat:
            if tuple(simplex) not in simplex_radius:
                simplex_radius[tuple(simplex)] = R
                filtration.append(dionysus.Simplex(list(simplex), R))

        # for s in filtration:
        #     print(s, end=", ")
        # print()

        H = homology_d(c)
        homologies.append((R, H))
        print(R, H)
        if H[0] == 1 and H[1] == 0:
            print("My homology says: ", homology(c))

            # we found the solution with smallest R
            print("Stopping the loop, R=", R, "H=", H)
            break
        R += step

    pers = dionysus.homology_persistence(filtration)
    diagram = dionysus.init_diagrams(pers, filtration)

    # find the smallest r that has 0th Betti number 1 and 1st Betti number 0
    min_betti_0 = min(homologies, key=lambda x: x[1][0])[1][0]
    results = [h for h in homologies if h[1][0] == min_betti_0]
    min_betti_1 = min(results, key=lambda x: x[1][1])[1][1]
    results = [h for h in results if h[1][1] == min_betti_1]
    min_R = min(results, key=lambda x: x[0])[0]

    return min_R, homologies, diagram


def cech(S, R):
    """
    Computes the cech complex for the given point cloud S with radius parameter R

    :param S: list of points
    :param R: radius parameter for the complex
    :return: dictionary: dimension -> list of simplices (dionysus objects)
    """
    vr = dionysus.fill_rips(np.array(S), 3, R * 2)
    vr_complex = [list(s) for s in vr if len(s) <= 3]  # only take dimension 2 or lower
    ch_complex = []

    for simplex in vr_complex:
        r, c = miniball([tuple(S[x]) for x in simplex], [])
        if r <= R:
            ch_complex.append(simplex)
        # print("miniball radius:", r, "R:",R)

    #TODO: this algorithm is not working corectly -- cech and vietoris are always the same
    if len(ch_complex) != len(vr_complex):
        print(len(ch_complex))
        print(len(vr_complex))
        print("cech and vietoris are different, you fixed the bug!")

    result = defaultdict(list)
    resultsFlat = []
    for s in ch_complex:
        dim = len(s) - 1
        result[dim].append(tuple(s))
        resultsFlat.append(s)

    return result, resultsFlat


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

def generify(points):
    r1 = random.uniform(-0.01, 0.01)
    r2 = random.uniform(-0.01, 0.01)
    r3 = random.uniform(-0.01, 0.01)
    return [(p[0] + r1, p[1] + r2, p[2] + r3) for p in points]


if __name__ == "__main__":
    for file in os.listdir("data/"):
        print("Computing optimal r and R for coordinates in", file)
        points = load_points("data/" + file)
        points = generify(points)
        plot_points(points, file)

        r, components = optimal_r(points, 0, 1)
        print("Optimal r for VR complex is %f" % r)
        plot_r(components)

        _, E = vietoris(points, r)
        plot_points(points, file, edges=E)

        # for the Cech complex, start with the optimal r (or just below it)
        R, homologies, diagram = optimal_R(points, (r - 0.1) / 2, 0.5)
        print("Optimal R for Cech complex is %f" % R)
        plot_R_homology(homologies)
        plot_R_barcode(diagram)

        K, _ = cech(points, R)
        print(R, "num of simplices in the complex 0:", len(K[0]), "1:", len(K[1]), " 2:", len(K[2]))
        plot_points(points, file, R=R)
        plot_points(points, file, complex=K)

    show()
