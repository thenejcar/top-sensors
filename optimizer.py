from vietoris import vietoris, findComponents
from cech import cech, homology_d
import random

def optimize(points, r, R):
    print("Optimizing", len(points), "points")
    points_random = optimize_random(points, r, R)
    # check if we can optimize the best solution further
    points_optimal = optimize(points_random, r, R)

    return points_optimal

def optimize_2(points, r, R):
    candidates = []
    for i in range(0, len(points)):
        pts = [p for (j, p) in enumerate(points) if i != j]
        t, sol = check(pts, r, R)
        if t:
            candidates.append(sol)
        print("\r",i, end="")
    print("\nGeneration 1 candidates:", len(candidates))
    for g in range(2, 6):
        new_candidates = []
        for c_i, (opt_points, vr, cech) in enumerate(candidates):
            for i in range(0, len(opt_points)):
                pts = [p for (j, p) in enumerate(opt_points) if i != j]
                t, sol = check(pts, r, R)
                if t:
                    new_candidates.append(sol)
                print("\r", c_i, " ", i, "candidates:", len(new_candidates), end="                     ")
        print("\nGeneration", str(g), " candidates:", len(new_candidates), end="                     ")
        print()
        candidates = new_candidates
    print(candidates)

    # return one of the candidates
    return candidates[0][0]


def optimize_random(points, r, R, retries=30, miss_threshold=10):

    best_solution = (points, None, None)
    for g in range(0, retries):
        misses = 0
        pts = [p for p in points]
        while misses < miss_threshold:
            random.shuffle(pts)
            popped = pts.pop()
            t, sol = check(pts, r, R)
            if t and len(best_solution[0]) > len(sol[0]):
                best_solution = sol
                print("\nnew best, len=" + str(len(best_solution[0])) + "\n")
            else:
                pts.append(popped)
                misses = misses + 1
            print("\r%d: %d/%d" % (g, misses, miss_threshold), end="                    ")

    print()
    return best_solution[0]



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





