#!/usr/bin/env python

import sys
sys.path.append("/home/boisgera/DISKS/VOYAGER/SANDBOX/ACSAN")



def save_pdf_svg(name, dpi=None):
    import matplotlib
    import pylab
    if dpi:
        options = {"dpi": dpi}
    else:
        options = {}
    matplotlib.rc('text', usetex=True)
    matplotlib.rc("font", size=8, family="serif")
    pylab.savefig(name + ".pdf", **options)
    #matplotlib.rcdefaults()
    pylab.savefig(name + ".svg")#, **options)

from pylab import *
from numpy import *
from numpy.linalg import *
import nltk; timit = nltk.corpus.timit

from bitstream2 import *
from filters import *
from quantizers import *
from lp import *
import wave



#-------------------------------------------------------------------------------
# Tex Matplotlib Configuration
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Downsampling: 16kHz (TIMIT source) to 8kHz
#-------------------------------------------------------------------------------
def timit_to_8kHz(uid, N=127):
    "Create a numpy array of 8kHz audio data from a TIMIT utterance id"
    str_data = timit.audiodata(uid)
    data = BitStream(str_data).read(int16, inf).newbyteorder()
    low_pass_filter = low_pass(fc=8000.0, dt=1.0/16000.0, window=hamming)(n=2*N+1)
    data = convolve(data, low_pass_filter)[N:-N:2]
    return data/max(abs(data))
#-------------------------------------------------------------------------------
UID = "dr1-fvmh0/sa1"
data = timit_to_8kHz(UID)

FRAME_LENGTH = 160 # 20 ms at 8 khz.
SUBFRAME_LENGTH = 32 # 4 ms
NUM_SUBFRAMES_PER_FRAME = FRAME_LENGTH / SUBFRAME_LENGTH
FREQUENCY = 8000.0

def split_data(data, frame_length=FRAME_LENGTH):
    """
    Split audio data into (an array of) frames with a given length.

    The original data is padded with zeros when necessary to produce frames
    of a constant length. 
    """
    n = len(data)
    if n % frame_length:
        data = append(data, zeros(frame_length - n % frame_length))
    n = len(data)
    num_frames = n / frame_length
    frames = reshape(data, (-1, frame_length))
    return frames

def merge_frames(frames):
    """
    Merge the frames
    """
    return ravel(frames)

frames = split_data(data, FRAME_LENGTH)

scale_factors = scale_factors = linspace(2**(-8), 1.0, 2**8)
error_quantizer = ScaleFactor(scale_factors=scale_factors, N=2**8-1)

class FakeQuantizer(Quantizer):
    def encode(self, data):
        return data
    def decode(self, data):
        return data

fake = FakeQuantizer()

class STP(Quantizer):
    def __init__(self, error_quantizer=None):
        self.quantizer = error_quantizer or fake
        self.fir = FIR()
        self.ar = AR()
        self.error = []

    def encode(self, frame):
        a = lp(frame, 16, zero_padding=False)
        self.fir.a = r_[0.0, a]
        predicted = self.fir(frame)
        error = frame - predicted
        self.error.extend(error)
        error = self.quantizer.encode(error)
        return (a, error)

    def decode(self, data):
        a, error = data
        error = self.quantizer.decode(error)
        self.ar.a = a
        return self.ar(error) 

def ACF(data, frame_length):
    frame = data[-frame_length:]
    frame = frame / norm(frame)
    past_length = len(data) - frame_length
    correl = zeros(past_length + 1)
    for i, _ in enumerate(correl):
        past_frame = data[past_length-i:past_length-i+frame_length]
        past_frame = past_frame / norm(past_frame)
        correl[i] = dot(past_frame, frame)
    return array(correl) 

stp = STP()
_ = [stp(frame) for frame in frames]
stp_error = stp.error

#-------------------------------------------------------------------------------
# stp_error_frames = split_data(stp_error, SUBFRAME_LENGTH)
plot(arange(len(data))-7600, data, "k-", color="#777777", linewidth=0.75)
plot(arange(len(stp_error))-7600, stp_error, "k-", linewidth=0.75)
yticks([-0.2, -0.1, 0.0, 0.1, 0.2])
xlabel("sample index")
ylabel("sample value")
gcf().subplots_adjust(bottom=0.20)
grid(True)
axis([7600-7600, 7759-7600, -0.25, 0.25])

#------------------------------------------------------------------------------
# Figure Export
#------------------------------------------------------------------------------

# (w, h) = fig.get_size_inches()
fig = gcf()
width_cm = 12.0#12.0
width_in = width_cm / 2.54
ratio = 2.5 # 1.618 # thin 
fig.set_size_inches((width_in, width_in / ratio))

save_pdf_svg("show_stp_spikes")


#-------------------------------------------------------------------------------

error = stp_error[7600:7760]
ac = ACF(error, SUBFRAME_LENGTH)
clf(); fig = gcf()
width_cm = 12.0#12.0
width_in = width_cm / 2.54
ratio = 2.5 # 1.618 # thin 
fig.set_size_inches((width_in, width_in / ratio))
plot(ac, "k-", linewidth=0.75)
plot(ac, "k.", markersize=3.0)
axis([-1, len(ac), -0.25, 1.05])
yticks([0.0, 0.5, 1.0])
grid(True)
xlabel("offset")
ylabel("correlation")
gcf().subplots_adjust(bottom=0.20)
save_pdf_svg("autocorrelation")



