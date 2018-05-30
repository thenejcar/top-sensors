from vpython import *


def plot_points(points, text, edges=None, R=None, complex=None):
    if edges is not None:
        title = 'Communication between sensors: ' + text
    elif R is not None:
        title = 'Ranges of the sensors: ' + text
    else:
        title = 'Sensors on the sphere: ' + text

    scene = canvas(title=title,
                   width=800, height=600,
                   center=vector(0, 0, 0), background=color.white)

    for p in points:
        sphere(canvas=scene, pos=to_vector(p), radius=0.02, color=color.black)
        if R is not None:
            sphere(canvas=scene, pos=to_vector(p), radius=R, color=color.red, opacity=0.1)

    if edges is not None:
        for e in edges:
            # also plot the edges between the points
            plot_edge(scene, points, e)

        earth = sphere(canvas=scene, pos=vector(0, 0, 0), radius=1, opacity=0.3,
                       texture=dict(file=textures.earth))
    elif complex is not None:
        for simplices in complex.values():
            for simplex in simplices:
                if len(simplex) == 2:
                    # plot the edge
                    plot_edge(scene, points, simplex)
                elif len(simplex) == 3:
                    # plot the triangle
                    plot_triangle(scene, points, simplex)
        # earth = sphere(canvas=scene, pos=vector(0, 0, 0), radius=1, color=color.cyan, shininess=0.7, opacity=0.2)
    else:
        earth = sphere(canvas=scene, pos=vector(0, 0, 0), radius=1, texture=dict(file=textures.earth))


def plot_edge(scene, points, e):
    a = points[e[0]]
    b = points[e[1]]
    curve(to_vector(a), to_vector(b), color=color.red, radius=0.005, canvas=scene)


def plot_triangle(scene, points, t):
    a = points[t[0]]
    b = points[t[1]]
    c = points[t[2]]

    T = triangle(
        canvas=scene,
        v0=vertex(pos=to_vector(a)),
        v1=vertex(pos=to_vector(b)),
        v2=vertex(pos=to_vector(c)),
        texture=dict(file=textures.gravel, bumpmap=bumpmaps.gravel)
    )


def to_vector(p):
    return vector(p[1], p[2], p[0])
