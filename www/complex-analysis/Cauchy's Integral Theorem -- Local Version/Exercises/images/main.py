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

# Local Packages
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

    "pgf.texsystem": "xelatex"
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

# ------------------------------------------------------------------------------

def fourier():
    def line(a, b):
        def _line(t):
            return (1 - t) * a + t * b
        return _line

    omega = 1
    tau = 2

    gamma = path.concat(
      line(-tau + 1j * omega, tau + 1j * omega),
      line(tau + 1j * omega, tau),
      line(tau, -tau),
      line(-tau, -tau + 1j * omega),
    )

    pp.clf()
    set_ratio(1.618)
    a_s = dict(n=4, scale=2*0.07, aspect=0.7)
    path.draw(gamma, a_s=a_s, lw=1.0)
    pp.axis("equal")
    pp.xticks([0])
    pp.yticks([0])
    #pp.ylim([-0.1, 1.1])

    pp.text(0.25, 0.25, r"$\gamma_0^{\leftarrow}$",
      verticalalignment='center', horizontalalignment='center', fontsize=10)
    pp.text(0.25, 1.25, r"$\gamma$",
        verticalalignment='center', horizontalalignment='center', fontsize=10)
    pp.text(2.25, 0.5, r"$\mu_+^{\leftarrow}$",
        verticalalignment='center', horizontalalignment='center', fontsize=10)
    pp.text(-1.75, 0.5, r"$\mu_{-}$",
        verticalalignment='center', horizontalalignment='center', fontsize=10)
    pp.grid(True)
    save("fourier")


def cauchy_formula_sets():

#    b1 = path.bezier(1.5, 1.5+1j, 1j)
#    b2 = path.bezier(1j, -1.5+1j, -1.5)
#    b3 = path.bezier(-1.5, -1.5-1j, -1j)
#    b4 = path.bezier(-1j, 1.5-1j, 1.5)
#    gamma = path.concat(b1, b2, b3, b4)
   
    l1 = path.line(1.5-1j, 1.5 +1j)
    l2 = path.line(1.5+1j, -1.5 +1j)
    l3 = path.line(-1.5+1j, -1.5 -1j)
    l4 = path.line(-1.5-1j, 1.5 -1j)
    alpha = path.concat(l1, l2, l3, l4)

    l5 = path.line(-0.5j, 0.5j)
    l6 = path.line(0.5j , -1 + 0.5j)
    l7 = path.line(-1 + 0.5j, -1 -0.5j)
    l8 = path.line(-1 - 0.5j, -0.5j)
    beta = path.concat(l5, l6, l7, l8)

    circle = lambda t: 0.75 + 0.99*0.75 * np.exp(1j * 2 * np.pi * t)

    small_circle = lambda t: 0.75 + 0.5 * np.exp(1j * 2 * np.pi * t)


    pp.clf()
    set_ratio(1.618)
    a_s = {"n":0}
    path.draw(alpha, a_s=a_s, lw=1.0, fc=(0.95, 0.95, 0.95), ec=(0.8, 0.8, 0.8), fill=True,
    label=r"$\Omega$")
    path.draw(beta, a_s=a_s, lw=1.0, fc="white", ec=(0.8, 0.8, 0.8), fill=True)
#    path.draw(small_circle, a_s=a_s, lw=0.0, fc=(0.9, 0.9, 0.9), ec=(0.4, 0.4, 0.4), fill=True, 
#    label="$D$")
    a_s.update({"color": "black", "n": 2, "aspect": 0.7, "scale":0.1})
    path.draw(small_circle, a_s=a_s, lw=1.0)

    #pp.plot([1.25], [0], "k-", label=r"$\gamma$")



    pp.plot([0.75], [00], "k+")
    pp.plot([0.5], [-0.25], "k+")
    pp.plot([0.75,1.25], [0,0], "k", lw=0.5)

    pp.text(-0.5, 0.55 + 0.125, r"$\Omega$",
        verticalalignment='center', horizontalalignment='center', fontsize=10)

    pp.text(0.75, 0.5 + 0.125, r"$\gamma$",
        verticalalignment='center', horizontalalignment='center', fontsize=10)

    pp.text(0.75, 0.125, r"$c$",
        verticalalignment='center', horizontalalignment='center', fontsize=10)
    pp.text(1.0, 0.125, r"$r$",
        verticalalignment='center', horizontalalignment='center', fontsize=10)


    pp.text(0.5, -0.125, r"$z$",
        verticalalignment='center', horizontalalignment='center', fontsize=10)

    pp.axis("equal")
    pp.axis([-1.5, 1.5, -1, 1])
