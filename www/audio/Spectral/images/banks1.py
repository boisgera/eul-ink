#!/usr/bin/env python

import sys
sys.path.append("/home/boisgera/DISKS/VOYAGER/SANDBOX/ACSAN")

from numpy import *
from numpy.fft import *
from spectrum import *
from filters import low_pass
from h import h_0

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
# Matplotlib Tex Config
#-------------------------------------------------------------------------------
#from matplotlib import rc
#rc('text', usetex=True)
#rc("font", size=8, family="serif")

#-------------------------------------------------------------------------------
# Computations
#-------------------------------------------------------------------------------
window = hanning

N = 64
M = 4
df = 44100.0
dt = 1.0 / df
h0 = low_pass(fc=df/4.0/M, dt = dt, window=hanning)(N)

f_1 = arange(-2.0, 2.0, 0.001) * df/2
f_2 = arange( 0.0, 1.0, 0.001) * df/2

n = arange(-0.5*(N-1), 0.5*(N-1) + 1) 

a0 = h0 * 2 * cos(pi*(0+ 0.5) * n / float(M))
a1 = h0 * 2 * cos(pi*(1+ 0.5) * n / float(M))
a2 = h0 * 2 * cos(pi*(2+ 0.5) * n / float(M))
a3 = h0 * 2 * cos(pi*(3+ 0.5) * n / float(M))

#-------------------------------------------------------------------------------
# Plots
#-------------------------------------------------------------------------------
from pylab import *


fig = gcf()

for i, f_ in enumerate([f_1, f_2]):
    if i == 0:
        marker = "k-"
        width = 0.75
    else:
        marker = "k-"
        width = 0.75
    plot(f_, abs(F(h0, dt=dt)(f_)), "k:", linewidth=0.75)
    plot(f_, abs(F(a0, dt=dt)(f_)), marker, linewidth=width)
    plot(f_, abs(F(a1, dt=dt)(f_)), marker, linewidth=width)
    plot(f_, abs(F(a2, dt=dt)(f_)), marker, linewidth=width)
    plot(f_, abs(F(a3, dt=dt)(f_)), marker, linewidth=width)

# Add grey rectangle OUTSIDE THE CORRECT REGION ? OR IN ?
rect1 = Rectangle((-df/2, -1.0), df/2, 3.0, facecolor="#eeeeee", linewidth=0.0)
gca().add_patch(rect1)
rect2 = Rectangle((df/2, -1.0), df/2, 3.0, facecolor="#eeeeee", linewidth=0.0)
gca().add_patch(rect2)


h = 1.20

f =  - df/16
gca().annotate("$|h(f)|$", xy=(f, abs(F(h0, dt=dt)(f))) , xytext=(f,h), 
horizontalalignment="center",
arrowprops=dict(arrowstyle="-", linewidth=0.5, 
connectionstyle="angle,angleA=90,angleB=45,rad=0"))

f = df/2 - df/16
gca().annotate("$|a_3(f)|$", xy=(f, abs(F(a3, dt=dt)(f))) , xytext=(f,h), 
horizontalalignment="center",
arrowprops=dict(arrowstyle="-", linewidth=0.5, 
connectionstyle="angle,angleA=90,angleB=45,rad=0"))

f = df/2 - 3*df/16
gca().annotate("$|a_2(f)|$", xy=(f, abs(F(a2, dt=dt)(f))) , xytext=(f,h), 
horizontalalignment="center",
arrowprops=dict(arrowstyle="-", linewidth=0.5, 
connectionstyle="angle,angleA=90,angleB=45,rad=0"))

f = df/2 - 5*df/16
gca().annotate("$|a_1(f)|$", xy=(f, abs(F(a1, dt=dt)(f))) , xytext=(f,h), 
horizontalalignment="center",
arrowprops=dict(arrowstyle="-", linewidth=0.5, 
connectionstyle="angle,angleA=90,angleB=45,rad=0"))

f = df/2 - 7*df/16
gca().annotate("$|a_0(f)|$", xy=(f, abs(F(a0, dt=dt)(f))) , xytext=(f,h), 
horizontalalignment="center",
arrowprops=dict(arrowstyle="-", linewidth=0.5, 
connectionstyle="angle,angleA=90,angleB=45,rad=0"))


# Add phase plot too. Notice how phase CANCEL EACH OTHER AT TRANSITIONS !
xlabel("Frequency $f$ (Hz)")
gcf().subplots_adjust(bottom=0.20)

ylabel("Filter Gain")
xticks([-df/2.0, 0.0, df/2.0])
yticks([0.0, 1.0])
grid(True)
axis([-df/8.0, df/2.0 + df/8.0, 0.0, 1.5])


#plot(f_, 20*log10(abs(F_h0(f_))), "k")
#plot(f_, 20*log10(abs(F_h1(f_))), "g")
#plot(f_, 20*log10(abs(F_h2(f_))), "b:")

# (w, h) = fig.get_size_inches()
width_cm = 12.0#12.0
width_in = width_cm / 2.54
ratio = 2.5 
fig.set_size_inches((width_in, width_in / ratio))


save_pdf_svg("banks1")

#-------------------------------------------------------------------------------

clf()

f = arange(0.0, 1.0, 0.0001) * df/2

sp0 = F(a0, dt=dt)
sp1 = F(a1, dt=dt)
sp2 = F(a2, dt=dt)
sp3 = F(a3, dt=dt)

