#!/usr/bin/env python

# Python 2.7 Standard Library
from __future__ import division
import os

# Third-Party Packages
import numpy as np; np.seterr(all="ignore")
import matplotlib as mpl; mpl.use("Agg")
import matplotlib.pyplot as pp

# Audio Package
from audio.quantizers import Uniform, mulaw

# Local Libraries
from floating import *

#
# Matplotlib Configuration
# ------------------------------------------------------------------------------
#
rc = {
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": [],      # use latex default serif font
    "font.sans-serif": [], # use a specific sans-serif font
    "legend.fontsize": 10, # "medium" make it 10 (equivalent)
    "axes.titlesize":  10,
    "axes.labelsize":  10,
    "xtick.labelsize": 10, # alt: "small",
    "ytick.labelsize": 10, # alt: "small",
}
mpl.rcParams.update(rc)

# Use PGF to render PDF with LaTeX fonts of the proper size.
from matplotlib.backends.backend_pgf import FigureCanvasPgf
mpl.backend_bases.register_backend("pdf", FigureCanvasPgf)

# The width of the standard LaTeX document is 345.0 pt.
width_in = 345.0 / 72.0


# Helper Functions
# ------------------------------------------------------------------------------
#
def save(name, dpi=None, prefix=""):
    if dpi:
        options = {"dpi": dpi}
    else:
        options = {}
    pp.savefig(prefix + name + ".pdf", **options)
    pp.savefig(prefix + name + ".png", **options)
    pp.savefig(prefix + name + ".pgf")
    pp.savefig(prefix + name + ".svg")


def set_ratio(ratio, bottom=0.1, top=0.1, left=0.1, right=0.1):
    height_in = (1.0 - left - right)/(1.0 - bottom - top) * width_in / ratio
    pp.gcf().set_size_inches((width_in, height_in))
    pp.gcf().subplots_adjust(bottom=bottom, top=1.0-top, left=left, right=1.0-right)


# Floating-Point Numbers
# ------------------------------------------------------------------------------

toy = FloatingPoint(3, 4)

i = range(0, (2**3-1) << 4) 
j = range(1<<7, (1<<7) + ((2**3-1) << 4))

pp.grid(True)

pp.plot(i, toy.decode(i), "k.", markersize=0.75)
pp.plot(j, toy.decode(j), "k.", markersize=0.75)
pp.plot(0, 0, "k.", markersize=5)
pp.plot(112, 16, "k.", markersize=5)
pp.plot(128, 0, "k.", markersize = 5)
pp.plot(240, -16, "k.", markersize=5)

pp.gca().text(5, 2, "$0^+$")
pp.gca().text(112.5, 13, "$+\infty$")
pp.gca().text(117, 1, "$\\bot$")
pp.gca().text(132, -4, "$0^-$")
pp.gca().text(240.5, -15.5, "$-\infty$")
pp.gca().text(245, 1, "$\\bot$")

pp.xticks([0, 112, 128, 240, 256])
pp.yticks(range(-16, 17, 16))

pp.axis([-4, 259, -18, 18])

save("float")


# Mu-Law
# ------------------------------------------------------------------------------
pp.clf()
codes = np.arange(0,256)
pp.plot(codes, mulaw.decode(codes), "k+", markersize=2.0)

pp.xticks(np.arange(0,257,32))
pp.yticks(np.arange(-1.0, 1.1, 0.25))
pp.grid(True)

pp.axis([0, 256, -1.0, 1.0])
set_ratio(2.5)

save("mu-law-decode-final")

#-------------------------------------------------------------------------------
pp.clf()
data = np.arange(0.0, 0.05, 0.00001)
pp.plot(data, mulaw.encode(data), "k.", markersize=0.05)
pp.xticks(np.arange(0.0,0.051,0.01))
pp.yticks(np.arange(0,257,8))
pp.grid(True)
pp.axis([0.0, 0.05, 192, 256])
set_ratio(2.5)
save("mu-law-encode-final")


# Uniform Quantizer
# ------------------------------------------------------------------------------

pp.clf()
x = np.arange(np.pi + np.pi/2, np.pi + 2*np.pi - np.pi/2 + np.pi/2 + np.pi/4, 0.001)
pp.xticks([-1, 20])
pp.yticks([-1.0, 0.0, 1.0])

q = Uniform(-1.0, 1.0, N=7)
f = lambda x: 1.1 * np.sin(x) * np.exp(-np.abs(x-3*np.pi/2)**2/10.0)
z = f(x)

pp.plot(x, z, "k-", linewidth=0.75, label="original")#, markersize = 1.0, markeredgewidth=0.1)
pp.plot(x, q(z), "k.", markersize=0.1, linewidth=0.1, label="quantized")#, markersize = 0.01, markeredgewidth=0.01)

a =2*np.pi+0.6 # 0.6
pp.gca().annotate("original number $x$", xy=(a, f(a)) , xytext=(5.0,0.75), arrowprops=dict(arrowstyle="-", linewidth=0.5,
connectionstyle="angle,angleA=0,angleB=135,rad=0"))
a =2*np.pi+0.6 # 1.4
pp.gca().annotate("quantized number $[ x ]$", xy=(a, q(f(a))) , xytext=(7.85,-0.35), arrowprops=dict(arrowstyle="-", linewidth=0.5,
connectionstyle="angle,angleA=0,angleB=-45,rad=0"))

#gca().annotate('arrowstyle', xy=(0, 1),  xycoords='data',
#                xytext=(-50, 30), textcoords='offset points',
#                arrowprops=dict(arrowstyle="->")
#                )

#legend(loc=2)

pp.axis([x[0], x[-1], -1.25, 1.25])
set_ratio(2.5)
save("sin_quant")


