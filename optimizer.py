from vietoris import vietoris, findComponents
from cech import cech, homology_d
import dionysus


def optimize(points, r, R):
    """
    Removes the sensors, so that the VR and cech complexes are still ok

    :param points: input points
    :param r: Vietoris Rips parameter
    :param R: Cech parameter
    :return: optimized points
    """

    best_solution = (points, None, None)
    best_len = 0 # length of skipped sensors in the best possible solution

    for i in range(0, len(points)):
        for j in range(0, len(points)):
            if i != j:
                for k in range(0, len(points)):
                    if k not in {i, j}:
                        for l in range(0, len(points)):
                            if l not in {i, j, k}:
                                new_points = [p for (ii, p) in enumerate(points) if ii not in {i, j, k, l}]
                                t, sol = check(new_points, r, R)
                                if t:
                                    best_len = 4
                                    best_solution = sol
                                    break # best possible solution found, return
                        if best_len < 4:
                            new_points = [p for (ii, p) in enumerate(points) if ii not in {i, j, k}]
                            t, sol = check(new_points, r, R)
                            if t:
                                best_len = 3
                                best_solution = sol
                        print("k=",k)
                if best_len < 3:
                    new_points = [p for (ii, p) in enumerate(points) if ii not in {i, j}]
                    t, sol = check(new_points, r, R)
                    if t:
                        best_len = 2
                        best_solution = sol
                print("j=", j)
        if best_len < 2:
            new_points = [p for (ii, p) in enumerate(points) if ii != i]
            t, sol = check(new_points, r, R)
            if t:
                best_len = 1
                best_solution = sol
        print("i=", i)

    return best_solution

def optimize_2(points, r, R):
    candidates = []
    for i in range(0, len(points)):
        pts = [p for (j, p) in enumerate(points) if i != j]
        t, sol = check(pts, r, R)
        if t:
            candidates.append(sol)

    for g in range(2, 6):
        new_candidates = []
        for (opt_points, vr, cech) in candidates:
            for i in range(0, len(opt_points)):
                pts = [p for (j, p) in enumerate(opt_points) if i != j]
                t, sol = check(pts, r, R)
                if t:
                    new_candidates.append(sol)
        print("Generation", str(g), " candidates:", len(new_candidates))

def check(points, r, R):
    vr = vietoris(points, r)
    comps = findComponents([s[0] for s in vr[0]], vr[1])
    if len(comps) > 1:
        return False, (points, None, None)

    c = cech(points, R)
    h = homology_d(c)
    if h[0] != 1 or h[1] != 0:
        return False, (points, None, None)

    return True, (points, vr, c)





