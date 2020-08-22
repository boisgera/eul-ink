#!/usr/bin/env python

import sys
sys.path.append("/home/boisgera/DISKS/VOYAGER/SANDBOX/ACSAN")

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
from timeit import Timer
from pylab import *

import pickle

if "new" in sys.argv:

	setup = """from numpy.fft import fft
try:
    from __main__ import x, f
except ImportError:
	from fft_speed import x, f
from spectrum import F 
	"""

	max_n = 18 #20 # 1 to 1,000,000
	min_n = 0

	is_ = range(min_n, max_n+1)
	n1 = [2**i for i in range(min_n, max_n+1)]

	import random

	print ">",
	x = ravel([random.uniform(-1.0, 1.0) for _ in range(2**max_n)])

	print "<" # NO THAT'S TOO FAST, THAT'S IMPOSSIBLE !

	fft_template = "F(x[:{0}], n={0}, power_of_two=False)(f)"

	r1 = []
	for i in n1:
		cmd = fft_template.format(i)
		print "PO2:", i, cmd
		f = arange(0.0, 1.0, 1.0 / i)
		r1.append(min(Timer(cmd, setup).repeat(10, 1)))

	print 40*'-'



	n2 = [int(ceil(z)) for z in logspace(min_n, max_n, num=500, base=2)]
	n2.extend([2**i for i in range(min_n, max_n+1)])
	n2.extend(arange(128))
	n2 = list(set(n2))
	n2 = sorted(n2)
	print n2
	r2 = []
	for i in n2:
		cmd = fft_template.format(i)
		print "NON-PO2:", i, cmd,
		f = arange(0.0, 1.0, 1.0 / i)
		if i in n1 or i <= 1000:
		    times = 10
		else:
		    times = 1
		sr = min(Timer(cmd, setup).repeat(times, 1))
		print "timing:", sr
		r2.append(sr) 



	#-------------------



	#-------------------
	max_n = 12

	from random import uniform
	x = ravel([uniform(-1.0, 1.0) for _ in range(2**max_n)])


	from timeit import Timer

	#n = range(2**min_n, 2**max_n + 1)[::10]
	n3 = concatenate((arange(128), [int(ceil(i_)) for i_ in logspace(7, max_n, base=2, num=100)]))
	n3 = sorted(list(set(n3))) # remove duplicates
	r3 = []

	for i in n3:
		print "EXACT:", i,
		f = arange(0.0, 1.0, 1.0 / i)
		cmd = "F(x[:{0}])(f)".format(i)
		if i <= 100:
		    times = 10
		else:
		    times = 5
		t = min(Timer(cmd, setup).repeat(times, 1))
		print t
		r3.append(t)


	#-------------------

	#print len(primes()), len(_primes())

	print 70*"*"
	print "*** TESTING PRIMES"
	print 70*"*"

	def primes(n):
	  """ returns a list of prime numbers from 2 to < n """
	  if n < 2:  return []
	  if n == 2: return [2]
	  # do only odd numbers starting at 3
	  s = range(3, n, 2)
	  # n**0.5 may be slightly faster than math.sqrt(n)
	  mroot = n ** 0.5
	  half = len(s)
	  i = 0
	  m = 3
	  while m <= mroot:
		if s[i]:
		  j = (m * m - 3)//2
		  s[j] = 0
		  while j < half:
		    s[j] = 0
		    j += m
		i = i + 1
		m = 2 * i + 3
	  # make exception for 2
	  return [2]+[x for x in s if x]

	max_n = 14
	n4 = primes(256) + primes(2**max_n+1)[::5]
	n4 = sorted(list(set(n4)))
	r4 = []
	for i in n4:
		cmd = fft_template.format(i)
		print "PRIME:", i, cmd,
		f = arange(0.0, 1.0, 1.0 / i)
		if i <= 1000:
		    times = 5
		else:
		    times = 1
		sr = min(Timer(cmd, setup).repeat(times, 1))
		print "timing:", sr
		r4.append(sr)

	pickle.dump((n1, r1, n2, r2, n3, r3, n4, r4), open("fft_speed.pck", "w"))
else:
    (n1, r1, n2, r2, n3, r3, n4, r4) = pickle.load(open("fft_speed.pck"))

#-------------------------------------------------------------------------------
# Plots
#-------------------------------------------------------------------------------


#gca().annotate("DFT", xy=(n3[50], r3[50]) , xytext=(10,0.1), 
#                arrowprops=dict(arrowstyle="-", linewidth=0.25))

fig = gcf()
subsx = logspace(0, 6, 7)
subsy = logspace(-5, 0, 6)
loglog(n1, r1, "k.", markersize=4.0, basex=2, basey=2, subsx=subsx, subsy=subsy)
loglog(n1, r1, "k:", linewidth=0.5, basex=2, basey=2, subsx=subsx, subsy=subsy)

loglog(n2, r2, "k", linewidth=0.75)

#gca().annotate("{FFT-PO2}", xy=(n1[12], r1[12]) , xytext=(10000,0.00002), arrowprops=dict(arrowstyle="-", linewidth=0.25))

loglog(n4, r4, "k:", linewidth=0.5)


loglog(n3, r3, "k--", linewidth=0.75) # exact

axis([0, n1[-1], 1e-5, 1e0])
grid(True)


#gca().text(2, 0.4, "$t$")
ylabel("computation time $t$ in seconds")

xlabel("signal length")
gcf().subplots_adjust(bottom=0.15)


# (w, h) = fig.get_size_inches()
width_cm = 12.0#12.0
width_in = width_cm / 2.54
ratio = 1.618 # thin 
fig.set_size_inches((width_in, width_in / ratio))


#yticks((-1.0, 0.0, 1.0))

save_pdf_svg("fft-speed")



