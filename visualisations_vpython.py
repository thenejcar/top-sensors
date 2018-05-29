from vpython import *




def plot_points(points, edges=None, R=None):

    if edges is not None:
        title = 'Communication between sensors'
    elif R is not None:
        title = 'Ranges of the sensors'
    else:
        title = 'Sensors on the sphere'

    scene = canvas(title=title,
                    width=800, height=600,
                    center=vector(0, 0, 0), background=color.white)


    for p in points:
        sphere(canvas=scene, pos=vector(p[0], p[1], p[2]), radius=0.02, color=color.black)
        if R is not None:
            sphere(canvas=scene, pos=vector(p[0], p[1], p[2]), radius=R, color=color.red, opacity=0.5)


    if edges is not None:
        for e in edges:
            # also plot the edges between the points
            a = points[e[0]]
            b = points[e[1]]
            curve(vector(a[0], a[1], a[2]), vector(b[0], b[1], b[2]), color=color.red, radius=0.005, canvas=scene)

        earth = sphere(canvas=scene, pos=vector(0, 0, 0), radius=1, color=color.cyan, shininess=0.7, opacity=0.3)
    else:
        earth = sphere(canvas=scene, pos=vector(0, 0, 0), radius=1, color=color.cyan, shininess=0.7, opacity=0.7)


