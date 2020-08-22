#!/usr/bin/env python

# Python 2.7 Standard Library
from __future__ import division
import os

# Third-Party Packages
import numpy as np; np.seterr(all="ignore")
import scipy.misc
import matplotlib as mpl; mpl.use("Agg")
import matplotlib.pyplot as pp

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

def p(z):
    return z ** 3 + z + 1.0

def argument_principle():
    t = np.linspace(0.0, 1.0, 1001)
    p_gamma_t = p(np.exp(1j * 2 * np.pi * t))
    arg_p_gamma_t = np.angle(p_gamma_t)

    pp.clf()
    ratio = 2.0 * 1.618
    set_ratio(ratio, bottom=0.15)
    pp.axis([0, 1.0, -4, 8])
    pp.grid(True)
    pp.xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    pp.yticks([-np.pi, 0.0, np.pi, 2*np.pi], [r"$-\pi$", "0", r"$+\pi$", r"$+2\pi$"])

    #t_inv = np.arange(1.0, 1000.0, 0.01)
    #t = 1 / t_inv
    pp.plot(t, np.unwrap(arg_p_gamma_t), "k--")
    pp.plot(t, arg_p_gamma_t, "k")
    #pp.xlabel("$t$")

    save("argument_principle", dpi=600)
    pp.clf()
    ratio = 2.0 * 1.618
    set_ratio(ratio, bottom=0.15)
    pp.xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    pp.yticks([0, 1, 2, 3, 4])
    pp.axis([0, 1.0, -0.5, 3.5])
    pp.plot(t, np.abs(p_gamma_t), "k")
    pp.grid(True)

    save("modulus", dpi=600)

if __name__ == "__main__":
    argument_principle()

