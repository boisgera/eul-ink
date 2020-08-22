#!/usr/bin/env python

import sys
sys.path.append("/home/boisgera/DISKS/VOYAGER/SANDBOX/ACSAN")

from numpy import *
from numpy.fft import *
from pylab import *
from timeit import Timer
from random import uniform
from spectrum import *

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

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------

def ATH(f): 
    "Absolute Threshold in Quiet (f in Hz)"
    f = ravel(f) / 1000.0
    return 3.64 * f ** (-0.8) - 6.5 * exp(-0.6 * (f-3.3) ** 2) + 1e-3 * f ** 4




#-------------------------------------------------------------------------------
# Plots
#-------------------------------------------------------------------------------
#from pylab import *
#from matplotlib import rc
#rc('text', usetex=True)
#rc("font", size=8, family="serif")


#gca().annotate("DFT", xy=(n3[50], r3[50]) , xytext=(10,0.1), 
#                arrowprops=dict(arrowstyle="-", linewidth=0.25))


fig = gcf()

f = logspace(1.0, log10(30000.0), 10000)
semilogx(f, ATH(f), "k")

gca().text(17, 100, "$$T_a(f) = 3.64 \\frac{f}{1000}^{-0.8} - 6.5 \\exp\\left( -0.6 \\left(\\frac{f}{1000} - 3.3\\right)^2\\right) + 10^{-3} \\frac{f}{1000}^4$$", size=6)

grid(True)

#xticks((-df/2, 0, df/2, df))

rect = Rectangle((1.0, -5.1), 100000, 93+5.1, facecolor="#eeeeee", linewidth=0.0)
gca().add_patch(rect)
ylabel("SPL $L$ (dB)")
xlabel("frequency $f$ (Hz)")
gcf().subplots_adjust(bottom=0.15)

gca().set_title('Absolute Threshold of Hearing (ATH)')
gcf().subplots_adjust(top=0.90)

#plot(0*ravel([-1/dt/2, -1/dt/2]), [0.0, 50.0], "k:", linewidth=0.5)
#plot(2*ravel([1/dt/2, 1/dt/2]), [0.0, 50.0], "k:", linewidth=0.5)

##xlabel("frequency $f$ (Hz)")
#annotate("$|\mathcal{F}(x)(f)|$", 
#         xy=(-1/dt/4, abs(F(s, dt=dt)(-1/dt/4))), xytext=(-0.394/dt, max(fft_c)*0.8),
#         arrowprops=dict(arrowstyle="-", linewidth=0.25))
#text(1.40 / dt, 0.04*max(fft_c), "$f$ (Hz)")

## text(1.2 / dt, 0.5*max(fft_c), "$\Delta f = {0}$ kHz".format(df/1000))

#annotate("$f=\Delta f$", 
#         xy=(1/dt, 1.155 * max(fft_c)), xytext=(1.15 / dt, 1.1 * max(fft_c)),
#         arrowprops=dict(arrowstyle="-", linewidth=0.25))

##annotate("$f=\Delta f/2$", 
##         xy=(0.5/dt, 1.155 * max(fft_c)), xytext=(0.5 * 1.25/ dt, 1.09 * max(fft_c)),
##         arrowprops=dict(arrowstyle="-", linewidth=0.25))

#annotate("$|\hat{x}_k|$", 
#         xy=(f_N[1], fft_N[1]), xytext=(1.2*f_N[2], 1.0 * max(fft_c)),
#         arrowprops=dict(arrowstyle="-", linewidth=0.25, connectionstyle="angle,angleA=90,angleB=30"))

# axis([ -0.6 / dt, 1.6 / dt, 0.0, max(fft_c)*1.4])

# (w, h) = fig.get_size_inches()
width_cm = 12.0#12.0
width_in = width_cm / 2.54
ratio = 1.618 #3.0 # 1.618 # thin 
fig.set_size_inches((width_in, width_in / ratio))


axis([10, 30000, -20, 120])
#yticks((-1.0, 0.0, 1.0))



save_pdf_svg("ATH")

