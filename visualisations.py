import matplotlib.pyplot as plt
import matplotlib.patches as mptch

def scale_fonts():
    SMALL_SIZE = 15
    MEDIUM_SIZE = 17
    BIGGER_SIZE = 19

    plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

def plot_r(components, title):
    fig = plt.figure(figsize=(15, 10))
    scale_fonts()
    fig.suptitle("Number of components in VR complex for " + title)
    ax = fig.add_subplot(111)
    ax.set_ylabel('number of components')
    ax.set_xlabel('r parameter')
    ax.grid(which='major', linestyle='-')
    ax.grid(which='minor', linestyle=':')

    x = [c[0] for c in components]
    y = [c[1] for c in components]
    ax.plot(x, y, '-', linewidth=2)
    plt.draw()
    fig.savefig("images/plot_vr_" + title + ".pdf", bbox_inches='tight')


def plot_R_homology(homologies, title):
    fig = plt.figure(figsize=(15, 10))
    scale_fonts()
    fig.suptitle("Betti numbers of Čech complex for " + title)
    fig.show()
    ax = fig.add_subplot(111)
    ax.set_ylabel('Betti numbers')
    ax.set_xlabel('R parameter')
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
    fig.savefig("images/plot_cech_" + title + ".pdf", bbox_inches='tight')


def plot_R_barcode(diagram, infinity, title):
    fig = plt.figure(figsize=(15, 10))
    scale_fonts()
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

    plt.legend(handles=[mptch.Patch(color='r', label="Components"), mptch.Patch(color='b', label="Cycles")])
    plt.draw()
    fig.savefig("images/barcode_" + title + ".pdf", bbox_inches='tight')


def show():
    plt.show()
