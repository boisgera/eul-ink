#!/usr/bin/env python

import sys

sys.path.append("../SCRIPTS")

import ulaw

import matplotlib

def save_pdf_svg(name):
    matplotlib.rc('text', usetex=True)
    matplotlib.rc("font", size=8, family="serif")
    savefig(name + ".pdf")
    #matplotlib.rcdefaults()
    savefig(name + ".svg")
    
from pylab import *


#grid(True)

fig = gcf()

# target: 30 in (12 cm)

# (w, h) = fig.get_size_inches()
width_cm = 12.0
width_in = width_cm / 2.54
ratio = 3.5 # extra-wide #1.618 # golden
fig.set_size_inches((width_in, width_in / ratio))
#print 2*w

t_max = 2 / 1000.0 # ms
t = arange(0, t_max, 1.0/8000.0)
tc = arange(0, t_max, 1.0/800000.0)
def sin10k(t):
    return sin(2*pi*10000*t)
def sin2k(t):
    return sin(2*pi*2000*t)

axis([0, t_max, -1.1, 1.1])
yticks((-1.0, 0.0, 1.0))

#plot(tc, sin10k(tc), "k", linewidth=0.75)
plot(t, sin2k(t), "k.")

axis([0, t_max, -1.1, 1.1])
gcf().subplots_adjust(bottom=0.15)

save_pdf_svg("frequency_shift_sampling-0")

plot(tc, sin2k(tc), "k", linewidth=0.75)

axis([0, t_max, -1.1, 1.1])
gcf().subplots_adjust(bottom=0.15)
yticks((-1.0, 0.0, 1.0))

save_pdf_svg("frequency_shift_sampling-1")

clf()

#plot(tc, sin2k(tc), "k", linewidth=0.75)
plot(tc, sin10k(tc), "k", linewidth=0.75)
plot(t, sin2k(t), "k.")

axis([0, t_max, -1.1, 1.1])
gcf().subplots_adjust(bottom=0.15)
yticks((-1.0, 0.0, 1.0))

save_pdf_svg("frequency_shift_sampling-2")





