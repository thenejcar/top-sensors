from vpython import *


def draw_earth(points, text, edges=None, R=None, complex=None, simplex_centers=None):
    """
    Draws all possible 3d visualisations of sensors on the earth
    :param points:
    :param text:
    :param edges:
    :param R:
    :param complex:
    :param simplex_centers:
    :return:
    """

    if edges is not None:
        title = 'Communication between sensors: ' + text
    elif R is not None:
        title = 'Ranges of the sensors: ' + text
    else:
        title = 'Sensors on the sphere: ' + text

    scene = canvas(title=title,
                   width=800, height=600,
                   center=vector(0, 0, 0), background=color.black)
    scene.lights = []

    d = 5
    light_brightness = 0.5

    scene.lights.append(distant_light(direction=vec(d, d, d), color=color.gray(light_brightness)))
    scene.lights.append(distant_light(direction=vec(d, d, -d), color=color.gray(light_brightness)))
    scene.lights.append(distant_light(direction=vec(d, -d, d), color=color.gray(light_brightness)))
    scene.lights.append(distant_light(direction=vec(d, -d, -d), color=color.gray(light_brightness)))
    scene.lights.append(distant_light(direction=vec(-d, d, d), color=color.gray(light_brightness)))
    scene.lights.append(distant_light(direction=vec(-d, d, -d), color=color.gray(light_brightness)))
    scene.lights.append(distant_light(direction=vec(-d, -d, d), color=color.gray(light_brightness)))
    scene.lights.append(distant_light(direction=vec(-d, -d, -d), color=color.gray(light_brightness)))

    labels = set([])

    for p in points:
        sphere(canvas=scene, pos=to_vector(p), radius=0.02, color=color.red)
        if R is not None:
            sphere(canvas=scene, pos=to_vector(p), radius=R, color=color.green, opacity=0.3)

    if edges is not None:
        for e in edges:
            # also plot the edges between the points
            plot_edge(scene, points, e)

        earth = sphere(canvas=scene, pos=vector(0, 0, 0), radius=1, opacity=0.3,
                       texture=dict(file=textures.earth), shininess=0)
    elif complex is not None:
        for simplices in complex.values():
            for simplex in simplices:
                if len(simplex) == 2:
                    # plot the edge
                    plot_edge(scene, points, simplex)
                    plot_labels(scene, labels, points, simplex)
                elif len(simplex) == 3:
                    # plot the triangle
                    plot_triangle(scene, points, simplex)
        if simplex_centers is not None:
            for (c, r, s_points) in simplex_centers:
                sphere(canvas=scene, pos=to_vector(c), radius=r, opacity=0.3, color=color.blue)
                sphere(canvas=scene, pos=to_vector(c), radius=0.03, opacity=0.4, color=color.green)
                curve(to_vector(c), to_vector(s_points[0]), color=color.green, radius=0.006, opacity=0.4, canvas=scene)
                curve(to_vector(c), to_vector(s_points[1]), color=color.green, radius=0.006, opacity=0.4, canvas=scene)
                curve(to_vector(c), to_vector(s_points[2]), color=color.green, radius=0.006, opacity=0.4, canvas=scene)
    else:
        earth = sphere(canvas=scene, pos=vector(0, 0, 0), radius=1, texture=dict(file=textures.earth), shininess=0)


def plot_edge(scene, points, e):
    a = points[e[0]]
    b = points[e[1]]
    curve(to_vector(a), to_vector(b), color=color.yellow, radius=0.005, canvas=scene)


def plot_triangle(scene, points, t):
    a = points[t[0]]
    b = points[t[1]]
    c = points[t[2]]

    T = triangle(
        canvas=scene,
        v0=vertex(pos=to_vector(a), color=color.yellow, opacity=0.3),
        v1=vertex(pos=to_vector(b), color=color.yellow, opacity=0.3),
        v2=vertex(pos=to_vector(c), color=color.yellow, opacity=0.3),
    )


def plot_labels(scene, labels, points, simplex):
    for p in simplex:
        if p not in labels:
            labels.add(p)
            label(canvas=scene, pos=to_vector(points[p]), text=str(p), xoffset=0.2, yoffset=0.2, background=color.white,
                  color=color.black)


def to_vector(p):
    return vector(p[1], p[2], p[0])
