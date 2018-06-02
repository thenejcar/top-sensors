from collections import defaultdict

import dionysus
import numpy as np

def optimal_r(points, range_min, range_max):
    """
    Computes the optimal Vietoris-Rips parameter r for the given list of points.
    Parameter needs to be as small as possible and VR complex needs to have 1 component

    :param points: list of tuples
    :return: the optimal r parameter and list of (r, n_components) tuples
    """

    step = (range_max - range_min) / 100
    components_for_r = []

    r = range_min
    while r < range_max:
        vr = vietoris(points, r)

        comps = findComponents([s[0] for s in vr[0]], vr[1])

        components_for_r.append((r, len(comps)))
        if (len(comps) == 1):
            # we found the solution with smallest r
            print("Stopping the loop, r=", r, "n components=", len(comps))
            break

        r += step
    # find the smallest r that has 1 component
    min_r = min(components_for_r, key=lambda x: x[0] if x[1] == 1 else 100 + range_max)[0]

    return min_r, components_for_r


def vietoris(points, r):
    vr = dionysus.fill_rips(np.array(points), 2, r)

    complex = defaultdict(list)
    for s in vr:
        complex[len(s) - 1].append(tuple(s))
    return complex


def findComponents(V, E):
    # zgradi slovar sosedov
    neighbors = {}
    for v in V:
        neighbors[v] = set([])

    for (e1, e2) in E:
        neighbors[e1].add(e2)
        neighbors[e2].add(e1)

    visited = set([])  # visited je set ze obiskanih vozlisc
    components = []  # v components shranimo ze najdene komponente
    for v in V:
        if v not in visited:
            visited.add(v)
            components.append(dfs(v, neighbors, visited))

    return components


# rekurzivno vrne se neobiskana vozlisca iz iste komponente kot je podano vozlisce
def dfs(v, neighbors, visited):
    ret = [v]
    for u in neighbors[v]:
        if u not in visited:
            visited.add(u)
            ret += dfs(u, neighbors, visited)

    return ret
