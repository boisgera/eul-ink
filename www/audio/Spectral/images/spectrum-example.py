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
    if dpi:
        options = {"dpi": dpi}
    else:
        options = {}
    matplotlib.rc('text', usetex=True)
    matplotlib.rc("font", size=8, family="serif")
    savefig(name + ".pdf", **options)
    #matplotlib.rcdefaults()
    savefig(name + ".svg", **options)

#-------------------------------------------------------------------------------
# Data Generation
#-------------------------------------------------------------------------------

# DEPRECATED - in favor of a deterministic finite signal
# s = ravel([uniform(-1.0, 1.0) for _ in range(N)]) * hanning(10)
s = [0.0, 
     0.072227619384959835, 
     0.25762112500789686, 
     0.18269264449726078, 
     0.27119333307466942, 
     0.29066178042731527, 
     0.49543395742959062, 
     -0.018326747145149536, 
     0.074760148335074397, 
     0.0]
N = len(s)
M = 16 # power of two
s = ravel(s)
df = 8000.0
dt = 1.0 / df

f_N = arange(N) / float(N)  * df
fft_N = abs(F(s, dt=dt, n=N)(f_N))

f_M = arange(M) / float(M) / dt
fft_M = abs(F(s, dt=dt, n=M)(f_M))

f_c = arange(-0.6, 1.6, 0.001) / dt
fft_c = abs(F(s, dt=dt)(f_c))

#-------------------------------------------------------------------------------
# Plots
#-------------------------------------------------------------------------------

fig = gcf()

plot(f_N, fft_N, "k.", markersize=6.0)
vlines(f_N, 0*fft_N, fft_N, linewidth=0.5)

plot(f_c, fft_c, "k", linewidth=0.75)

xticks((-df/2, 0, df/2, df))

rect = Rectangle((-1/dt/2, -30), 1/dt, 60, facecolor="#bbbbbb", linewidth=0.0)
gca().add_patch(rect)

plot(0*ravel([-1/dt/2, -1/dt/2]), [0.0, 50.0], "k:", linewidth=0.5)
plot(2*ravel([1/dt/2, 1/dt/2]), [0.0, 50.0], "k:", linewidth=0.5)


annotate("$|\mathcal{F}(x)(f)|$", 
         xy=(-1/dt/4, abs(F(s, dt=dt)(-1/dt/4))), xytext=(-0.394/dt, max(fft_c)*0.8),
         arrowprops=dict(arrowstyle="-", linewidth=0.25))
text(1.40 / dt, 0.04*max(fft_c), "$f$ (Hz)")



annotate("$f=\Delta f$", 
         xy=(1/dt, 1.155 * max(fft_c)), xytext=(1.15 / dt, 1.1 * max(fft_c)),
         arrowprops=dict(arrowstyle="-", linewidth=0.25))

annotate(r"$\Delta t \times|\hat{x}_k|$", 
         xy=(f_N[1], fft_N[1]), xytext=(1.2*f_N[2], 1.0 * max(fft_c)),
         arrowprops=dict(arrowstyle="-", linewidth=0.25, connectionstyle="angle,angleA=90,angleB=30"))

plot(f_M, fft_M, "kx", markersize=3.5)
axis([ -0.6 / dt, 1.6 / dt, 0.0, max(fft_c)*1.4])



#------------------------------------------------------------------------------
# Figure Export
#------------------------------------------------------------------------------

# (w, h) = fig.get_size_inches()
width_cm = 12.0#12.0
width_in = width_cm / 2.54
ratio = 3.0 # 1.618 # thin 
fig.set_size_inches((width_in, width_in / ratio))




save_pdf_svg("spectrum-example")

#-------------------------------------------------------------------------------

clf()
fig = gcf()

annotate("$x_n$", 
         xy=(2*dt, s[2]), xytext=(0, 1.5*s[2]),
         arrowprops=dict(arrowstyle="-", linewidth=0.25, connectionstyle="angle,angleA=0,angleB=-45"))

t = arange(N)*dt
plot([t[4], t[5]], 0.5*0.5*(s[4]+s[5])*ravel([1,1]),"k", linewidth=0.25 )

text(t[4] + 0.3*(t[5]-t[4]), 1.1 * 0.5*0.5*(s[4]+s[5]), "$\Delta t$")

text(0.92*N*dt, -0.16*max(s),  "$t$ (s)")

vlines(arange(N)*dt, 0*s, 1*s, linewidth=0.75)
plot(arange(N)*dt, s, "k.")
plot([-dt, N*dt], [0,0], "k:", linewidth=0.5)

xticks(t[::2])
axis([-1*dt, N*dt, -max(s)*0.2, max(s)*1.1])

# (w, h) = fig.get_size_inches()
width_cm = 12.0#12.0
width_in = width_cm / 2.54
ratio = 3.0 # 1.618 # thin 
fig.set_size_inches((width_in, width_in / ratio))



save_pdf_svg("spectrum-example-temporal")


