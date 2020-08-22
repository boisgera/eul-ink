#!/usr/bin/env python

import sys
sys.path.append("/home/boisgera/DISKS/VOYAGER/SANDBOX/ACSAN")

from numpy import *
from numpy.fft import *
from pylab import *
from timeit import Timer
from random import uniform
from spectrum import *

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------

def save_pdf_svg(name, dpi=None):
    import matplotlib
    import pylab
    if dpi:
        options = {"dpi": dpi}
    else:
        options = {}
    matplotlib.rc('text', usetex=True)
    matplotlib.rc("font", size=8, family="serif")
    savefig(name + ".pdf", **options)
    #matplotlib.rcdefaults()
    pylab.savefig(name + ".svg")#, **options)

def DFc(f): 
    "Critical Bandwidth (f in Hz)"
    f = ravel(f) / 1000.0
    return 25.0 + 75.0 * (1.0 + 1.4 * f**2) ** 0.69

def sDFc(f): 
    "Critical Bandwidth (f in Hz) -- simplified model"
    return maximum(100.0, 0.2 * f)


#-------------------------------------------------------------------------------
# Plots
#-------------------------------------------------------------------------------
from pylab import *
from matplotlib import rc
rc('text', usetex=True)
rc("font", size=8, family="serif")


#gca().annotate("DFT", xy=(n3[50], r3[50]) , xytext=(10,0.1), 
#                arrowprops=dict(arrowstyle="-", linewidth=0.25))


fig = gcf()

f = logspace(log10(20.0), log10(20000.0), 1000)
loglog(f, DFc(f), "k", linewidth=0.75)
loglog(f, sDFc(f), "k:", linewidth=0.75)

#gca().text(17, 100, "$$T_a(f) = 3.64 \\frac{f}{1000}^{-0.8} - 6.5 \\exp\\left( -0.6 \\left(\\frac{f}{1000} - 3.3\\right)^2\\right) + 10^{-3} \\frac{f}{1000}^4$$", size=6)

grid(True)


ylabel("$\Delta F_c$ (Hz)")
xlabel("frequency $f$ (Hz)")
gcf().subplots_adjust(bottom=0.15)

gca().set_title('Critical Bandwidth')
gcf().subplots_adjust(top=0.90)


#gca().annotate("$500$ Hz", 
#         xy=(500, 100), xytext=(500, 25),
#         horizontalalignment="center",
#         arrowprops=dict(arrowstyle="-", linewidth=0.25))#, connectionstyle="angle,angleA=90,angleB=90"))

gca().text(700, 2000, "$\Delta F_c = 25 + 75 (1 + 1.4 (f/1000.0)^2)^{0.69}$", size=8, horizontalalignment="center")


# (w, h) = fig.get_size_inches()
width_cm = 12.0#12.0
width_in = width_cm / 2.54
ratio = 1.618 #3.0 # 1.618 # thin 
fig.set_size_inches((width_in, width_in / ratio))

axis([20.0, 20000.0, 10.0, 5000.0])
#axis([10, 30000, -20, 120])
#xticks([100.0, 500.0, 5000.0, 10000.0])



save_pdf_svg("DF")

