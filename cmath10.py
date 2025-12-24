""" Implementation of the Complex Decimal Math library for the cnc10
    calculator.

    Modeled on the cmath.py library distributed as part of Python,
    but using the decimal.py long decimal math machinery.

    OPEN QUESTION - should the scalar machinery be split out as a
    separate module?

Started 2025-12-21

Copyright (C) 2025 NYGeek LLC

    ToDo list in README.md

"""

# ----- Python libraries ----- #
import json
from decimal import Decimal, getcontext, InvalidOperation

# ----- Local libraries ----- #
from trace_debug import DebugTrace

# ----- JSON Encoder for Decimal ----- #

class DecimalEncoder(json.JSONEncoder):
    """ Enable decimal.py objects to be JSON serialized. """
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super().default(o)


def decimal_decoder(dct):
    """ Convert to Decimal in JSON handler """
    for key, value in dct.items():
        if isinstance(value, str):
            try:
                dct[key] = Decimal(value)
            except (InvalidOperation, TypeError, ValueError):
                pass
    return dct


# ----- ----- Scalar functions ----- ----- #

# ----- scalar constants ----- #

def scalar_pi():
    """ return pi """
    # docs.python.org/3/library/decimal.html#recipes
    getcontext().prec += 2
    three = Decimal(3)
    lasts, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24
    while s != lasts:
        lasts = s
        n, na = n+na, na+8
        d, da = d+da, da+32
        t = (t * n) / d
        s += t
    getcontext().prec -= 2
    return +s


def scalar_e():
    """ return e """
    return Decimal('1').exp()


# ----- scalar trigonometric functions ----- #

def scalar_cos(x):
    """ return cosine """
    # from docs.python.org/3/library/decimal.html#recipes.
    _twopi = 2 * scalar_pi()
    if ((x > _twopi) or (x < -_twopi)):
        x %= _twopi
    getcontext().prec += 2
    i, lasts, s, fact, num, sign = 0, 0, 1, 1, 1, 1
    while s != lasts:
        lasts = s
        i += 2
        fact *= i * (i-1)
        num *= x * x
        sign *= -1
        s += num / fact * sign
    getcontext().prec -= 2
    return +s


def scalar_sin(x):
    """ return sin """
    # from docs.python.org/3/library/decimal.html#recipes
    getcontext().prec += 2
    _twopi = 2 * scalar_pi()
    if ((x > _twopi) or (x < -_twopi)):
        x %= _twopi
    i, lasts, s, fact, num, sign = 1, 0, x, 1, x, 1
    while s != lasts:
        lasts = s
        i += 2
        fact *= i * (i-1)
        num *= x * x
        sign *= -1
        s += num / fact * sign
    getcontext().prec -= 2
    return +s


def scalar_tan(x):
    """ sin(x) / cos(x) """
    return scalar_sin(x) / scalar_cos(x)


def scalar_acos(x):
    """ inverse cosine """
    return (scalar_pi() / 2) - scalar_asin(x)


def scalar_asin(x):
    """ inverse sine
        Compute arcsin(x) using Taylor series.
        Valid for |x| <= 1
        arcsin(x) = x + (1/2)(x^3/3) + (1*3)/(2*4)(x^5/5)
            + (1*3*5)/(2*4*6)(x^7/7) + ...
        """
    getcontext().prec += 2
    if abs(x) > 1:
        raise ValueError("arcsin(x) requires |x| <= 1")
    if abs(x) > Decimal('0.7'):
        sign = 1 if x >= 0 else -1
        result = scalar_pi() / 2 - \
            scalar_asin((1 - x*x).sqrt()) * sign
        getcontext().prec -= 2
        return +result
    power = x
    result = x
    i = 1
    while True:
        power *= x * x * (2*i - 1) * (2*i - 1) / ((2*i) * (2*i + 1))
        term = power
        if abs(term) < Decimal(10) ** -(getcontext().prec - 2):
            break
        result += term
        i += 1
    getcontext().prec -= 2
    return +result


