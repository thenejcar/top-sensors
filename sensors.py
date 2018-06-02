import os
import random

from visualisations import plot_r, plot_R_homology, show, plot_R_barcode
from visualisations_vpython import draw_earth
from cech import optimal_R, cech_full_barcode, cech
from vietoris import optimal_r, vietoris


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

    # # plot the barcodes
    # # this takes some time
    # for file in ["data/sensors01.txt", "data/sensors02.txt"]:
    #     points = generify(load_points(file))
    #     print("plotting the barcode for cech complex")
    #     plot_R_barcode(cech_full_barcode(points, 0, 0.5), 0.51, file)
    #     show()

    for file in ["data/sensors01.txt", "data/sensors02.txt"]:
        print("Computing optimal r and R for coordinates in", file)
        points = load_points(file)
        points = generify(points)
        #draw_earth(points, file)

        r, components = optimal_r(points, 0, 1)
        print("Optimal r for VR complex is %f" % r)
        plot_r(components)

        vr = vietoris(points, r)
        draw_earth(points, file, edges=vr[1])

        R, K, homologies, eulers = optimal_R(points, 0, 0.5)
        print("Optimal R for Cech complex is %f" % R)
        plot_R_homology(homologies, eulers)

        print(R, "num of simplices in the complex 0:", len(K[0]), "1:", len(K[1]), " 2:", len(K[2]))
        draw_earth(points, file, R=R)
        draw_earth(points, file, complex=K)

    show()
