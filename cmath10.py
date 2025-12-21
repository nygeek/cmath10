""" Implementation of the Complex Decimal Math library for the cnc10
    calculator.

Modeled on the cmath.py library distributed as part of Python,
but using the decimal.py long decimal math machinery.

Started 2025-12-21

Copyright (C) 2025 NYGeek LLC

"""

# ----- Python libraries ----- #
import json
from decimal import *

# ----- Local libraries ----- #
from trace_debug import DebugTrace

# ----- JSON Encoder for Decimal ----- #

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)

def decimal_decoder(dct):
    for key, value in dct.items():
        if isinstance(value, str):
            try:
                dct[key] = Decimal(value)
            except:
                pass
    return dct

# ----- Main CMath10 class ----- #

class CMath10:
    """ Class to implement the Complex Decimal Math machinery. """

    # ToDo:
    #   [2025-12-21] phase
    #   [2025-12-21] polar
    #   [2025-12-21] rect
    #   [2025-12-21] exp
    #   [2025-12-21] log
    #   [2025-12-21] sqrt
    #   [2025-12-21] acos
    #   [2025-12-21] asin
    #   [2025-12-21] atan
    #   [2025-12-21] cos
    #   [2025-12-21] sin
    #   [2025-12-21] tan
    #   [2025-12-21] acosh
    #   [2025-12-21] asinh
    #   [2025-12-21] atanh
    #   [2025-12-21] cosh
    #   [2025-12-21] sinh
    #   [2025-12-21] tanh
    #   [2025-12-21] pi
    #   [2025-12-21] e 
    #   [2025-12-21] add 
    #   [2025-12-21] sub 
    #   [2025-12-21] mul 
    #   [2025-12-21] div 


    def __init__(self, real, imag, precision=32):
        """ Initialize a complex decimal. """
        self.real = Decimal(real)
        self.imag = Decimal(imag)
        self.precision = precision
        getcontext().prec = precision

    def __str__(self):
        """ return a string representation of the number """
        if (self.imag >= 0):
            return "(" + str(self.real) + "+" + str(self.imag) + "j)"
        else:
            return "(" + str(self.real) + str(self.imag) + "j)"

    def add(self, b):
        """ Implement self + b """
        self.real += b.real
        self.imag += b.imag
        return self


    def sub(self, b):
        """ Implement self - b """
        self.real -= b.real
        self.imag -= b.imag
        return self


    def mul(self, b):
        """ Implement self * b """
        _real = (self.real * b.real) - (self.imag * b.imag)
        _imag = (self.real * b.imag) + (self.imag * b.real)
        self.real = _real
        self.imag = _imag
        return self


    def div(self, b):
        """ Implement self / b """
        _denominator = (b.real * b.real) + (b.imag * b.imag)
        _real = (self.real * b.real) + (self.imag * b.imag)
        _imag = (self.imag * b.real) - (self.real * b.imag)
        self.real = _real / _denominator
        self.imag = _imag / _denominator
        return self


def main():
    """ simple smoke test """
    DEBUG = DebugTrace(True)
    z = CMath10("1", "2")
    print("Z")
    print(z)
    a = CMath10("1", "3")
    b = CMath10("2.1", "7.9")
    print("a")
    print(a)
    print("b")
    print(b)
    a.add(b)
    print("a + b")
    print(a)
    a = CMath10("1", "3")
    a.sub(b)
    print("a - b")
    print(a)
    a = CMath10("1", "3")
    a.mul(b)
    print("a * b")
    print(a)
    a = CMath10("1", "1")
    b = CMath10("1", "-1")
    a.div(b)
    print("a / b")
    print(a)


if __name__ == '__main__':
    main()
