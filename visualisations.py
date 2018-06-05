import matplotlib.pyplot as plt


def plot_r(components, title):
    fig = plt.figure(figsize=(15, 10))
    fig.suptitle("Number of components in VR complex for " + title)
    ax = fig.add_subplot(111)
    ax.set_xlabel('number of components')
    ax.set_ylabel('r parameter')
    ax.grid(which='major', linestyle='-')
    ax.grid(which='minor', linestyle=':')

    x = [c[0] for c in components]
    y = [c[1] for c in components]
    ax.plot(x, y, '-', linewidth=2)
    plt.draw()

def plot_R_homology(homologies, title):
    fig = plt.figure(figsize=(15, 10))
    fig.suptitle("Betti numbers of Čech complex for " + title)
    fig.show()
    ax = fig.add_subplot(111)
    ax.set_xlabel('Betti numbers')
    ax.set_ylabel('R parameter')
    ax.grid(which='major', linestyle='-')
    ax.grid(which='minor', linestyle=':')

    x = [c[0] for c in homologies]
    y_0 = [c[1][0] for c in homologies]
    y_1 = [c[1][1] for c in homologies]
    ax.plot(x, y_0, ls='-', c='r', linewidth=2, label="Betti 0")
    ax.plot(x, y_1, ls='-', c='b', linewidth=2, label="Betti 1")

    ax.set_ylim(top=100)
    plt.legend()
    plt.draw()


def plot_R_barcode(diagram, infinity, title):
    fig = plt.figure(figsize=(15, 10))
    fig.suptitle("Barcode for " + title)
    fig.show()
    ax = fig.add_subplot(111)
    ax.set_xlabel('radius')
    ax.set_ylabel('components / cycles')

    counter = 0
    for i, dgm in enumerate(diagram):
        for pt in dgm:
            if i == 0:
                if pt.death == float("inf"):
                    ax.arrow(pt.birth, counter, infinity - pt.birth, 0, color='r', shape='full')
                else:
                    ax.plot([pt.birth, pt.death], [counter, counter], c='r')
            elif i == 1:
                if pt.death == float("inf"):
                    ax.arrow(pt.birth, counter, infinity - pt.birth, 0, color='b', shape='full')
                else:
                    ax.plot([pt.birth, pt.death], [counter, counter], c='b')
            counter = counter + 1
    plt.draw()


def show():
    plt.show()
