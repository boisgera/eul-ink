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


def smooth():
    pp.clf()
    ratio = 2 * 1.618
    set_ratio(ratio, bottom=0.15)
    pp.axis([-1, 5, -0.1, 1.1])
    #pp.xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    pp.yticks([0.0, 1.0])

    x = np.linspace(-1, 5, 1000)
    y = np.exp(-1.0 / x) * (x > 0)
    pp.plot(x, y, "k-")

    save("smooth", dpi=600)

if __name__ == "__main__":
    smooth()

