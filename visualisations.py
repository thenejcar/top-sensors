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
    #y_2 = [c[1][2] if len(c[1]) > 2 else 0 for c in homologies]
    ax.plot(x, y_0, ls=':', c='r', linewidth=1, label="Betti 0")
    ax.plot(x, y_1, ls='-', c='b', linewidth=2, label="Betti 1")
    #ax.plot(x, y_2, ls=':', c='g', linewidth=1, label="Betti 2")

    plt.legend()
    plt.draw()


def show():
    plt.show()
