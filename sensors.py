import os

import random

# import local functions
from visualisations import plot_r, plot_R_homology, show, plot_R_barcode
from visualisations_vpython import draw_earth
from cech import optimal_R, cech_full_barcode
from vietoris import optimal_r, vr_full_barcode
from optimizer import optimize_smart
import numpy as np


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


def save_points(filename, opt_points, r=1):
    phis = []
    thetas = []
    for p in opt_points:
        phis.append(p.phi)
        thetas.append(p.th)

    coss = np.cos
    sinn = np.sin

    xx = r * coss(phis) * sinn(thetas)
    yy = r * sinn(phis) * sinn(thetas)
    zz = r * coss(thetas)
    points = list(zip(xx, yy, zz))
    with open(filename, "wt") as f:
        f.write("{")

        l = len(points)
        for i, p in enumerate(points):
            f.write("{%f,%f,%f}" % tuple(p))
            if i < l - 1:
                f.write(",")
        f.write("}\n")
        f.close()


def generify(points):
    r1 = random.uniform(-0.01, 0.01)
    r2 = random.uniform(-0.01, 0.01)
    r3 = random.uniform(-0.01, 0.01)
    return [(p[0] + r1, p[1] + r2, p[2] + r3) for p in points]


def optimize_points(file, points, r, R, VR, C):
    opt_points, opt_vr, opt_cech = optimize_smart(points, r, R, VR, C)

    if opt_vr is not None and opt_cech is not None:
        redundant = [p for p in points if p not in opt_points]
        print("Redundant sensors: ", redundant)
        print("optimiser used %d/%d points" % (len(opt_points), len(points)))
        draw_earth(opt_points, "optimized " + file, R=R)
        draw_earth(opt_points, "optimized " + file, edges=opt_vr[1])
        save_points("data/optimized_" + file + ".txt", opt_points)
    else:
        print("No redundant sensors detected")


def plot_barcodes():
    # this doesn't need to be run every time, we just need to export the images once
    for file in ["sensors01.txt", "sensors02.txt", "generated01.txt"]:
        points = generify(load_points("data/" + file))

        file = file.split(".")[0]

        print("plotting the barcodes for", file)
        plot_R_barcode(cech_full_barcode(points, 0, 0.5), 0.51, "cech_" + file)
        plot_R_barcode(vr_full_barcode(points, 0, 1), 1.01, "vr_" + file)


if __name__ == "__main__":

    for file in ["sensors01", "sensors02", "generated01"]:
        print()
        print("*****************************************************")
        print("***  " + file)
        print("*****************************************************")

        points = generify(load_points("data/" + file + ".txt"))
        scene = draw_earth(points, file)
        #scene.delete()

        print("Computing the optimal VR complex")
        r, VR, components = optimal_r(points, 0, 1)
        print("Optimal r for VR complex is %f" % r)
        print("num of simplices in the complex 0:", len(VR[0]), "1:", len(VR[1]), " 2:", len(VR[2]))
        plot_r(components, file)
        scene = draw_earth(points, file, edges=VR[1])
        print()
        #scene.delete()

        print("Computing the optimal Čech complex")
        R, C, homologies = optimal_R(points, 0, 0.5)
        print("Optimal R for Cech complex is %f" % R)
        print("num of simplices in the complex 0:", len(C[0]), "1:", len(C[1]), " 2:", len(C[2]))
        plot_R_homology(homologies, file)
        scene = draw_earth(points, file, R=R)
        #scene.delete()
        print()

        # find redundant sensors -- this takes a long time
        optimize_points(file, points, r, R, VR, C)

    # plot the barcodes
    plot_barcodes()

    # show the plots (if not called, they are still saved to pdf files)
    show()


# redundant example for sensors02
# [(0.08153072939427779, -0.0674609629388395, -0.9941234825453283), (0.1045781293942778, -0.023768662938839513, -0.9941234825453283), (0.07954352939427779, 0.06862523706116049, -0.9941234825453283), (0.037590929394277786, 0.09470543706116048, -0.9941234825453283), (-0.011729470605722212, 0.09747993706116048, -0.9941234825453283), (-0.0853248706057222, 0.03626663706116049, -0.9941234825453283), (-0.09158117060572221, -0.012733962938839511, -0.9941234825453283), (-0.07357937060572221, -0.05873546293883951, -0.9941234825453283), (-0.03572717060572222, -0.09047506293883952, -0.9941234825453283), (0.012708149394277786, -0.10018186293883952, -0.9941234825453283), (0.05986782939427778, -0.0854792629388395, -0.9941234825453283), (0.039211029394277785, 0.5632665370611605, -0.8244554825453283), (-0.2349480706057222, 0.5094575370611605, -0.8244554825453283), (-0.4497480706057222, 0.3307975370611605, -0.8244554825453283), (-0.5525980706057223, 0.07102733706116049, -0.8244554825453283), (-0.5183170706057223, -0.2062514629388395, -0.8244554825453283), (-0.3552980706057222, -0.4331504629388395, -0.8244554825453283), (-0.1034540706057222, -0.5541184629388395, -0.8244554825453283)]