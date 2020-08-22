
# Python 2.7 Standard Library
import struct

# Third-Party Libraries
import numpy as np
	
# Audio
from audio.quantizers import Quantizer

# DEPRECATE ? Transfer in SCRIPTS ?
class FloatingPoint(Quantizer):
    def __init__(self, exp_bits=3, frac_bits=4):
        self.exp_bits = exp_bits
        self.frac_bits = frac_bits
        self.num_bits = 1 + self.exp_bits + self.frac_bits

        self.exp_bias = 2 ** (exp_bits - 1) - 1

        self.sign_shift = self.num_bits - 1
        self.sign_mask  = 1
        self.exp_shift = self.frac_bits
        self.exp_mask  = (2 ** exp_bits - 1)
        self.frac_shift = 0
        self.frac_mask = 2 ** frac_bits - 1 

    def _split(self, i):
        sign_bits = (i >> self.sign_shift) & self.sign_mask
        exp_bits  = (i >> self.exp_shift ) & self.exp_mask
        frac_bits = (i >> self.frac_shift) & self.frac_mask        
        return sign_bits, exp_bits, frac_bits

    def decode(self, i): # do the opposite: scalar imp and vector loops over it
        try:
            len(i)
            i_ = i
        except TypeError:
            i_ = [i]
        result = []
        for i in i_:
            sign_bits, exp_bits, frac_bits = self._split(i)
            sign = -sign_bits or 1
            exp_ = exp_bits - self.exp_bias
            frac = frac_bits * 2 ** (-self.frac_bits)
            #print "*", sign, exp_, frac
            if 0 < exp_bits < 2**self.exp_bits - 1:
                #print ">",  2 ** exp_, (1 + frac)
                result.append(sign * (1 + frac) * 2 ** exp_)
            elif exp_bits == 2**self.exp_bits - 1:
                if frac == 0:
                    result.append(sign * inf)
                else:
                    result.append(nan)
            else:
                #print "><",  2 ** (exp_ + 1), frac
                result.append(sign * frac * 2 ** (exp_ + 1))
        return result
               
# USELESS (support implemented in BitStream)
class Double(Quantizer):
    def encode(self, x):
        try:
            n = len(x)
        except TypeError:
            x = [x]
            n = 1
        return np.array(struct.unpack(n*"Q", struct.pack(n*"d", *x)), dtype=uint64)
        
    def decode(self, i):
        try:
            n = len(i)
        except TypeError:
            i = [i]
            n = 1
        return np.array(struct.unpack(n*"d", struct.pack(n*"Q", *i)), dtype=float64)
	
double = Double() 
 
def double2int(x):
    return struct.unpack('q', struct.pack('d', x))[0]

def revert(x):
    # checks. include revert(revert(x)) == x.
    # TODO: suitable doc + corresponding test.
    # """Two-complement to sign-magnitude representation conversion"""
    if x >= 0:
        return x
    else:
        return - (2**63 + x)

def isnan(x):
    return isinstance(x, float) and not x == x

def gap(x, y):
    """Compute the distance in ulps between the floats x and y."""
    
    if isnan(x) or isnan(y):
        inf = float('inf')
        return gap(-inf, inf) + 1
    else:
        int_x = revert(double2int(x))
        int_y = revert(double2int(y))

        return abs(int_x-int_y)
        
        
