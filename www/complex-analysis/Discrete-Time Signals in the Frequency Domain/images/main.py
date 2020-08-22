#!/usr/bin/env python

# Python 2.7 Standard Library
from __future__ import division
import sys

# Third-Party Packages
import numpy as np; np.seterr(all="ignore")
import matplotlib as mpl; mpl.use("Agg")
import matplotlib.pyplot as pp

# Matplotlib Configuration
# ------------------------------------------------------------------------------
rc = {
    "text.usetex": True,
    "pgf.preamble": [r"\usepackage{amsmath,amsfonts,amssymb}"], 
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
def save(name, dpi=None):
    if dpi:
        options = {"dpi": dpi}
    else:
        options = {}
    pp.savefig(name + ".pdf", **options)
    pp.savefig(name + ".png", **options)
    pp.savefig(name + ".pgf")
    pp.savefig(name + ".svg")


def set_ratio(ratio, bottom=0.1, top=0.1, left=0.1, right=0.1):
    height_in = (1.0 - left - right)/(1.0 - bottom - top) * width_in / ratio
    pp.gcf().set_size_inches((width_in, height_in))
    pp.gcf().subplots_adjust(bottom=bottom, top=1.0-top, left=left, right=1.0-right)

# ------------------------------------------------------------------------------

from numpy import linspace, exp, pi, abs, angle

df = 8000.0
dt = 1.0 / df
N = 1000
f = linspace(0.0, df/2, N)
z_f = exp(1j * 2 * pi * f * dt)
h_f = z_f / (z_f - 0.5)

pp.clf()
pp.plot(f, abs(h_f), "k")
pp.xticks([0.0, 1000.0, 2000.0, 3000.0, 4000.0])
pp.yticks([0.0, 0.5, 1.0, 1.5, 2.0])
pp.xlabel(r"$f$ in Hz")
pp.ylabel(r"$|h(f)|$")
pp.title(r"AR Filter Frequency Response -- Magnitude")
pp.axis([0.0, 4000.0, 0.0, 2.1])
pp.grid(True)

set_ratio(2.0, bottom=0.2, left=0.15)
save("amplitude")

pp.clf()
pp.plot(f, angle(h_f), "k")
pp.xticks([0.0, 1000.0, 2000.0, 3000.0, 4000.0])
pp.yticks([-3*pi/16,-pi/8, -pi/16, 0], [r"$-3\pi/16$", r"$-2\pi/16$", r"$-\pi/16$", "0"])
pp.xlabel(r"$f$ in Hz")
pp.ylabel(r"$\mathrm{arg} \,  h(f)$ in rad")
pp.title(r"AR Filter Frequency Response -- Phase")
pp.axis([0.0, 4000.0, -3*pi/16, 0.0])
pp.grid(True)

set_ratio(2.0, bottom=0.2, left=0.15)
save("phase")
pp.clf()

# ------------------------------------------------------------------------------

def x_pm(z):
   inside = np.abs(z) <= 1
   outside = np.abs(z) > 1
   x_p = 1.0 / (1j * 2 * np.pi) * (np.log(z - 1j) - np.log(z + 1j)) + 1.0
   x_m = 1.0 / (1j * 2 * np.pi) * np.log(1 - 2j / (z + 1j))
   return inside * x_p + outside * x_m

def x_r(r, f, dt=1.0):
    if r == 0:
        return 0.5 * np.ones_like(f)
    else:
        z = r * np.exp (1j * 2 * np.pi * f * dt)
        return x_pm(z) - x_pm(1/np.conj(z)) # 1/conj gets weird when r=0, generates
    # a Nan

#def P(r, theta):
#    return (1 - r*r) / (1 -2*r*np.cos(2*np.pi*theta)+ r*r)

dt = 1.0
f = np.linspace(-0.75, 0.75, 1000, endpoint=True)

pp.clf()
#pp.text(-0.25, 4.0, r"$\frac{1-r^2}{1 - 2r\cos 2\pi f + r^2}$", va="center", ha="center", fontsize=10)
pp.plot([-10, 10], [0, 0], "k:", lw=0.5)
pp.plot([0, 0], [-10, 10], "k:", lw=0.5)
pp.axis([-0.55, 0.55, -0.1, 1.1])
pp.xticks([-0.5, 0, 0.5])
pp.grid(True)

#pp.plot(f, np.real(x_r(r=0.0, f=f)), color="0.75", label="$r=0.0$")
#pp.plot(f, np.real(x_r(r=0.5, f=f)), color="0.625", label="$r=0.5$")
#pp.plot(f, np.real(x_r(r=0.75, f=f)), color="0.5", label="$r=0.75$")
#pp.plot(f, np.real(x_r(r=0.875, f=f)), color="0.25", label="$r=0.875$")
#pp.plot(f, np.real(x_r(r=0.9375, f=f)), color="0.0", label="$r=0.9375$")

pp.plot(f, np.real(x_r(r=0.0, f=f)), color="0.875", label=r"$r=0$")
pp.plot(f, np.real(x_r(r=0.5, f=f)), color="0.75", label=r"$r=1 - 2^{-1}$")
pp.plot(f, np.real(x_r(r=0.75, f=f)), color="0.5", label=r"$r=1 - 2^{-2}$")
pp.plot(f, np.real(x_r(r=0.875, f=f)), color="0.25", label=r"$r=1 - 2^{-3}$")
pp.plot(f, np.real(x_r(r=0.9375, f=f)), color="0.0", label=r"$r=1 - 2^{-4}$")

#pp.plot(theta, P(r=0.0, theta=theta), color="0.75", label="$r=0$", lw=1.0)
#pp.plot(theta, P(r=0.20, theta=theta), color="0.625", label="$r=1/5$", lw=1.0)
#pp.plot(theta, P(r=1.0/3.0, theta=theta), color="0.5", label="$r=1/3$", lw=1.0)
#pp.plot(theta, P(r=0.5, theta=theta), color="0.25", label="$r=1/2$", lw=1.0)
#pp.plot(theta, P(r=2.0/3.0, theta=theta), color="0.0", label="$r=2/3$", lw=1.0)
set_ratio(np.sqrt(3), bottom=0.15, top=0.125)
pp.xlabel(r"normalized frequency $f_n = f / \Delta f$")
pp.ylabel(r"$x_r(f)$")
pp.title(r"Low-Pass Filter Frequency Response")
pp.legend(loc="lower center")
save("low-pass-filter", dpi=600)
pp.clf()
# ------------------------------------------------------------------------------


def P(r, theta):
    return (1 - r*r) / (1 -2*r*np.cos(2*np.pi*theta)+ r*r)

theta = np.linspace(-1.0, 1.0, 1000, endpoint=True)

pp.text(-0.25, 4.0, r"$\frac{1-r^2}{1 - 2r\cos 2\pi f_n + r^2}$", va="center", ha="center", fontsize=10)
pp.plot([-10, 10], [0, 0], "k:", lw=0.5)
pp.plot([0, 0], [-10, 10], "k:", lw=0.5)
pp.axis([-0.5, 0.5, -0.5, 5.5])
#pp.grid(True)
pp.plot(theta, P(r=0.0, theta=theta), color="0.875", label=r"$r=0$", lw=1.0)
pp.plot(theta, P(r=0.5, theta=theta), color="0.75", label=r"$r=1-2^{-1}$", lw=1.0)
pp.plot(theta, P(r=0.75, theta=theta), color="0.5", label=r"$r=1-2^{-2}$", lw=1.0)
pp.plot(theta, P(r=1-2**(-3), theta=theta), color="0.25", label=r"$r=1 -2^{-3}$", lw=1.0)
pp.plot(theta, P(r=1-2**(-4), theta=theta), color="0.00", label=r"$r=1 - 2^{-4}$", lw=1.0)
set_ratio(np.sqrt(3), bottom=0.15, top=0.02)
pp.xticks([-0.5, 0, 0.5])
pp.xlabel(r"normalized frequency $f_n = f / \Delta f$")
pp.ylabel(r"$x_r(f)/\Delta t$")
#pp.ylabel(r"$P(r,\theta)$")
#pp.title(r"Poisson Kernel")
pp.legend()
save("poisson-kernel-2", dpi=600)
pp.clf()


