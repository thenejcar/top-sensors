import numpy as np
from math import sqrt, sin, cos, exp, pi
import random
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from mpl_toolkits.mplot3d import Axes3D


random.seed(1)


class Point:
    """
    Representation of a point in spherical coordinates.
    """
    def __init__(self, r, phi, th):
        self.r = r
        self.phi = phi
        self.th = th


def create_random_points(n, r):
    """
    Randomly distribute n points on sphere.
    :param n: number of points
    :param r: radium of sphere
    :return: list of Points
    """
    return [Point(r, random.uniform(0,1)*2*pi, random.uniform(0,1)*pi) for _ in range(n)]


def euclidean(p1, p2):
    """
    Calculate euclidean distance in spherical coordinates.
    :param p1: First Point(r, phi, th)
    :param p2: Second Point(r, phi, th)
    :return: euclidean distance calculated in spherical coordinates
    """
    return sqrt(p1.r**2 + p2.r**2 - 2*p1.r*p2.r*(sin(p1.th)*sin(p2.th)*cos(p1.phi-p2.phi)+cos(p1.th)*cos(p2.th)))


def energy(points):
    """
    Calculates Electrostatic-Energy of all points on sphere.
    :param points: list of points
    :return: Electrostatic-Energy without actual physics constants, unit [m**-1]
    """
    E = 0
    n = len(points)
    for i in range(0, n):
        p1 = points[i]
        for j in range(i+1, n):
            p2 = points[j]
            E += 1/abs(euclidean(p1, p2))
    return E


def sphere_optimisation(points, sigma, T, dT, N0=1000, N_max=10000):
    """
    Redistributes random points on sphere in a way that Electrostatic-Energy
    achieves its minimum, based on simulated annealing in combination with
    Monte-Carlo.
    :param points: Randomly distributed list of points on sphere.
    :param sigma: Variance parameter for Gaussian distribution.
    :param T: Initial Temperature of our system.
    :param dT: Step for decreasing T, T -> T-dT
    :param N0: Maximum number of accepted moves for each T.
    :param N_max: Maximum number of iterations for each T.
    :return: List of evenly distributed points on sphere.
    """
    Ec = energy(points)
    print(Ec)
    while T > 0:
        n_iter = 0
        N_accepted = N0
        while N_accepted > 0 and n_iter < N_max:
            n_iter += 1
            point = random.choice(points[1:])  # let one point intact
            dphi = np.random.normal(0, sigma)
            dth = np.random.normal(0, sigma/2)

            point.phi += dphi
            point.th += dth
            En = energy(points)
            dE = En-Ec
            print(T, Ec, dE, N_accepted, n_iter)

            if dE < 0:
                Ec = En
                N_accepted -= 1
                continue
            else:
                r1 = random.uniform(0,1)
                if r1 < exp(-dE/T):
                    Ec = En
                    N_accepted -= 1
                    continue
                else:
                    point.phi -= dphi
                    point.th -= dth
        T -= dT
    return points


def visualize_points(opt_points, r):
    phis = []
    thetas = []
    for p in opt_points:
        phis.append(p.phi)
        thetas.append(p.th)

    coss = np.cos
    sinn = np.sin
    phi, theta = np.mgrid[0.0:pi:100j, 0.0:2.0*pi:100j]
    x = r*sinn(phi)*coss(theta)
    y = r*sinn(phi)*sinn(theta)
    z = r*coss(phi)

    xx = r*coss(phis)*sinn(thetas)
    yy = r*sinn(phis)*sinn(thetas)
    zz = r*coss(thetas)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(
        x, y, z,  rstride=1, cstride=1, color='c', alpha=0.3, linewidth=0)

    ax.scatter(xx,yy,zz,color="k",s=20)

    ax.set_xlim([-r,r])
    ax.set_ylim([-r,r])
    ax.set_zlim([-r,r])
    ax.set_aspect("equal")
    plt.tight_layout()
    plt.show()

R = 3
rpoints = create_random_points(50, R)
opt_points = sphere_optimisation(rpoints, 0.05, 10, 0.1)
visualize_points(opt_points, R)
