import dionysus
from homology import homology_d
from collections import defaultdict
import numpy as np
import miniball

def optimal_R(points, range_min, range_max):
    """
    Computes the optimal Cech parameter R for the given list of points.
    Parameter needs to be as small as possible and Cech complex needs to have Euler characteristic of 0

    :param points: list of tuples
    :return: the optimal r parameter and list of (r, n_components) tuples
    """

    step = (range_max - range_min) / 100
    homologies = []
    eulers = []

    result = None

    R = range_min
    filtration = dionysus.Filtration()
    simplex_radius = {}
    while R < range_max:
        c, flat = cech(points, R)

        for simplex in flat:
            if tuple(simplex) not in simplex_radius:
                simplex_radius[tuple(simplex)] = R
                filtration.append(dionysus.Simplex(list(simplex), R))

        e = len(c[0]) - len(c[1]) + len(c[2])
        eulers.append(e)

        H = homology_d(c)
        homologies.append((R, H))
        print("R:", R, "H:", H, "e:", e)

        if result is None and H[0] == 1 and H[1] == 0:
            result = (R, c)
            break

        R += step

    return result[0], result[1], homologies, eulers


def cech(S, R):
    """
    Computes the cech complex for the given point cloud S with radius parameter R

    :param S: list of points
    :param R: radius parameter for the complex
    :return: dictionary: dimension -> list of simplices (dionysus objects)
    """
    vr = dionysus.fill_rips(np.array(S), 2, R * 2)
    vr_complex = [list(s) for s in vr if len(s) <= 3]  # only take dimension 2 or lower
    ch_complex = []

    for simplex in vr_complex:
        s_points = [tuple(S[x]) for x in simplex]
        mb = miniball.Miniball(s_points)
        c = mb.center()
        r = np.sqrt(mb.squared_radius())

        if r < R:
            ch_complex.append(simplex)
        # inside = True
        # for a in s_points:
        #     if dist(a, c) > r + 1e-8:
        #         inside = False
        #         break
        # if inside:
        #     ch_complex.append(simplex)


    result = defaultdict(list)
    resultsFlat = []
    for s in ch_complex:
        dim = len(s) - 1
        result[dim].append(tuple(s))
        resultsFlat.append(s)

    return result, resultsFlat


def cech_full_barcode(points, range_min, range_max):
    """
    Computes the dionysus persistence diagram, used to draw the full Cech barcode
    """
    step = (range_max - range_min) / 100
    ctr = 0

    R = range_min
    filtration = dionysus.Filtration()
    simplex_radius = {}
    while R < range_max:
        _, cech_flat = cech(points, R)

        for simplex in cech_flat:
            if tuple(simplex) not in simplex_radius:  # add the simplices that are new
                simplex_radius[tuple(simplex)] = R
                filtration.append(dionysus.Simplex(list(simplex), R))

        R += step

        ctr += 1
        if ctr % 10 == 0:
            print(str(ctr) + "%")

    return dionysus.init_diagrams(dionysus.homology_persistence(filtration), filtration)


def find_cycles_on_surface(f, cutoff, R_max):
    """
    Count the number of cycles that have not died yet. It only looks at the first 'cutoff' ones
    Cutoff is determined from the barcode - cycles that appear later are inside the earth, not on the surface
    """
    count = 0
    pers = dionysus.homology_persistence(f)
    diag = dionysus.init_diagrams(pers, f)

    for (i, pt) in enumerate(diag[1]):  # only check dimension 1
        if i <= cutoff:
            # count the cycles with inf death
            if pt.death > R_max:
                count += 1

    return count


def dist(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))
