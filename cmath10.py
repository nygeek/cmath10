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

    def __init__(self, real, imag, precision=32):
        self.real = Decimal(real)
        self.imag = Decimal(imag)
        self.precision = precision
        getcontext().prec = precision

    def __str__(self):
        return "(" + str(self.real) + "+" + str(self.imag) + "j)"


def main():
    """ simple smoke test """
    z = CMath10("1", "2")
    print(z)


if __name__ == '__main__':
    main()
