#!/usr/bin/env python

import sys
sys.path.append("/home/boisgera/DISKS/VOYAGER/SANDBOX/ACSAN")

from filters import *
from spectrum import *

from pylab import *

#-------------------------------------------------------------------------------
# Tex Matplotlib Configuration
#-------------------------------------------------------------------------------
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

df = 44100.0
dt = 1.0 / df
fc = 8000.0

N = 31
n1 = arange(N)
h1 = low_pass(fc=fc, dt=dt)(N)

f1 = arange(0, df/2, 10.0)
fft_h1 = abs(F(h1, dt=dt)(f1))

#t = arange(1000) * dt
#fi = 2000.0 + 8000.0 * (t / 1000.0 / dt)
#s = round_(sin(fi*t))

#s = sin(arange(100)/100.0 * 2*pi)
s = []
s = r_[s, sin(arange(50)/50.0 * 2 * pi)]
s = r_[s, sin(arange(25)/25.0 * 2 * pi)]

s = r_[s, sin(arange(12)/12.0 * 2 * pi)]
s = r_[s, sin(arange(12)/12.0 * 2 * pi)]
s = r_[s, sin(arange(12)/12.0 * 2 * pi)]


s = r_[s, sin(arange(4)/4.0 * 2 * pi)]
s = r_[s, sin(arange(4)/4.0 * 2 * pi)]
s = r_[s, sin(arange(4)/4.0 * 2 * pi)]
s = r_[s, sin(arange(4)/4.0 * 2 * pi)]
s = r_[s, sin(arange(4)/4.0 * 2 * pi)]
s = r_[s, sin(arange(4)/4.0 * 2 * pi)]
s = r_[s, sin(arange(4)/4.0 * 2 * pi)]
s = r_[s, sin(arange(4)/4.0 * 2 * pi)]
s = r_[s, sin(arange(4)/4.0 * 2 * pi)]
s = r_[s, sin(arange(4)/4.0 * 2 * pi)]
s = r_[s, sin(arange(4)/4.0 * 2 * pi)]
s = r_[s, sin(arange(4)/4.0 * 2 * pi)]
s = r_[s, sin(arange(4)/4.0 * 2 * pi)]
s = r_[s, sin(arange(4)/4.0 * 2 * pi)]
s = r_[s, sin(arange(4)/4.0 * 2 * pi)]
s = r_[s, sin(arange(4)/4.0 * 2 * pi)]




t = arange(len(s))*dt

s2 = dt * convolve(s, h1)

#-------------------------------------------------------------------------------
# Plots
#-------------------------------------------------------------------------------

fig = gcf()

plot(n1, h1, "k.", markersize=2.0)
vlines(n1, 0*h1, h1, linewidth=0.5)

title(r"$h^{31}_n = 1.6\times 10^4 \,  \mbox{sinc} \, 1.6 \times 10^4 (n - 15), \; n \in \{0, \cdots, 31\}$")

#text(6, 20000, "$h^{31}_n = 16000 \,  \mbox{sinc} \, 16000 (n - 15), \; n \in \{0, \cdots, 30\}$")
xlabel("n")
#plot([-1, 1000], [0,0], "k-", linewidth=0.5);

#annotate("$|\mathcal{F}(x)(f)|$", 
#         xy=(-1/dt/4, abs(F(s, dt=dt)(-1/dt/4))), xytext=(-0.394/dt, max(fft_c)*0.8),
#         arrowprops=dict(arrowstyle="-", linewidth=0.25))
#text(1.40 / dt, 0.04*max(fft_c), "$f$ (Hz)")

grid(True)
yticks([-10000, 0, 10000, 20000])
axis([0, N, -2*fc*0.3, 2*fc*1.1])
gcf().subplots_adjust(top=0.8)

#------------------------------------------------------------------------------
# Figure Export
#------------------------------------------------------------------------------

# (w, h) = fig.get_size_inches()
width_cm = 12.0#12.0
width_in = width_cm / 2.54
ratio = 3.0 # 1.618 # thin 
fig.set_size_inches((width_in, width_in / ratio))


save_pdf_svg("low_pass_fig1")

#------------------------------------------------------------------------------
# Plots
#------------------------------------------------------------------------------

clf()

plot(f1, fft_h1, "k-", linewidth=0.75)
#plot([-1, 1000], [0,0], "k-", linewidth=0.5);

plot([0, 8000, 8000, df/2], [1.0, 1.0, 0.0, 0.0], "k", linewidth=0.75)

#annotate("$|\mathcal{F}(h)(f)|$", 
#         xy=(-1/dt/4, abs(F(s, dt=dt)(-1/dt/4))), xytext=(-0.394/dt, max(fft_c)*0.8),
#         arrowprops=dict(arrowstyle="-", linewidth=0.25))
text(20000, -0.15, "$f$ (Hz)")
text(11000, 0.7, "$|\mathcal{F}(h^{31})(f)|$")
grid(True)
yticks([0.0, 0.5, 1.0])
axis([0, df/2, -0.2, 1.2])

#------------------------------------------------------------------------------
# Figure Export
#------------------------------------------------------------------------------

# (w, h) = fig.get_size_inches()
width_cm = 12.0#12.0
width_in = width_cm / 2.54
ratio = 3.0 # 1.618 # thin 
fig.set_size_inches((width_in, width_in / ratio))

save_pdf_svg("low_pass_fig2")

#------------------------------------------------------------------------------
# Plots
#------------------------------------------------------------------------------

clf()
fig = gcf()

plot(1000*t, s, "k-", linewidth=0.5)
plot(1000*t, s, "k.", markersize=1.5)

plot(1000*arange(len(s2))*dt, s2, "k-", linewidth=0.5, markersize=2.0)
plot(1000*arange(len(s2))*dt, s2, "k+", linewidth=0.5, markersize=2.0)

axis([0, 1000*t[-1], -1.1, 1.1])
xlabel("$t$ (ms)")
gcf().subplots_adjust(bottom=0.20)
yticks([-1, 0, 1])
grid(False)



#------------------------------------------------------------------------------
# Figure Export
#------------------------------------------------------------------------------

# (w, h) = fig.get_size_inches()
width_cm = 12.0#12.0
width_in = width_cm / 2.54
ratio = 3.0 # 1.618 # thin 
fig.set_size_inches((width_in, width_in / ratio))

save_pdf_svg("low_pass_fig3")


