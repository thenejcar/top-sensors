from collections import defaultdict

import miniball
import numpy as np
import dionysus
import visualisations_vpython as vv

# test ce nam cech pravilno dela

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

    miniballs = []
    for simplex in vr_complex:
        s_points = [tuple(S[x]) for x in simplex]
        mb = miniball.Miniball(s_points)
        c = mb.center()
        r = np.sqrt(mb.squared_radius())
        if len(s_points) == 3:
            miniballs.append((c, r, s_points))

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

    return result, resultsFlat, miniballs


def dist(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))



print()
print()
print()
print()
print()
print()
print("triangles test")
r = 0.275
triangles = [
 (0.6506604615576731, 0.6095438361585862, -0.4478503279952455),
 (0.2761524615576731, 0.8423608361585863, -0.4478503279952455),
 (0.877631461557673, 0.48458383615858625, 0.03494517200475451),
 (0.5352464615576731, 0.8415138361585862, 0.03494517200475451),
 (0.06365446155767306, 0.9906018361585862, 0.03494517200475451),
 (0.8406804615576731, 0.2183568361585862, 0.5105916720047545),
 (0.6304554615576731, 0.5901618361585862, 0.5105916720047545),
 (0.2677124615576731, 0.8156648361585862, 0.5105916720047545)
]

results, results_flat, miniballs = cech(triangles, r)
vv.draw_earth(triangles, "Čech, R=" + str(r), complex=results, R=r)
vv.draw_earth(triangles, "Čech, R=" + str(r), complex=results, simplex_centers=miniballs)

print("breakpoint")
cech(triangles, r)

# print()
# print()
# print()
# print()
# print()
# print("sphere test")
#
#
# def sample_spherical(npoints, ndim=3):
#     vec = np.random.randn(npoints, ndim)
#     return [tuple(row / np.linalg.norm(row)) for row in vec]
#
# points = [tuple(arr) for arr in sample_spherical(10)]
# # vv.draw_earth(points, "20 random points")
# r = 0.7
#
# results, results_flat = cech(points, r)
#
# # print("VR:", vr)
# # vv.draw_earth(points, "VR, r=" + str(r), complex=vr, R=r)
# # print()
#
# print("Cech:", results)
# print(results_flat)
# vv.draw_earth(points, "Čech, R=" + str(r), complex=results, R=r)
# vv.draw_earth(points, "Čech, R=" + str(r), complex=results)
#
# print("breakpoint")
# cech(points, r)
