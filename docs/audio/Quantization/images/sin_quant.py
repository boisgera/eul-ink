#!/usr/bin/env python
from matplotlib import rc
# rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)
rc("font", size=8, family="serif")

from pylab import *

from numpy import *

class Uniform(object):
    def __init__(self, low=0.0, high=1.0, num_bits=None, num_values=256, rounding=round_):
        self.low = float(low)
        self.high = float(high)
        if num_bits:
            self.num_values = 2 ** num_bits
        else:
            self.num_values = num_values
        self.delta = (high - low) / self.num_values
        self.rounding = rounding
        
    def encode(self, x):
        low, high, delta = self.low, self.high, self.delta
        x = clip(x, low + delta/2.0, high - delta/2)
        flints = self.rounding((x - low) / delta - 0.5)
        return array(flints, dtype=long)

    def decode(self, i):
        return self.low + (i + 0.5) * self.delta 

    def __call__(self, x):
        return self.decode(self.encode(x))


grid(True)
fig = gcf()

# target: 30 in (12 cm)

# (w, h) = fig.get_size_inches()
width_cm = 13.0
width_in = width_cm / 2.54
ratio = 2.5 # extra wide
fig.set_size_inches((width_in, width_in / ratio))
#print 2*w

x = arange(pi + pi/2, pi + 2*pi - pi/2 + pi/2 + pi/4, 0.001)
xticks([-1, 20])
yticks([-1.0, 0.0, 1.0])

q = Uniform(-1.0, 1.0, num_values=7)
f = lambda x: 1.1*sin(x) * exp(-abs(x-3*pi/2)**2/10.0)
z = f(x)

plot(x, z, "k-", linewidth=0.75, label="original")#, markersize = 1.0, markeredgewidth=0.1)
plot(x, q(z), "k.", markersize=0.1, linewidth=0.1, label="quantized")#, markersize = 0.01, markeredgewidth=0.01)

a =2*pi+0.6 # 0.6
gca().annotate("original number $x$", xy=(a, f(a)) , xytext=(5.0,0.75), arrowprops=dict(arrowstyle="-", linewidth=0.5,
connectionstyle="angle,angleA=0,angleB=135,rad=0"))
a =2*pi+0.6 # 1.4
gca().annotate("quantized number $[ x ]$", xy=(a, q(f(a))) , xytext=(7.85,-0.35), arrowprops=dict(arrowstyle="-", linewidth=0.5,
connectionstyle="angle,angleA=0,angleB=-45,rad=0"))

#gca().annotate('arrowstyle', xy=(0, 1),  xycoords='data',
#                xytext=(-50, 30), textcoords='offset points',
#                arrowprops=dict(arrowstyle="->")
#                )

#legend(loc=2)

axis([x[0], x[-1], -1.25, 1.25])

savefig("sin_quant.pdf", dpi=600)