def scalar_atan(x):
    """
    Compute arctan(x) using Taylor series.
    arctan(x) = x - x^3/3 + x^5/5 - x^7/7 + ...  for |x| <= 1
    For |x| > 1, use scalar_atan(x) = pi/2 - scalar_atan(1/x) for x > 0
                           or = -pi/2 - scalar_atan(1/x) for x < 0
    """
    getcontext().prec += 2
    x = Decimal(x)
    # For |x| > 1, use the identity to improve convergence
    if abs(x) > 1:
        sign = 1 if x > 0 else -1
        result = sign * scalar_pi() / 2 - scalar_atan(1 / x)
        getcontext().prec -= 2
        return +result
    # For values close to 1, use scalar_atan(x) =
    #   pi/4 + scalar_atan((x-1)/(x+1)) to improve convergence
    if abs(x) > Decimal('0.5'):
        result = scalar_pi() / 4
        if x + 1 != 0:
            result += scalar_atan((x - 1) / (x + 1))
        getcontext().prec -= 2
        return +result
    power = x
    result = x
    i = 1
    while True:
        power *= -x * x
        term = power / (2 * i + 1)
        if abs(term) < Decimal(10) ** -(getcontext().prec - 2):
            break
        result += term
        i += 1
    getcontext().prec -= 2
    return +result


def scalar_atan2(x, y):
    """ inverse tangent x / y, with sign of y """
    _sign = 1
    if y < 0:
        _sign = -1
    getcontext().prec += 2
    _ratio = x / y
    _result =  _sign * scalar_atan(_ratio)
    getcontext().prec -= 2
    return _result


# ----- Main CMath10 class ----- #

class CMath10:
    """ Class to implement the Complex Decimal Math machinery. """


    def __init__(self, real, imag, precision=32):
        """ Initialize a complex decimal. """
        self.real = Decimal(real)
        self.imag = Decimal(imag)
        self.precision = precision
        getcontext().prec = precision


    def __str__(self):
        """ return a string representation of the number """
        if self.imag >= 0:
            return "(" + str(self.real) + "+" + str(self.imag) + "j)"
        return "(" + str(self.real) + str(self.imag) + "j)"


# ----- Basic complex arithmetic ----- #

    def add(self, b):
        """ Implement self + b """
        getcontext().prec += 2
        self.real += b.real
        self.imag += b.imag
        getcontext().prec -= 2
        return self


    def sub(self, b):
        """ Implement self - b """
        getcontext().prec += 2
        self.real -= b.real
        self.imag -= b.imag
        getcontext().prec -= 2
        return self


    def mul(self, b):
        """ Implement self * b """
        getcontext().prec += 2
        _real = (self.real * b.real) - (self.imag * b.imag)
        _imag = (self.real * b.imag) + (self.imag * b.real)
        self.real = _real
        self.imag = _imag
        getcontext().prec -= 2
        return self


    def div(self, b):
        """ Implement self / b """
        getcontext().prec += 2
        _denominator = (b.real * b.real) + (b.imag * b.imag)
        _real = (self.real * b.real) + (self.imag * b.imag)
        _imag = (self.imag * b.real) - (self.real * b.imag)
        self.real = _real / _denominator
        self.imag = _imag / _denominator
        getcontext().prec -= 2
        return self


# ----- complex math ----- #

    def abs(self):
        """ aka mag """
        return CMath10(self.scalar_abs(), 0)


    def exp(self):
        """ exp(a+bi) = exp(a)*(cos(b)+isin(b)) """
        getcontext().prec +=2
        _mag = self.real.exp()
        _real = _mag * scalar_cos(self.imag)
        _imag = _mag * scalar_sin(self.imag)
        self.real = _real
        self.imag = _imag
        getcontext().prec -=2
        return self


    def log(self):
        """ natural logarithm of z """
        # note: in cmath log is natural log, log10 is decimal log
        # note: in decimal.py ln is natural log
        _real = self.scalar_abs().ln() # this calls decimal.py ln
        _imag = scalar_atan2(self.imag, self.real)
        return CMath10(_real, _imag)


    def phase(self):
        """ phase of z, aka arg z """
        return CMath10(scalar_atan2(self.real, self.imag), Decimal(0))


    def sqrt(self):
        """ square root of z """
        # Principal square root.  There is another, of course
        getcontext().prec +=2
        _r = self.scalar_abs()
        _sign = 1
        if self.imag < 0:
            _sign = -1
        _result = CMath10( ((_r + self.real)/2).sqrt(), 
                       _sign * ((_r - self.real)/2).sqrt())
        getcontext().prec -=2
        return _result


# ----- scalar result on complex numbers ----- #

    def scalar_abs(self):
        """ aka mag """
        getcontext().prec +=2
        _result = (self.real * self.real + self.imag * self.imag).sqrt()
        getcontext().prec -=2
        return _result


def main():
    """ simple smoke test """
    print("Smoke test is now in smoke.py.")


if __name__ == '__main__':
    main()
