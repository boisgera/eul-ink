#!/usr/bin/env python

# Python 2.7 Standard Library
from __future__ import division
import gc
import os

# Third-Party Packages
import numpy as np; np.seterr(all="ignore")
import numpy.linalg as la
import scipy.misc
import matplotlib as mpl; mpl.use("Agg")
import matplotlib.pyplot as pp
import matplotlib.patches as pa

# Local
import path

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
    options = {"bbox_inches": "tight"}
    if dpi:
        options["dpi"] = dpi
    cwd = os.getcwd()
    root = os.path.dirname(os.path.realpath(__file__))
    os.chdir(root)
    pp.savefig(name + ".pdf", **options)
    pp.savefig(name + ".png", **options)
    pp.savefig(name + ".pgf", **options)
    pp.savefig(name + ".svg", **options)
    os.chdir(cwd)

def set_ratio(ratio=1.0, bottom=0.1, top=0.1, left=0.1, right=0.1):
    height_in = (1.0 - left - right)/(1.0 - bottom - top) * width_in / ratio
    pp.gcf().set_size_inches((width_in, height_in))
    pp.gcf().subplots_adjust(bottom=bottom, top=1.0-top, left=left, right=1.0-right)

# Paths/Arrows Support
# ------------------------------------------------------------------------------
#def arrows(path, n=1, scale=1.0, color="k"):
#    def vec(c):
#        return np.array([np.real(c), np.imag(c)], dtype=np.float64)
#    ts = np.r_[0.0:n] / n + 0.5 / n
#    l = 0.1 * 0.75 * scale
#    w = 0.7 * l
#    d = 0.0 * l
#    vertices = np.array([[0.0, -w/2], [l, 0.0], [0.0, w/2], [0.0, -w/2]]) - [d, 0.0]
#    for t in ts:
#        z = vec(path(t))
#        dt = 1e-7
#        u = vec((path(t+dt) - path(t)) / dt)
#        u = u / la.norm(u)
#        P = np.array([[u[0], -u[1]], [u[1], u[0]]])
#        vs = [list(np.dot(P, v) + z) for v in vertices]
#        pp.gca().add_patch(pa.Polygon(vs, color=color, ec=color))

# ------------------------------------------------------------------------------
def peano_seq(n=1, seq=None):
    if seq is None:
        seq = [(1,1),(-1,1),(1,1),(1,-1),(-1,-1), (1,-1),(1, 1),(-1,1),(1,1)]
    if n==1:
        return seq
    else:
        seq2 = []
        for (i, j) in seq:
            sseq = [(i*x, j*y) for (x, y) in seq]
            seq2.extend(sseq)
        return peano_seq(n-1, seq2)

def peano_curve(n=1):
    pp.clf()
    seq = peano_seq(n)
    #print len(seq), seq
    ds = []
    for (i, j) in seq:
      ds.append((i/(3**n), j/(3**n)))
    points = [(0,0)]
    for i, d in enumerate(ds):
        x, y = points[-1]
        xn, yn = x+d[0], y+d[1]
        delta = [xn-x, yn-y] 
        points.append([xn, yn])
        pp.text(0.5*x +0.5*xn, 0.5*y + 0.5*yn + 1/12/n, str(i+1), 
                horizontalalignment='center', verticalalignment='center', fontsize=10/n)
        pp.plot([x, xn], [y, yn], "k-o", lw=1.0/n, ms=3.0/n, mew=1.0/n)
        pp.arrow(x, y, 0.5*(xn-x), 0.5*(yn-y), lw=1.0/n, width=0.001/n, ec="k", fc="k")
    pp.axis("equal")
    pp.axis([-0.1,1.1,-0.1,1.1])
    pp.xticks([0,1/3.0, 2/3.0, 1], ["0", "1/3", "2/3", "1"])
    pp.yticks([0,1/3.0, 2/3.0, 1], ["0", "1/3", "2/3", "1"])
    pp.grid(True)
    set_ratio(1.618)
    save("peano" + str(n))          

def koch_seq(n=1, seq=None):
    if seq is None:
        seq = [2,2,2]
    if n == 1:
        return seq
    else:
        seq2 = []
        for c in seq:
            seq2.extend([c, -1, 2, -1])
        return koch_seq(n-1, seq2)

def koch_curve(n=1):
    pp.clf()
    seq = koch_seq(n)
    u = np.exp(1j * (np.pi / 3))
    d = (1.0/3.0)**(n-1)
    a, x0, y0 = -2, 0, 0
    for c in seq:
        a += c
        z1 = (x0 + 1j * y0) + d * u ** a
        #print z1
        x1, y1 = np.real(z1), np.imag(z1)
        pp.plot([x0,x1],[y0,y1], "k-", lw=1.0)#, ms=3.0/n, mew=1.0/n)
        #pp.arrow(x0, y0, 0.5*(x1-x0), 0.5*(y1-y0), lw=1.0/n, width=0.001/n, ec="k", fc="k")
        x0, y0 = x1, y1
    pp.axis("equal")
    l = (np.sqrt(3.0)/2.0)/3.0
    e=0.01
    pp.axis([-e,1+e,-l-e,3*l+e])
    #pp.xticks([0,1/3.0, 2/3.0, 1], ["0", "1/3", "2/3", "1"])
    #pp.yticks([0,1/3.0, 2/3.0, 1], ["0", "1/3", "2/3", "1"])
    #pp.grid(True)
    set_ratio(1.0)
    pp.gca().set_aspect("equal")
    pp.axis("off")
    save("koch" + str(n)) 

def segment():
    pp.clf()
    ratio = 2.0 * 1.618
    set_ratio()
    pp.gca().set_aspect("equal")

    gamma = lambda t: 0*(1-t) + (2+1j)*t
    t = np.linspace(0,1,1000)
    path.draw(gamma, 
              a_s={"t": [0, 0.5, 1.0], "scale":0.05, "aspect":0.7}, 
              lw=1.0)
    #pp.plot(np.real(gamma(t)), np.imag(gamma(t)), "k")
    #arrows(gamma)
    pp.xticks([0, 1, 2])
    pp.yticks([0, 1])
    pp.grid(True)
    pp.axis([-0.1, 2.1, -0.1, 1.1])
    save("segment", dpi=600)

def circle():
    pp.clf()
    ratio = 2.0 * 1.618
    set_ratio()
    pp.gca().set_aspect("equal")

    gamma = lambda t: np.exp(2j*np.pi*t)
    t = np.linspace(0,1,1000)
    path.draw(gamma, 
              a_s={"t": [0, 0.5, 1.0], "scale":0.05, "aspect":0.7}, 
              lw=1.0)
    #pp.plot(np.real(gamma(t)), np.imag(gamma(t)), "k")
    #arrows(gamma)
    pp.xticks([-1, 0, 1])
    pp.yticks([-1, 0, 1])
    pp.grid(True)
    pp.axis([-1.1, 1.1, -1.1, 1.1])
    save("circle", dpi=600)

if __name__ == "__main__":
    segment()
    circle()
    peano_curve(1)
    peano_curve(2)
    for i in range(1, 4+1):
        gc.collect()
        koch_curve(i)


