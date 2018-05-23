import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_r(components):
    fig = plt.figure()
    fig.suptitle("r / number of components")
    plt.xlabel('number of components')
    plt.ylabel('r')

    x = [c[0] for c in components]
    y = [c[1] for c in components]
    plt.plot(x, y, '-', linewidth=2)
    plt.show()


def plot_points(points):
    fig = plt.figure()
    fig.suptitle("Sensors on the sphere")
    axis3d = Axes3D(fig)

    x = [p[0] for p in points]
    y = [p[1] for p in points]
    z = [p[2] for p in points]
    axis3d.scatter(x, y, z)
    plt.show()
