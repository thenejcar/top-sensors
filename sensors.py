import os

import random

# import local functions
from visualisations import plot_r, plot_R_homology, show, plot_R_barcode
from visualisations_vpython import draw_earth
from cech import optimal_R, cech_full_barcode
from vietoris import optimal_r, vr_full_barcode


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


def plot_barcodes():
    # this doesn't need to be run every time, we just need to export the images once
    for file in ["data/sensors01.txt", "data/sensors02.txt"]:
        points = generify(load_points(file))
        print("plotting the barcodes for", file)
        plot_R_barcode(cech_full_barcode(points, 0, 0.5), 0.51, "Cech barcode for " + file)
        plot_R_barcode(vr_full_barcode(points, 0, 1), 1.01, "Vietoris rips barcode for " + file)


if __name__ == "__main__":

    for file in os.listdir("data"):
        print()
        print("*****************************************************")
        print("***  " + file)
        print("*****************************************************")

        file = "data/" + file
        points = generify(load_points(file))

        print("Computing the optimal VR complex")
        r, VR, components = optimal_r(points, 0, 1)
        print("Optimal r for VR complex is %f" % r)
        print("num of simplices in the complex 0:", len(VR[0]), "1:", len(VR[1]), " 2:", len(VR[2]))
        plot_r(components, file)
        draw_earth(points, file, edges=VR[1])
        print()

        print("Computing the optimal Čech complex")
        R, C, homologies = optimal_R(points, 0, 0.5)
        print("Optimal R for Cech complex is %f" % R)
        print("num of simplices in the complex 0:", len(C[0]), "1:", len(C[1]), " 2:", len(C[2]))
        plot_R_homology(homologies, file)
        draw_earth(points, file, R=R)
        print()


    plot_barcodes()

    show()
