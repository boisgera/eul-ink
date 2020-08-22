#!/usr/bin/env python

import os
import sys

from numpy import *
from pylab import *
from bitstream2 import *
import nltk; timit = nltk.corpus.timit

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

##-------------------------------------------------------------------------------
#from pylab import *
#from matplotlib import rc
#rc('text', usetex=True)
#rc("font", size=8, family="serif")
#-------------------------------------------------------------------------------

uid = 'dr1-fvmh0/sa1'
str_data = timit.audiodata(uid)
data = BitStream(str_data).read(int16, inf).newbyteorder()

plot(data, "k", linewidth=0.55, rasterized=False)

max_ = 15000
words = timit.word_times(uid)
for word, start, end in words:
     lmax = max(abs(data[start:end]))
     gca().text(0.5*(start + end), lmax + 500, word, 
                horizontalalignment="center", rotation="90", size="small")
     plot([start, start], [-max_, max_],  "k", linewidth=0.5)     
     plot([end, end], [-max_, max_],  "k", linewidth=0.2)     

yticks([0])
#print len(data)
xlabel("sample index")
#ylabel("sample value")
axis([0, len(data), -10000,max_])
gcf().subplots_adjust(bottom=0.20)

#-------------------------------------------------------------------------------
width_cm = 12.0
width_in = width_cm / 2.54
ratio = 2.5 # thin 
gcf().set_size_inches((width_in, width_in / ratio))
save_pdf_svg("she_had", dpi=600)