T_0 = abs(sp0(f)*sp0(f) + sp1(f)*sp1(f) + sp2(f)*sp2(f) + sp3(f)*sp3(f) - exp(-1j*2*pi*(N-1)*dt*f))
T_1 = abs(sp0(f)*sp0(f+1*df/4) + sp1(f)*sp1(f+1*df/4) + sp2(f)*sp2(f+1*df/4) + sp3(f)*sp3(f+1*df/4))
T_2 = abs(sp0(f)*sp0(f+2*df/4) + sp1(f)*sp1(f+2*df/4) + sp2(f)*sp2(f+2*df/4) + sp3(f)*sp3(f+2*df/4))
T_3 = abs(sp0(f)*sp0(f+3*df/4) + sp1(f)*sp1(f+3*df/4) + sp2(f)*sp2(f+3*df/4) + sp3(f)*sp3(f+3*df/4))

for i in (0,1,2,3):
    clf()
    f = arange(0.0, 1.0, 0.0001) * df/2

    T = eval("T_%s" % i)
    plot(f, T, "k-", linewidth=0.75)


    rect1 = Rectangle((-df/2, -1.0), df/2, 3.0, facecolor="#eeeeee", linewidth=0.0)
    gca().add_patch(rect1)
    rect2 = Rectangle((df/2, -1.0), df/2, 3.0, facecolor="#eeeeee", linewidth=0.0)
    gca().add_patch(rect2)

    xticks([-df/2.0, 0.0, df/2.0])
    yticks([0.0, 1.0])
    grid(True)
    axis([-df/8.0, df/2.0 + df/8.0, 0.0, 1.1])

    text(1000, 0.5, "$|T_%s(f)|$" % i)
    text(23500, 0.15, "$f$ (Hz)")

    width_cm = 12.0#12.0
    width_in = width_cm / 2.54
    ratio = 6.0
    fig.set_size_inches((width_in, width_in / ratio))
    save_pdf_svg("distorsion%s" % i)


#-------------------------------------------------------------------------------

clf()
fig = gcf()
plot(h_0, "k-", linewidth=0.75)
axis([0, 512, -0.010, 0.040])
width_cm = 12.0#12.0
width_in = width_cm / 2.54
ratio = 1.618
fig.set_size_inches((width_in, width_in / ratio))
save_pdf_svg("prototype")

#-------------------------------------------------------------------------------

a0 = h0 * 2 * cos(pi*(0+ 0.5) * n / float(M) + (-1)**0 * pi/4)
a1 = h0 * 2 * cos(pi*(1+ 0.5) * n / float(M) + (-1)**1 * pi/4)
a2 = h0 * 2 * cos(pi*(2+ 0.5) * n / float(M) + (-1)**2 * pi/4)
a3 = h0 * 2 * cos(pi*(3+ 0.5) * n / float(M) + (-1)**3 * pi/4)

s0 = h0 * 2 * cos(pi*(0+ 0.5) * n / float(M) - (-1)**0 * pi/4)
s1 = h0 * 2 * cos(pi*(1+ 0.5) * n / float(M) - (-1)**1 * pi/4)
s2 = h0 * 2 * cos(pi*(2+ 0.5) * n / float(M) - (-1)**2 * pi/4)
s3 = h0 * 2 * cos(pi*(3+ 0.5) * n / float(M) - (-1)**3 * pi/4)

clf()
f = arange(0.0, 1.0, 0.0001) * df/2
spa0 = F(a0, dt=dt)
spa1 = F(a1, dt=dt)
spa2 = F(a2, dt=dt)
spa3 = F(a3, dt=dt)

sps0 = F(s0, dt=dt)
sps1 = F(s1, dt=dt)
sps2 = F(s2, dt=dt)
sps3 = F(s3, dt=dt)

T_0 = abs(sps0(f)*spa0(f) + sps1(f)*spa1(f) + sps2(f)*spa2(f) + sps3(f)*spa3(f))
T_1 = abs(sps0(f)*spa0(f+1*df/4) + sps1(f)*spa1(f+1*df/4) + sps2(f)*spa2(f+1*df/4) + sps3(f)*spa3(f+1*df/4))
T_2 = abs(sps0(f)*spa0(f+2*df/4) + sps1(f)*spa1(f+2*df/4) + sps2(f)*spa2(f+2*df/4) + sps3(f)*spa3(f+2*df/4))
T_3 = abs(sps0(f)*spa0(f+3*df/4) + sps1(f)*spa1(f+3*df/4) + sps2(f)*spa2(f+3*df/4) + sps3(f)*spa3(f+3*df/4))

#plot(f, T_0, "k")
plot(f, T_1, "g")
plot(f, T_2, "b")
plot(f, T_3, "r")
xlabel("Frequency $f$ (Hz)")
gcf().subplots_adjust(bottom=0.20)

rect1 = Rectangle((-df/2, -1.0), df/2, 3.0, facecolor="#eeeeee", linewidth=0.0)
gca().add_patch(rect1)
rect2 = Rectangle((df/2, -1.0), df/2, 3.0, facecolor="#eeeeee", linewidth=0.0)
gca().add_patch(rect2)

xticks([-df/2.0, 0.0, df/2.0])
yticks([0.0, 1.0])
grid(True)
#axis([-df/8.0, df/2.0 + df/8.0, 0.0, 1.1])


save_pdf_svg("distortion-PQMF")


#---------------------------------------------------------------------------

clf()
from filters import *
df = MPEG.df
f = arange(0.0, 1.0, 0.001)* df/2
plot(f, 20*log10(abs(D(0)(f))), "k-", linewidth=0.75)
axis([0, df/2, -100, -80])
ylabel("distortion (dB)")
xlabel("frequency (Hz)")
save_pdf_svg("distortion-MPEG-0")




