#!/usr/bin/env python
# coding: utf-8

# Python 2.7 Standard Library
from __future__ import division
import gc
import os

# Third-Party Packages
from numpy import *
import numpy as np; np.seterr(all="ignore")
import numpy.linalg as la
import scipy.misc
import matplotlib as mpl; mpl.use("Agg")
import matplotlib.pyplot as pp
import matplotlib.patches as pa

# Audio
from audio.quantizers import *
import audio.wave
from audio.fourier import F

# Local
#import path

#
# Matplotlib Configuration & Helper Functions
# ------------------------------------------------------------------------------
#
rc = {
    "text.usetex": True,
    "text.latex.unicode": True,
    "pgf.preamble": [r"\usepackage{amsmath,amsfonts,amssymb}"], 
    "font.family": "serif",
    "font.serif": [],
    "font.monospace": ["Computer Modern Typewriter"],
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
#    cwd = os.getcwd()
#    root = os.path.dirname(os.path.realpath(__file__))
#    os.chdir(root)
    pp.savefig(name + ".pdf", **options)
    pp.savefig(name + ".png", **options)
    pp.savefig(name + ".pgf", **options)
    pp.savefig(name + ".svg", **options)
#    os.chdir(cwd)

def set_ratio(ratio=1.0, bottom=0.1, top=0.1, left=0.1, right=0.1):
    height_in = (1.0 - left - right)/(1.0 - bottom - top) * width_in / ratio
    pp.gcf().set_size_inches((width_in, height_in))
    pp.gcf().subplots_adjust(bottom=bottom, top=1.0-top, left=left, right=1.0-right)

# ------------------------------------------------------------------------------

def rice_question():
    x = 100 * ones(12, dtype=int8)
    x[::2] = -100

    #pp.plot(r_[0:len(x)], x, "k",alpha=0.1)
    pp.figure()
    pp.plot(r_[0:len(x)], x, "k+")
    pp.axis([-1,len(x), -150,150])
    pp.xticks(r_[0:len(x)])
    pp.grid(True)
    pp.xlabel(r"$\texttt{i}$")
    pp.ylabel(r"$\texttt{x[i]}$")
    pp.title(r"Repr\'esentation du tableau \texttt{x}")
    set_ratio(2.0)
    save("rice-plot")

def quantization_question():
    pp.figure()
    def f(x):
        return (x>=0) * ((2*x-x*x) * (x <= 1) + ones_like(x) * (x > 1)) +\
               (x < 0) * ((2*x+x*x) * (x>=-1) - ones_like(x) * (x < -1))

    x = np.linspace(-1, 1, 1000)
    pp.plot(x, f(x), "k")
    #pp.plot(x, 2*x, "k--")
    pp.grid(True)
    pp.xlabel(r"$x$")
    pp.ylabel(r"$f(x)$")
    pp.title(r"Fonction Caract\'eristique $f$")
    set_ratio(2.0)
    #pp.axis([-2.2, 2.2, -1.1, 1.1])
    pp.axis("equal")
    pp.gca().set_xlim([-2.2, 2.2])
    pp.xticks([-1,-0.5, 0, 0.5, 1])
    pp.yticks([-1,-0.5, 0, 0.5, 1])
    save("quantization")

def histogram():
    pp.figure()
    x = 2.0 * random.random(size=100000) - 1.0
    #pp.grid()
    pp.hist(x, bins=20, density=True, color="black", histtype="bar", fill=False)
    pp.xticks([-1.0, 0.0, 1.0])
    pp.yticks([0.0, 0.25, 0.5])
    pp.title(r"\texttt{hist(x, bins=20, density=True)}")
    set_ratio(3.0)
    save("histogram")

    uniform = Uniform(low=-1.0, high=1.0, N=2**8)
    n = uniform(x) - x
    #print mean(n*n)
    #print 1.0 / 12 * 2**(-14)
    SNR = 10.0 * log10( mean(x * x) / mean(n * n))
    #print 10.0 * log10( 1.0/ 3.0 / (1.0 / 12 * 2**(-14)))
    #print SNR

def expansion():
    df = 8000; dt = 1.0 / df; T = 3.0; f = 440.0 * 2**2
    t = r_[0.0:T:dt]; n = len(t)
    x = sin(2*pi*f*t)
    audio.wave.write(x, "x.wav", df=df)
    y = zeros(2*n); y[::2] = x
    audio.wave.write(y, "y.wav", df=2*df)
    pp.figure()
    f = r_[-8000:8000:10]
    Fx = F(x, dt=1.0/df, power_of_two=True)
    pp.plot(f, abs(Fx(f)), "k")
    pp.xlabel(u"Fréquence $f$ en Hz")
    pp.ylabel("$|x(f)|$")
    pp.title(u"Transformée de Fourier de $x(t)$ (magnitude)")
    pp.grid(True)
    set_ratio(3.0)
    save("expansion")

if __name__ == "__main__":
    #rice_question()
    #quantization_question()
    histogram()
    expansion()



