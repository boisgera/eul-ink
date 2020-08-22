#!/usr/bin/env python
"""
Complex-Step Differentiation
"""

# Python 2.7 Standard Library
from __future__ import division
import os

# Third-Party Packages
import numpy as np; np.seterr(all="ignore")
import numpy.linalg as la
import scipy.misc
import matplotlib as mpl; mpl.use("Agg")
import matplotlib.pyplot as pp
import matplotlib.patches as pa

#
# Matplotlib Configuration & Helper Functions
# ------------------------------------------------------------------------------
#
rc = {
    "text.usetex": True,
    "pgf.preamble": [r"\usepackage{amsmath,amsfonts,amssymb}"], 
    "font.family": "serif",
    "font.serif": [],
    "font.sans-serif": [],
    "legend.fontsize": 10, 
    "axes.titlesize":  10,
    "axes.labelsize":  10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
}
mpl.rcParams.update(rc)

# Use PGF to render PDF with LaTeX fonts of the proper size.
from matplotlib.backends.backend_pgf import FigureCanvasPgf
mpl.backend_bases.register_backend("pdf", FigureCanvasPgf)

# The width of the standard LaTeX document is 345.0 pt.
width_in = 345.0 / 72.0

def save(name, dpi=None):
    options = {}
    if dpi:
        options["dpi"] = dpi
    cwd = os.getcwd()
    root = os.path.dirname(os.path.realpath(__file__))
    os.chdir(root)
    pp.savefig(name + ".pdf", **options)
    pp.savefig(name + ".png", **options)
    pp.savefig(name + ".pgf")
    pp.savefig(name + ".svg")
    os.chdir(cwd)

def set_ratio(ratio, bottom=0.1, top=0.1, left=0.1, right=0.1):
    height_in = (1.0 - left - right)/(1.0 - bottom - top) * width_in / ratio
    pp.gcf().set_size_inches((width_in, height_in))
    pp.gcf().subplots_adjust(bottom=bottom, top=1.0-top, left=left, right=1.0-right)


# TODO: define "path" instead, with the same interface as "plot", 
#       only additional keywords ? Understand the fuck about hw 
#       (hl works as expected)

# TODO: implement with circles and triangles instead ?

def arrows(path, n=1, scale=1.0, color="k"):
    def vec(c):
        return np.array([np.real(c), np.imag(c)], dtype=np.float64)
    ts = np.r_[0.0:n] / n + 0.5 / n
    l = 0.1 * 0.75 * scale
    w = 0.7 * l
    d = 0.0 * l
    vertices = np.array([[0.0, -w/2], [l, 0.0], [0.0, w/2], [0.0, -w/2]]) - [d, 0.0]
    for t in ts:
        z = vec(path(t))
        dt = 1e-7
        u = vec((path(t+dt) - path(t)) / dt)
        u = u / la.norm(u)
        P = np.array([[u[0], -u[1]], [u[1], u[0]]])
        vs = [list(np.dot(P, v) + z) for v in vertices]
        pp.gca().add_patch(pa.Polygon(vs, color=color, ec=color))


# ------------------------------------------------------------------------------

def polyline_approximation(n=3):

    na = 2 * n

    def g(t):
        return np.exp(1j * 2 * np.pi * t) 
    def m(n, t):
        ts = np.array(t, ndmin=1)
        out = []
        for t_ in ts:
            k = int(np.floor(t_ * n))
            s = n * (t_ - k/n)
            out.append((1 - s) *g(k/n) + s* g((k+1)/n))
        out = np.array(out)
        if np.shape(t) == ():
            out = out[0]
        return out
    pp.clf()
    t = np.linspace(0, 1, 1000)
    arrows(g,n=na)
    #aplot(np.real(g(t)), np.imag(g(t)), 4, dspace=0.0, hl=0.1, hw=5.0, c='k', direc="neg")
    pp.plot(np.real(g(t)), np.imag(g(t)), "k", label="$\gamma$")
    m_ = [g(k/n) for k in np.arange(n+1)]
    line = pp.plot(np.real(m_), np.imag(m_), color="k",label="$\mu$")[0]
    line.set_dashes([5, 1])
    arrows(lambda t: m(n, t),n=na)
    #grey = (0.5, 0.5, 0.5)
    line = pp.plot(np.real(m(n, t) - g(t)), np.imag(m(n, t)-g(t)), color="grey", label="$\mu - \gamma$")[0]
    #line.set_dashes([5,1, 1, 1])
    arrows(lambda t: m(n, t) -g(t),n=na, scale=2.5/n, color="grey")
    pp.legend()
    set_ratio(1.618)
    pp.xlim([-2, 2])
    pp.axis("equal")
    pp.ylim([-1.1, 1.1])
    pp.grid(True)
    save("polyline_approximation-{0}".format(n))

if __name__ == "__main__":
    polyline_approximation(n=3)
    polyline_approximation(n=4)
    polyline_approximation(n=5)