#    pp.xticks([-2,-1,0,1,2])
#    pp.yticks([-1,0,1])

    pp.grid(False)
    pp.axis("off")
    #pp.legend()
    save("cauchy_formula_sets")

def cauchy_formula():
    x_0 = 0.5
    eps = np.pi / 16
    r = 0.2
    alpha = -np.pi / 2 - eps
    beta  = -3 * np.pi / 2 + eps
    def small_circle(t):
        angle = (1.0 - t) *alpha + t * beta
        return x_0 + r * np.exp(1j * angle)

    x_m = x_0 - r * np.sin(eps)
    y_m = np.sqrt(1 - x_m * x_m)
    line_1 = path.line(x_0 + r * np.exp(1j * beta), x_m + 1j * y_m)
    line_2 = path.line(x_m - 1j * y_m, x_0 + r * np.exp(1j * alpha))
    phi = np.arctan(y_m / x_m)
    def large_circle(t):
        angle = (1.0 - t) * phi + t * (2 * np.pi - phi)
        return np.exp(1j * angle)
    gamma = path.concat(line_2, small_circle, line_1, large_circle)

    alpha_2 = -np.pi / 2 + eps
    beta_2  =  np.pi / 2 - eps
    def small_circle_2(t):
        angle = (1.0 - t) * beta_2 + t * alpha_2
        return x_0 + r * np.exp(1j * angle)

    x_m = x_0 + r * np.sin(eps)
    y_m = np.sqrt(1 - x_m * x_m)
    line_3 = path.line(x_m + 1j * y_m, x_0 + r * np.exp(1j * beta_2))
    line_4 = path.line(x_0 + r * np.exp(1j * alpha_2), x_m - 1j * y_m)
    phi_2 = np.arctan(y_m / x_m)
    def large_circle_2(t):
        angle = (1.0 - t) * (- phi_2) + t * phi_2
        return np.exp(1j * angle)
    gamma_2 = path.concat(line_3, small_circle_2, line_4, large_circle_2)

    pp.clf()
    set_ratio(1.618)
    a_s = dict(n=4, scale=0.07, aspect=0.7)
    path.draw(gamma, a_s=a_s, lw=1.0)
    path.draw(gamma_2, a_s=a_s, lw=1.0)
    pp.axis("equal")


    #pp.xticks([-1,0,1])
    #pp.yticks([-1,0,1])
#    pp.ylim([-1.1, 1.1])
#    pp.grid(True)

    pp.plot([0.0], [00], "k+")
    pp.plot([0.5], [00], "k+")

    pp.text(0, 0.125, r"$c$",
        verticalalignment='center', horizontalalignment='center', fontsize=10)
    pp.text(0.5, 0.125, r"$z$",
        verticalalignment='center', horizontalalignment='center', fontsize=10)

    pp.text(-0.9, 0, r"$\mu$",
        verticalalignment='center', horizontalalignment='center', fontsize=10)
    pp.text(0.9, 0, r"$\nu$",
        verticalalignment='center', horizontalalignment='center', fontsize=10)


    pp.grid(False)
    pp.axis([-1.05, 1.05, -1.05, 1.05])
    pp.axis("off")
    save("cauchy_formula")

def cauchy_formula_2():

    def circle(c, r):
        def _circle(t):
            return c + r * np.exp(1j * 2 * np.pi * t)
        return _circle

    pp.clf()
    set_ratio(1.618)
    a_s = dict(n=2, scale=0.07, aspect=0.7)
    path.draw(circle(0, 1.0), a_s=a_s, lw=1.0, label=r"$\gamma(1)$")
    path.draw(circle((1-2/3.0) * 0.5, 2/3.0), a_s=a_s, lw=1.0, ls=(0,(5,1)), label=r"$\gamma(2/3)$")
    path.draw(circle((1- 1/3.0) * 0.5, 1/3.0), a_s=a_s, lw=1.0, ls=(0,(3,3)), label="$\gamma(1/3)$")
    pp.plot([0.5], [0.0], "k+")
    pp.axis("equal")
    pp.xticks([-1,0,1])
    pp.yticks([-1,0,1])
    pp.ylim([-1.1, 1.1])
    pp.grid(True)
    pp.legend()
    save("cauchy_formula_2")

if __name__ == "__main__":
    fourier()
    cauchy_formula_sets()
    cauchy_formula()
    cauchy_formula_2()

