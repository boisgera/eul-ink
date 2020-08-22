#!/usr/bin/env python
# coding: utf-8
"""
Aware -- Perceptual Audio Coder: Psychoacoustic Model.
"""

# Python 2.7 Standard Library
from __future__ import division
import sys

# Third-Party Libraries
from numpy import *
from numpy.fft import fft
seterr(all="ignore")

# Digital Audio Coding
from audio.filters import MPEG
from audio.psychoacoustics import ATH, bark

#
# Metadata
# ------------------------------------------------------------------------------
#
__author__ = u"Sébastien Boisgérault <Sebastien.Boisgerault@mines-paristech.fr>"
__license__ = "MIT License"

#
# Constants
# ------------------------------------------------------------------------------
#
df = 44100.0
dt = 1.0 / df
N = MPEG.N
M = MPEG.M
   
k = arange(N // 2 + 1)
f_k = k * df / N
b_k = bark(f_k)

k_i = r_[0:49, 49:97:2, 97:251:4]
f_i = k_i * df / N
b_i = bark(f_i)
ATH_i = ATH(f_i)
subband_i = array([int(s) for s in round_(f_i * 32 / (0.5 * df) - 0.5)])

#
# Perceptual Model
# ------------------------------------------------------------------------------
#
def P_k_from_frame(frame, window=hanning, dB=False):
    alpha = 1.0 / sqrt(sum(window(N)**2) / N)
    frame = alpha * window(N) * frame

    frame_fft_2 = abs(fft(frame)) ** 2

    P_k = 2.0 * frame_fft_2[:(N // 2 + 1)] / N ** 2
    P_k[0] = 0.5 * P_k[0]
    if (N % 2 == 0):
        P_k[-1] = 0.5 * P_k[-1]

    P_k = 10.0 ** (96.0 / 10.0) * P_k
    if dB:
        P_k = 10.0 * log10(P_k)  
    return P_k

class Classifier(object):
    def __init__(self):
        small  = array([-2, +2])
        medium = array([-3, -2, +2, +3]) 
        large  = array([-6, -5, -4, -3, -2, +2, +3, +4, +5, +6])
        self.neighbourhood = 256 * [None]
        for _k in range(2, 63):
            self.neighbourhood[_k] = small
        for _k in range(63, 127):
            self.neighbourhood[_k] = medium
        for _k in range(127, 251):
            self.neighbourhood[_k] = large        
    def __call__(self, k, P):
        assert all(k == arange(0, N // 2 + 1))
        k_t = []
        P_t = []
        for _k in arange(3, 251):
            if (P[_k-1] <= P[_k] and P[_k+1] <= P[_k]):
                js = self.neighbourhood[_k]
                if all(P[_k] >= 5.0 * P[_k+js]):
                    k_t.append(_k)
                    P_t.append(P[_k-1] + P[_k] + P[_k+1])
                    P[_k-1] = P[_k] = P[_k+1] = 0.0
        return (array(k_t), array(P_t)), (k, P)        

classify = Classifier()

def group_by_critical_band(k, P):
    b_k = bark(f_k)
    cb_k = array([int(b) for b in floor(b_k)])
    bands = [[[], []] for _ in arange(amax(cb_k) + 1)]
    for _k, _P in zip(k, P):
        band = bands[cb_k[_k]]
        band[0].append(_k)
        band[1].append(_P)
    for b, band in enumerate(bands):
        bands[b] = array(band)
    return bands

def merge_tonals(k_t, P_t):
    bands = group_by_critical_band(k_t, P_t)
    k_t_out, P_t_out = [], []
    for band, k_P_s in enumerate(bands):
        if len(k_P_s[0]):
            k_max = None
            P_max = - inf 
            for _k, _P in zip(*k_P_s):
               if _P > P_max:
                   k_max = _k
                   P_max = _P
            k_t_out.append(k_max)
            P_t_out.append(P_max)
    return array(k_t_out), array(P_t_out)

def merge_non_tonals(k_nt, P_nt):
    bands = group_by_critical_band(k_nt, P_nt)
    k_nt_out = zeros(len(bands), dtype=uint8)
    P_nt_out = zeros(len(bands))
    for band, k_P_s in enumerate(bands):
        if len(k_P_s[0]):
            k, P = k_P_s
            P_sum = sum(P)
            if P_sum == 0.0:
                P = ones_like(P)
            k_mean = int(round(average(k, weights=P))) 
            k_nt_out[band] = k_mean
            P_nt_out[band] = P_sum
    return k_nt_out, P_nt_out

def threshold(k, P):
    ATH_k = 10 ** (ATH(f_k) / 10.0)
    k_out, P_out = [], []
    for (_k, _P) in zip(k, P):
        if _P > ATH_k[_k]:
            k_out.append(_k)
            P_out.append(_P)
    return array(k_out), array(P_out)

def maskers(frame, merge=True, ATH_threshold=True):
    P_k = P_k_from_frame(frame)
    (k_t, P_t), (k_nt, P_nt) = classify(k, P_k)
    if merge:
        k_t, P_t = merge_tonals(k_t, P_t)
        k_nt, P_nt = merge_non_tonals(k_nt, P_nt)
    if ATH_threshold:
        k_t, P_t = threshold(k_t, P_t)
        k_nt, P_nt = threshold(k_nt, P_nt)
    return (k_t, P_t), (k_nt, P_nt)

def excitation_pattern(b, b_m, I_m, tonal):
    db = b - b_m
    db_1 = minimum(db + 1.0, 0.0)
    db_2 = minimum(db      , 0.0)
    db_3 = maximum(db      , 0.0)
    db_4 = maximum(db - 1.0, 0.0)    
    mask  = I_m \
          + (11.0 - 0.40 * I_m) * db_1 \
          + ( 6.0 + 0.40 * I_m) * db_2 \
          - (17.0             ) * db_3 \
          + (       0.15 * I_m) * db_4
    if tonal:
        mask += -1.525 - 0.275 * b - 4.5
    else:
        mask += -1.525 - 0.175 * b - 0.5
    return mask

def mask_from_frame(frame, subband=True):
    frame = array(frame, copy=False)
    if shape(frame) != (N,):
        error = "the frame should a 1-dim. array of length {0}."
        raise TypeError(error.format(N))
    mask_i = 10.0 ** (ATH_i / 10.0)
    (k_t, P_t), (k_nt, P_nt) = maskers(frame)
    for masker_index in arange(len(k_t)):
        _b, _P = b_k[k_t[masker_index]], P_t[masker_index]
        ep = excitation_pattern(b_i, b_m=_b, I_m=10.0*log10(_P), tonal=True)
        mask_i += 10.0 ** (ep / 10.0)
    for masker_index in arange(len(k_nt)):
        _b, _P = b_k[k_nt[masker_index]], P_nt[masker_index]
        ep = excitation_pattern(b_i, b_m=_b, I_m=10.0*log10(_P), tonal=False) 
        mask_i += 10.0 ** (ep / 10.0)
    mask_i = 10.0 * log10(mask_i)

    subband_mask = [[] for _ in range(32)]
    for i, _mask_i in enumerate(mask_i):
        subband_mask[subband_i[i]].append(_mask_i)
    for i, _masks in enumerate(subband_mask):
        subband_mask[i] = amin(_masks)
    return array(subband_mask)

if __name__ == "__main__":
    t = r_[0:512] * dt
    try:
        f = float(sys.argv[1])
    except:
        print "need an argument: the tone frequency f in Hz"
        sys.exit(1)
    frame = sin(2 * pi * f * t)

    print
    print "Subband Mask Levels for a pure tone with SPL = 96 dB, f={0}".format(f)
    print 80*"-"
    for i, mask_level in enumerate(mask_from_frame(frame)):
        print "subband {0:2d}: {1!r} dB".format(i, mask_level)
    print


