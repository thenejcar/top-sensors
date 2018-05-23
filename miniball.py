import numpy as np
from random import choice

def circle(boundary_points):
    """
    We are given num boundary points in dimension n.
    When num is less than n+1 we need to find linear subspace
    that contains boundary points and find the bounding
    sphere of dimension p-1 inside that subspace.

    First compute vectors spawning from the first boundary
    point to all others (subspace containing all points).
    Then compute QR decomposition in order to get the 
    orthogonal basis for them and transform coordinates of
    vectors into orthogonal basis. Add vector zero and
    find the bounding circe for these new points using
    method circle_full. 

    Finally transform coordinates back.
    """
    bp = np.asarray(boundary_points)
    num = len(bp)
    # No points are given, circle is undefined.
    if num == 0:
        return None, None
    # One point is a special case.
    if num == 1:
        return 0, boundary_points[0]
    d = len(boundary_points[0])
    assert all(len(p)==d for p in boundary_points), "All points must lie in the same dimension"    
    vectors = (bp-bp[0])[1:].transpose()
    q, r = np.linalg.qr(vectors)
    new_coordinates = np.matmul(q.transpose(), vectors)
    new_coordinates = np.append(new_coordinates, np.zeros((new_coordinates.shape[0], 1)), axis=1)
    r, circle_coordinates = full_circle(new_coordinates.transpose())
    circle_coordinates = np.asarray(circle_coordinates).transpose()
    real_coordinates = np.matmul(q, circle_coordinates)+bp[0]
    return r, np.ndarray.tolist(real_coordinates)


def full_circle(boundary_points):
    """
    Find the smallest circe with boundary_points on the boundary.
    There should be n+1 points on the boundary in dimension n.
    """
    num_points = len(boundary_points)
    dimension = len(boundary_points[0])
    assert num_points == dimension + 1, "Dimension and number of points do not match"
    a = [[2*boundary_points[i][d]-2*boundary_points[0][d] for d in range(dimension)]
          for i in range(1, num_points)]
    b = [sum(boundary_points[i][d]**2-boundary_points[0][d]**2 for d in range(dimension))
         for i in range(1, num_points)]
    result = np.linalg.solve(np.array(a), np.array(b))
    r = sum((boundary_points[0][d]-result[d])**2 for d in range(dimension))**0.5
    return r, np.ndarray.tolist(result)


def miniball(points, boundary_points):
    """Miniball algorithm"""
    if len(points)==0:
        try:
            return circle(boundary_points)
        except:
            return None, None
    dimension = len(points[0])
    if len(boundary_points) == dimension + 1:
        r, c = circle(boundary_points)
    p = choice(points)
    r, c = miniball([point for point in points if point != p], boundary_points)
    if r is not None and sum((p[d]-c[d])**2 for d in range(dimension)) <= r:
        return r, c
    return miniball([point for point in points if point != p], boundary_points + [p])




print(miniball([(-1, 0), (0, 0), (1, 0)], []))
