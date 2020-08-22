
# Python 2.7 Standard Library
from __future__ import division

# Third-Party Packages
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pp
import matplotlib.patches as pa

# TODO: path concat.

# TODO: find a replacement for polygon if the path is not closed!

# TODO: come up with a plan for sets, alpha & set operations 
#       (the boundaries should not be alpha'd ?)

# TODO: offset = None -> center of mass.

def arrow(scale=1.0, aspect=1.0, offset=0.5, position=(0,0), angle=0.0, 
          left=True, right=True, **kwargs):
    vertices = [[0,-1/2 * right], [1,0], [0,1/2 * left], [0,-1/2 * right]]
    width = scale
    height = width * aspect
    vertices = np.array(vertices, dtype=np.float64)
    vertices = [np.dot(np.diag([width, height]), v + [-offset, 0]) for v in vertices]
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle),  np.cos(angle)]])
    t = np.array(position, dtype=np.float64)    
    vertices = np.array([np.dot(R,v) + position for v in vertices])
    return vertices

# TODO: draw path itself, then the arrows

def draw(path, arrow_style=None, **kwargs):

    path_style = kwargs.copy()

    # TODO: look out for fc field to enable fill.
    if path_style.get("fill") is None:
        path_style["fill"] = False
    linewidth = None
    if path_style.get("linewidth") is None and path_style.get("lw") is None:
        path_style["linewidth"] = 2.0 # a bit thicker by default.
    linewidth = path_style.get("linewidth") or path_style.get("lw")

    t = path_style.get("t")
    arrow_style = (arrow_style or kwargs.get("a_s") or {}).copy()
    for key in ["t", "a_s"]:
        try:
            del path_style[key]
        except KeyError:
            pass
    if t is None:
        n = path_style.get("n", 1000)
        t = np.linspace(0.0, 1.0, n + 1) 
    t = np.array(t, dtype=np.float64)
    zs = np.array(path(t))
    vs = np.c_[zs.real, zs.imag]
    polyline = pa.Polygon(vs, closed=False, **path_style)
    pp.gca().add_patch(polyline)

    arrow_t = arrow_style.get("t")
    arrow_n = arrow_style.get("n", 1)
    if arrow_t is None and arrow_n is not None:
        if arrow_n:
            arrow_t = np.linspace(0.0, 1.0, arrow_n, endpoint=False) + 0.5 / arrow_n
        else: 
            arrow_t = []
 
    if len(arrow_t):
        arrow_t = np.array(arrow_t, dtype=np.float64)
        dt = 1e-7 * np.ones_like(arrow_t)
        dt[arrow_t==1.0] = -dt[arrow_t==1.0]
        arrow_t_dt = arrow_t + dt
        zs = np.array(path(arrow_t))
        dzs = (np.array(path(arrow_t_dt)) - zs) / dt 
        angles = np.angle(dzs)

        # TODO: deal with start (line) / end (shift arrow).

        if arrow_style.get("color") is None and arrow_style.get("facecolor") is None:
            arrow_style["facecolor"] = path_style.get("color") or \
                                       path_style.get("edgecolor") or \
                                       path_style.get("ec") or \
                                       "black"
        #arrow_style.setdefault("scale", 1.0) 
        vss = []
        for z, angle, t in zip(zs, angles, arrow_t):
            style = arrow_style.copy()
            if t == 0.0 or t == 1.0:
                style["scale"] = 1e-7 * style.get("scale", 1.0)
                style["aspect"] = style.get("aspect", 1.0) / 1e-7
                style["linewidth"] = linewidth
#            elif t == 1.0:
#                style["offset"] = 1.0
            vs = arrow(position=(z.real, z.imag), angle=angle, **style)
            for k in ["n", "t", "scale", "aspect", "offset", "position", "angle", "left", "right"]:
                try:
                    del style[k]
                except KeyError:
                    pass
            arrow_polygon = pa.Polygon(vs, **style)
            pp.gca().add_patch(arrow_polygon)

    return polyline

# ------------------------------------------------------------------------------
def line(initial, terminal):
    initial = np.array(initial)
    terminal = np.array(terminal)
    def _line(t):
        return (1.0 - t) * initial + t * terminal
    return _line

# TODO: angle start/end.
        
def circle(center=0j, radius=1.0):
    def _circle(t):
       return center + radius * np.exp(2j * np.pi * t)
    return _circle

def bezier(point, *points):
    points = list(points)
    _bezier = None
    if len(points) == 0:
        # print "*"
        def _bezier(t):
            # print np.shape(t), np.shape(np.array(len(t) * [point]))
            return np.array(len(t) * [point])
    else:
        # print "**"
        first = [point] + points[:-1]
        last = points
        # print "f/l", first, last
        def _bezier(t):
            # print np.shape(t), np.shape(bezier(*first)(t))
            out = (1.0 - t) * bezier(*first)(t) + t * bezier(*last)(t)
            return out
    return _bezier

def concat(*paths):
    n = len(paths)
    ts = np.linspace(0, 1, n + 1)
    def path(t):
        out = np.zeros_like(t, dtype=np.complex128)
        for i, ti in enumerate(ts[:-1]):
            tt = ts[i+1] 
            #print ti, tt, t, (ti <= t) * (t <= tt)
            wh = (ti <= t) * (t <= tt)
            st = t[wh]
            out[wh] = paths[i]((st - ti) / (tt - ti))
        return out
    return path
    

if __name__ == "__main__":
    # scale = 1/20 nice for drawings inside a unit square
    arrows = {"t": [0, 0.25, 0.75, 1.0], "scale":0.05, "aspect":0.7}
    draw(concat(line(0,1j), line(1j, 1)), arrows=arrows)
#    draw(circle(), arrows=arrows, fill=True, fc=(0.5, 0.5, 0.5, 0.5))
#    draw((lambda t: (circle()(t) + 1.0)), arrows=arrows, fill=True, fc=(0.75, 0.75, 0.75, 0.5))
#    b_style = arrows.copy()
#    b_style["t"] = np.linspace(0,1, 5)
#    draw(bezier(0.75, -1j, -1, 1j, 0.75), arrows=b_style, fill=True, fc="white")
    pp.axis("equal")
    pp.grid(True)
    pp.show()


