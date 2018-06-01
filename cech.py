import dionysus
from homology import homology_d
from collections import defaultdict
import numpy as np
from miniball import miniball



def optimal_R(points, range_min, range_max, cutoff):
    """
    Computes the optimal Cech parameter R for the given list of points.
    Parameter needs to be as small as possible and Cech complex needs to have Euler characteristic of 0

    :param points: list of tuples
    :return: the optimal r parameter and list of (r, n_components) tuples
    """

    step = (range_max - range_min) / 100
    homologies = []

    R = range_min
    filtration = dionysus.Filtration()
    simplex_radius = {}
    c = None
    while R < range_max:
        c, flat = cech(points, R)

        for simplex in flat:
            if tuple(simplex) not in simplex_radius:
                simplex_radius[tuple(simplex)] = R
                filtration.append(dionysus.Simplex(list(simplex), R))

        H = homology_d(c)
        homologies.append((R, H))
        print(R, H, end="")
        if H[0] == 1:
            # when we have 1 component, we can start counting the surface cycles
            num_cycles = find_cycles_on_surface(filtration, cutoff, R)
            print("cycles on the surface: ", num_cycles)
            if num_cycles <= 0:
                print("done, there are no more cycles on the surface")
                break
        else:
            print("")

        R += step


    return R, homologies, c


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
        r, c = miniball(s_points, [])
        inside = True
        for a in s_points:
            if dist(a, c) >= r + 1e-8:  #1e-8 is there for some tolerance to imprecise calcaultions
                inside = False
                break
        if inside:
            ch_complex.append(simplex)

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

