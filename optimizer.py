from vietoris import vietoris, findComponents
from cech import cech, homology_d
import random
import numpy as np


def optimize_2(points, can_remove, r, R, max=800):
    """
    Very slow optimizer, that covers all possible combinations (n!)
    it skips some combinations that are not possible, but it's still usable only for small cases
    bestu used when we remove as much vertices before calling this

    :param points: list of points to optimize
    :param can_remove: list of vertices, assumed to be save to remove from points
    :param r: vietoris rips parameter r
    :param R: cech parameter R
    :return: list of optimized points
    """
    candidates = []
    for i, rem in enumerate(can_remove):
        pts = [p for p in points if p != rem]
        t, sol = check(pts, r, R)
        if t:
            candidates.append(sol)
        print("\r", i, end="")

    print("\nGeneration 1 candidates:", len(candidates))

    # we remove up to 10 vertices
    for g in range(2, 10):
        new_candidates = []
        for c_i, (opt_points, vr, c) in enumerate(candidates):
            for i, rem in enumerate(can_remove):
                if rem in opt_points:
                    pts = [p for p in opt_points if p != rem]
                    t, sol = check(pts, r, R)
                    if t:
                        new_candidates.append(sol)
                    print("\r", c_i, " ", i, ", candidates:", len(new_candidates), end="                     ")
        print("\nGeneration", str(g), " candidates:", len(new_candidates), end="                     ")
        print()
        if len(new_candidates) > max:
            random.shuffle(new_candidates)
            new_candidates = new_candidates[:max]
            print("shortended the new candidate list to", max)

        if len(new_candidates) > 0:
            candidates = new_candidates
        else:
            print("No improvements, returning what we have")
            break

    print(candidates)

    if len(candidates) == 0:
        return points, cech(points, R), vietoris(points, r)
    # return one of the candidates
    return candidates[0]


def optimize_smart(points, r, R, vr, ch):
    originals = [p for p in points]
    can_remove = [p for p in points]

    # sort the vertices by how close to others they are

    # count how many neighbors they have in radius for R
    distances = {}
    index = {}
    for i, p in enumerate(points):
        count = 0
        for pp in points:
            if dist(p, pp) < R:
                count += 1
        distances[p] = count
        index[p] = i

    points = sorted(points, key=lambda x: distances[x], reverse=True)

    # remove all points that only have 1 or 2 such neighbors
    cutoff = len(points)
    for i, p in enumerate(can_remove):
        if distances[p] <= 2:
            cutoff = i
            break
    can_remove = can_remove[:cutoff]
    print("Removed points that definitely break the Cech complex, remaining:", len(can_remove))

    # find all cutvertices in the vietoris rips complex and remove them from the list
    # algorithm is not very good, because i ran out of time
    cutvertex_indices = []

    for ind in vr[0]:
        ind = ind[0]
        verts = [v[0] for v in vr[0] if v[0] != ind]
        edgs = [e for e in vr[1] if e[0] != ind and e[1] != ind]
        comps = findComponents(verts, edgs)
        if len(comps) > 1:
            cutvertex_indices.append(ind)
        can_remove = [p for p in can_remove if index[p] not in cutvertex_indices]
    print("Removed points that definitely break the Vietoris Rips complex, remaining:", len(can_remove))

    best_solution = (points, None, None)
    if len(can_remove) > 0:
        retries = 80
        miss_threshold = 7

        # randomly try to remove some vertices
        for g in range(0, retries):
            misses = 0
            round_points = [p for p in points]
            round_best = (round_points, None, None)
            while misses < miss_threshold:
                rem = random.choice(can_remove)  # pick one of the points that can be removed
                round_points = [p for p in round_points if p != rem]
                t, sol = check(round_points, r, R)
                if t and len(round_best[0]) > len(sol[0]):
                    round_best = sol
                    if len(round_best[0]) < len(best_solution[0]):
                        print("\nnew global best, len=" + str(len(round_best[0])))
                else:
                    misses = misses + 1
                print("\r%d: %d/%d" % (g, misses, miss_threshold), end="                    ")
            if len(round_best[0]) < len(best_solution[0]):
                best_solution = round_best

    print()
    return best_solution

    # if len(can_remove) <= 0:
    #     print("No points can be removed from the list")
    #     return originals, vr, ch
    # else:
    #     # perform the brute force search with some dropoff on the remaining simplices
    #     print("Performing the brute force search with dropoff on remaining vertices")
    #     opt_points, opt_vr, opt_cech = optimize_2(best_solution[0], can_remove, r, R, 250)
    #
    #     return opt_points, opt_vr, opt_cech


def dist(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))


def check(points, r, R):
    vr = vietoris(points, r)
    comps = findComponents([s[0] for s in vr[0]], vr[1])
    if len(comps) > 1:
        return False, (points, None, None)

    c = cech(points, R)
    h = homology_d(c)
    if h[0] == 1 and h[1] == 0:
        return True, (points, vr, c)
    else:
        return False, (points, None, None)

