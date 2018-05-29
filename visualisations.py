import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3D


def plot_r(components):
    fig = plt.figure()
    fig.suptitle("r / number of components")
    ax = fig.add_subplot(111)
    ax.set_xlabel('number of components')
    ax.set_ylabel('r parameter')

    x = [c[0] for c in components]
    y = [c[1] for c in components]
    ax.plot(x, y, '-', linewidth=2)
    plt.draw()

def plot_R_euler(components):
    fig = plt.figure()
    fig.suptitle("R / Euler characteristic")
    ax = fig.add_subplot(111)
    ax.set_xlabel('Euler characteristic')
    ax.set_ylabel('R parameter')

    x = [c[0] for c in components]
    y = [c[1] for c in components]
    ax.plot(x, y, '-', linewidth=2)
    plt.draw()


def plot_R_homology(homologies):
    fig = plt.figure()
    fig.suptitle("R / Betti numbers")
    fig.show()
    ax = fig.add_subplot(111)
    ax.set_xlabel('Betti numbers')
    ax.set_ylabel('R parameter')

    x = [c[0] for c in homologies]
    y_0 = [c[1][0] for c in homologies]
    y_1 = [c[1][1] for c in homologies]
    y_2 = [c[1][2] if len(c[1]) > 2 else 0 for c in homologies]
    ax.plot(x, y_0, ls=':', c='r', linewidth=1, label="Betti 0")
    ax.plot(x, y_1, ls='-', c='b', linewidth=2, label="Betti 1")
    ax.plot(x, y_2, ls=':', c='g', linewidth=1, label="Betti 2")

    plt.legend()
    plt.draw()


def plot_points(points, edges=None, R=None):
    fig = plt.figure()
    fig.suptitle("Sensors on the sphere")
    ax = fig.add_subplot(111, projection='3d')

    x = [p[0] for p in points]
    y = [p[1] for p in points]
    z = [p[2] for p in points]

    (x_sph, y_sph, z_sph) = drawSphere(0, 0, 0, 0.95)

    ax.plot_surface(x_sph, y_sph, z_sph, color='#6080D0E0')
    #ax.plot_wireframe(x_sph, y_sph, z_sph, color='#6080D0E0')
    ax.scatter(x, y, z, color='k', s=20)
    ax.set_aspect("equal")

    if edges is not None:
        # add the edges between points, conneted in VR complex
        for e in edges:
            xs = [points[e[0]][0], points[e[1]][0]]
            ys = [points[e[0]][1], points[e[1]][1]]
            zs = [points[e[0]][2], points[e[1]][2]]
            ax.add_line(Line3D(xs, ys, zs, color='r'))

    if R is not None:
        # add the sensor coverage spheres
        for p in points:
            (x_sph, y_sph, z_sph) = drawSphere(p[0], p[1], p[2], R)
            ax.plot_wireframe(x_sph, y_sph, z_sph, color='r')

    plt.draw()


def show():
    plt.show()

def drawSphere(xCenter, yCenter, zCenter, r):
    # draw sphere
    u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    # shift and scale sphere
    x = r * x + xCenter
    y = r * y + yCenter
    z = r * z + zCenter
    return (x, y, z)
