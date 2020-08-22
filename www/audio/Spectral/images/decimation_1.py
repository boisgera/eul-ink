#!/usr/bin/env python

import sys
sys.path.append("/home/boisgera/DISKS/VOYAGER/SANDBOX/ACSAN")

import matplotlib
from pylab import *

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

from numpy import *
from numpy.fft import *

#-------------------------------------------------------------------------------
# Plots
#-------------------------------------------------------------------------------

fig = gcf()

df = 44100.0
dt = 1.0 / df
N = 128
fc1 = 880.0
fc2 = 15000.0

n = arange(N)
t = n * dt

x = (0.85 * sin(2*pi*fc1*t) + 0.15 * sin(2*pi*fc2*t))* hanning(N)

vlines(1000.0 * t, 0.0*x, x, "k", linewidth=0.5)
plot(1000.0 * t, x, "k.", markersize=2.0)
#axis([0, n1[-1], 1e-5, 1e0])
grid(True)


gca().text(0.5, 0.5, "$x(t)$", horizontalalignment="center")
#ylabel("signal value $x(t)$")

xlabel("time $t$ (ms)")
gcf().subplots_adjust(bottom=0.20)


# (w, h) = fig.get_size_inches()
width_cm = 12.0#12.0
width_in = width_cm / 2.54
ratio = 2.5 # thin 
fig.set_size_inches((width_in, width_in / ratio))

xticks([0.0, 1.0, 2.0, 3.0])
yticks((-1.0, 0.0, 1.0))
axis([0.0, 1000.0*N*dt, -1.1, 1.1])

save_pdf_svg("decimation_1")

#--------------------------------------------------

clf()

x = x[::2]

t2 = t[::2]

vlines(1000.0 * t2, 0.0*x, x, "k", linewidth=0.5)
plot(1000.0 * t2, x, "k.", markersize=2.0)
#axis([0, n1[-1], 1e-5, 1e0])
grid(True)

gca().text(0.5, 0.5, "$(x\downarrow 2)(t)$", horizontalalignment="center")

#gca().text(2, 0.4, "$t$")
#ylabel("signal value $x(t)$")

xlabel("time $t$ (ms)")
gcf().subplots_adjust(bottom=0.20)


# (w, h) = fig.get_size_inches()
width_cm = 12.0#12.0
width_in = width_cm / 2.54
ratio = 2.5 # thin 
fig.set_size_inches((width_in, width_in / ratio))

xticks([0.0, 1.0, 2.0, 3.0])
yticks((-1.0, 0.0, 1.0))
axis([0.0, 1000.0*N*dt, -1.1, 1.1])


save_pdf_svg("decimation_2")

#-----------------------------------------------------------

clf()

n = arange(N)
t = n * dt

x = (0.85 * sin(2*pi*fc1*t) + 0.15 * sin(2*pi*fc2*t))* hanning(N)
x[1::2] = 0

vlines(1000.0 * t, 0.0*x, x, "k", linewidth=0.5)
plot(1000.0 * t, x, "k.", markersize=2.0)
#axis([0, n1[-1], 1e-5, 1e0])
grid(True)


gca().text(0.5, 0.5, "$((x\downarrow 2)\uparrow 2)(t)$", horizontalalignment="center")
#ylabel("signal value $x(t)$")

xlabel("time $t$ (ms)")
gcf().subplots_adjust(bottom=0.20)


# (w, h) = fig.get_size_inches()
width_cm = 12.0#12.0
width_in = width_cm / 2.54
ratio = 2.5 # thin 
fig.set_size_inches((width_in, width_in / ratio))

xticks([0.0, 1.0, 2.0, 3.0])
yticks((-1.0, 0.0, 1.0))
axis([0.0, 1000.0*N*dt, -1.1, 1.1])

save_pdf_svg("expansion-1")

#-----------------------------------------------------------

from spectrum import *

N = len(x)

def dome():
    xticks([-44100.0 *0.5, 44100.0 * 0.25, -0,44100.0 * 0.25, 44100.0 * 0.5])
    yticks([0.0, 0.25, 0.50])
    axis([-0.75*df/2 , 1.25*df/2, -0.00001*1e3, 0.00075*1e3])
    ylabel(r"amplitude $\times 10^{3}$")
    xlabel("frequency $f$ (Hz)")
    # (w, h) = fig.get_size_inches()
    width_cm = 12.0#12.0
    width_in = width_cm / 2.54
    ratio = 2.5 # thin 
    fig.set_size_inches((width_in, width_in / ratio))
    


clf()

x = (0.85 * sin(2*pi*fc1*t) + 0.15 * sin(2*pi*fc2*t))* hanning(N)
f = arange(-1.0, 1.25, 0.0001) * 0.5 * df 

plot(f, 1e3 * abs(F(x, dt=dt)(f)), "k", linewidth=0.75)
rect = Rectangle((0.0, -1.0), 44100.0 *0.5, 2.0, facecolor="#dddddd", linewidth=0.0)
gca().add_patch(rect)

gca().text(-7000, 0.5, "$|x(f)|$", horizontalalignment="center")
annotate("$\Delta f / 2$", 
         xy=(44100.0 / 2.0, 0.0), xytext=(16500, 0.25), 
         horizontalalignment = "center", verticalalignment="center",
         arrowprops=dict(arrowstyle="-", linewidth=0.25, connectionstyle="angle,angleA=90,angleB=135,rad=0"))

dome()

save_pdf_svg("decimation_spectrum-1")

#-----------------
clf()
gca().text(-7000, 0.5, "$|(x\downarrow 2)(f)|$", horizontalalignment="center")

plot(f, 1e3 * abs(F(x[::2], dt=2*dt)(f)), "k", linewidth=0.75)
rect = Rectangle((0.0, -1.0), 44100.0 *0.25, 2.0, facecolor="#dddddd", linewidth=0.0)
gca().add_patch(rect)

annotate("$(\Delta f/2) / 2$", 
         xy=(44100.0 / 4.0, 0.0), xytext=(16500, 0.25), 
         horizontalalignment = "center", verticalalignment="center",
         arrowprops=dict(arrowstyle="-", linewidth=0.25, connectionstyle="angle,angleA=90,angleB=45,rad=0"))

dome()


save_pdf_svg("decimation_spectrum-2")

#--------------------------


clf()
f = arange(-1.0, 1.25, 0.00001) * 0.5 * df 
x[1::2] = 0.0

plot(f, 1e3 * abs(F(x, dt=dt)(f)), "k", linewidth=0.75)
rect = Rectangle((0.0, -1.0), 44100.0 *0.5, 2.0, facecolor="#dddddd", linewidth=0.0)
gca().add_patch(rect)

gca().text(-7000, 0.5, "$|((x\downarrow 2)\uparrow 2)(t)(f)|$", horizontalalignment="center")
annotate("$\Delta f / 2$", 
         xy=(44100.0 / 2.0, 0.0), xytext=(16500, 0.25), 
         horizontalalignment = "center", verticalalignment="center",
         arrowprops=dict(arrowstyle="-", linewidth=0.25, connectionstyle="angle,angleA=90,angleB=135,rad=0"))

dome()

save_pdf_svg("expansion_spectrum")


