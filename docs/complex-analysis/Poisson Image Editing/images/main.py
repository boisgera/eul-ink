#!/usr/bin/env python
"""
Poisson Image Editing
"""

# Python 2.7 Standard Library
from __future__ import division
import os

# Third-Party Packages
import numpy as np; np.seterr(all="ignore")
import matplotlib as mpl; mpl.use("Agg")
import matplotlib.pyplot as pp

# Local Packages
import fourier

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


# Poisson Image Editing
# ------------------------------------------------------------------------------

def P(r, theta):
    return (1 - r * r) / (1 - 2 * r * np.cos(theta) + r * r)

def poisson_kernel():
    theta = np.linspace(-np.pi, np.pi, 1000, endpoint=True)

    pp.text(-3, 4.5, r"$\displaystyle P(r e^{i \theta}) = \frac{1-r^2}{1 - 2r\cos \theta + r^2}$", fontsize=10)
    pp.plot([-10, 10], [0, 0], "k:", lw=0.5)
    pp.plot([0, 0], [-10, 10], "k:", lw=0.5)
    pp.axis([-np.pi, np.pi, -0.5, 5.5])
    #pp.grid(True)
    pp.plot(theta, P(r=0.0, theta=theta), color="0.75", label="$r=0$", lw=1.0)
    pp.plot(theta, P(r=0.20, theta=theta), color="0.625", label="$r=1/5$", lw=1.0)
    pp.plot(theta, P(r=1.0/3.0, theta=theta), color="0.5", label="$r=1/3$", lw=1.0)
    pp.plot(theta, P(r=0.5, theta=theta), color="0.25", label="$r=1/2$", lw=1.0)
    pp.plot(theta, P(r=2.0/3.0, theta=theta), color="0.0", label="$r=2/3$", lw=1.0)
    set_ratio(np.sqrt(3), bottom=0.15, top=0.02)
    pp.xticks([-np.pi, -np.pi/2, 0.0, np.pi / 2, np.pi], 
              [r"$-\pi$", r"$-\pi/2$","$0$",r"$\pi/2$", r"$\pi$"])
    pp.xlabel(r"angle $\theta$")
    pp.legend()
    save("poisson-kernel", dpi=600)

def gradient():
    N = fourier.N
    i = np.r_[0:N]
    j = np.r_[0:N]
    I, J = np.meshgrid(i, j, indexing="ij")
    X, Y = fourier.xy(I, J, N)
    image = np.c_[0.5 + 0.25 * (X + Y), 0.95 * np.ones_like(X)]
    fourier.save(image, "gradient.png")

if __name__ == "__main__":
    poisson_kernel()
    fourier.dirichlet(n=3)
    gradient()
    fourier.analytic()


