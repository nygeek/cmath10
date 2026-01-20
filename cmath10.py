""" Implementation of the Complex Decimal Math library for the cnc10
    calculator.

    Modeled on the cmath.py library distributed as part of Python,
    but using the decimal.py long decimal math machinery.

Started 2025-12-21

Copyright (C) 2025 NYGeek LLC

    ToDo list in README.md

"""

# ----- Python libraries ----- #
import json
from decimal import Decimal, getcontext, InvalidOperation

# ----- Local libraries ----- #
# from trace_debug import DebugTrace
from math10 import Math10

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

def isclose(a, b, rel_tol=1e-15, abs_tol=0.0):
    """ True if a and b are close """
    # functional wrapper for OO original
    return a.isclose(b, rel_tol, abs_tol)

# ----- Main CMath10 class ----- #

class CMath10:
    """ Class to implement the Complex Decimal Math machinery. """


    def __init__(self, real, imag, precision=32):
        """ Initialize a complex decimal. """
        # print(f"DEBUG CMath10(real: {real}, imag: {imag})")
        self.real = Decimal(real)
        self.imag = Decimal(imag)
        self.precision = precision
        getcontext().prec = precision


    def __str__(self):
        """ return a string representation of the number """
        sgn = "+" if self.imag >= 0 else ""
        tol = Decimal(10) ** -self.precision
        _real = 0 if abs(self.real) < tol else self.real
        _imag = 0 if abs(self.imag) < tol else self.imag
        return "(" + str(_real) + sgn + str(_imag) + "i)"


    def __repr__(self):
        """ return the representation of CMath10 object """
        return f"CMath10('{str(self)}')"


    def copy(self):
        """ return a clone of this item """
        return CMath10(self.real, self.imag)


    def isclose(self, z, rel_tol=1e-9, abs_tol=0.0):
        """ are two numbers close? """
        if self == z:
            return True
        diff = abs(self-z)
        ref = max(self.abs(), z.abs())
        return diff <= max(rel_tol * ref, abs_tol)


# ----- Basic complex arithmetic ----- #

    def add(self, z):
        """ Implement self + b """
        getcontext().prec += 2
        _result = CMath10(self.real + z.real, self.imag + z.imag)
        getcontext().prec -= 2
        return _result


    def __add__(self, z):
        return self.add(z)


    def sub(self, z):
        """ Implement self - b """
        getcontext().prec += 2
        _result = CMath10(self.real - z.real, self.imag - z.imag)
        getcontext().prec -= 2
        return _result


    def __sub__(self, z):
        return self.sub(z)


    def mul(self, z):
        """ Implement self * b """
        getcontext().prec += 2
        _real = (self.real * z.real) - (self.imag * z.imag)
        _imag = (self.real * z.imag) + (self.imag * z.real)
        _result = CMath10(_real, _imag)
        getcontext().prec -= 2
        return _result


    def __mul__(self, z):
        return self.mul(z)


    def div(self, z):
        """ Implement self / b """
        getcontext().prec += 2
        _denominator = (z.real * z.real) + (z.imag * z.imag)
        _real = ((self.real * z.real) + (self.imag * z.imag))/_denominator
        _imag = ((self.imag * z.real) - (self.real * z.imag))/_denominator
        _result = CMath10(_real, _imag)
        getcontext().prec -= 2
        return _result


    def __truediv__(self, z):
        return self.div(z)


# ----- complex constants ----- #

    @staticmethod
    def pi():
        """ (pi, 0) """
        return CMath10(Math10.pi(), Decimal("0"))


    @staticmethod
    def e():
        """ (e, 0) """
        return CMath10(Math10.e(), Decimal("0"))


# ----- complex higher math ----- #

    def abs(self):
        """ aka mag """
        print(f"DEBUG abs(self: {self})")
        return CMath10(self.scalar_abs(), 0)


    def acos(self):
        """ inverse cosine of a complex number """
        _zz = self.mul(self)
        _i = CMath10(0,1)
        _result = _zz.sub(CMath10(1,0)).sqrt().add(self).log().div(_i)
        return _result


    def exp(self):
        """ exp(a+bi) = exp(a)*(cos(b)+isin(b)) """
        getcontext().prec +=2
        _mag = self.real.exp()
        _real = _mag * Math10(self.imag).cos()
        _imag = _mag * Math10(self.imag).sin()
        getcontext().prec -=2
        return CMath10(_real, _imag)


    def log(self):
        """ natural logarithm of z """
        # note: in cmath log is natural log, log10 is decimal log
        # note: in decimal.py ln is natural log
        _real = self.scalar_abs().ln() # this calls decimal.py ln
        _imag = Math10.atan2(self.imag, self.real)
        return CMath10(_real, _imag)


    def log10(self):
        """ natural logarithm of z """
        # note: in cmath log is natural log, log10 is decimal log
        # note: in decimal.py ln is natural log
        return self.log().div(CMath10(10,0).log())


    def phase(self):
        """ phase of z, aka arg z """
        return CMath10(Math10.atan2(self.real, self.imag), Decimal(0))


    def sqrt(self):
        """ square root of z """
        # Principal square root.  There is another, of course
        getcontext().prec +=2
        _r = self.scalar_abs()
        _sign = 1 if self.imag >= 0 else -1
        _result = CMath10(((_r + self.real)/2).sqrt(),
                          _sign * ((_r - self.real)/2).sqrt())
        getcontext().prec -=2
        return _result


    def cos(self):
        """ complex cosine """
        getcontext().prec += 2
        _real = Math10(self.real).cos() * Math10(self.imag).cosh()
        _imag = Math10(self.real).sin() * Math10(self.imag).sinh()
        _imag = Decimal("-1") * _imag
        _result = CMath10(_real, _imag)
        getcontext().prec -= 2
        return _result


    def sin(self):
        """ complex sine """
        getcontext().prec += 2
        _real = Math10(self.real).sin() * Math10(self.imag).cosh()
        _imag = Math10(self.real).cos() * Math10(self.imag).sinh()
        _result = CMath10(_real, _imag)
        getcontext().prec -= 2
        return _result


    def tan(self):
        """ complex tangent """
        getcontext().prec += 2
        _num = self.sin()
        _den = self.cos()
        _result = _num.div(_den)
        getcontext().prec -= 2
        return _result


# ----- scalar result on complex numbers ----- #

    def scalar_abs(self):
        """ aka mag """
        getcontext().prec +=2
        _result = (self.real * self.real + self.imag * self.imag).sqrt()
        getcontext().prec -=2
        return _result


    def scalar_arg(self):
        """ argument """
        getcontext().prec +=2
        _result = Math10.atan2(self.imag, self.real)
        getcontext().prec -=2
        return _result


# ----- StdLibAdapter class ----- #

class StdLibAdapter:
    """ Make CMath10 (OO) look like cmath (functional)."""
    @staticmethod
    def complex(real, imag=0):
        """ create a CMath10 complex number """
        return CMath10(real, imag)

    @staticmethod
    def sqrt(z):
        """ functional form of sqrt """
        return z.sqrt()

    @staticmethod
    def abs(z):
        """ functional form of abs """
        # This is a complex result.  Should we return .real()?
        print(f"DEBUG StdLibAdapter: abs(z): {z}")
        return z.abs()

    @staticmethod
    def phase(z):
        """ functional form of phase """
        return z.phase()

    @staticmethod
    def add(a, b):
        """ functional form of add """
        return a.add(b)

    @staticmethod
    def sub(a, b):
        """ functional form of sub """
        return a.sub(b)

    @staticmethod
    def mul(a, b):
        """ functional form of mul """
        return a.mul(b)

    @staticmethod
    def div(a, b):
        """ functional form of div """
        return a.div(b)

    @staticmethod
    def isclose(a, b, rel_tol=1e-15):
        """ functional form of isclose """
        return a.isclose(b, rel_tol)

# ----- Higher math ----- #

    @staticmethod
    def e():
        """ functional form of pi """
        return CMath10(Math10.e(), Decimal("0"))

    @staticmethod
    def pi():
        """ functional form of pi """
        return CMath10(Math10.pi(), Decimal("0"))

    @staticmethod
    def acos(z):
        """ functional form of acos """
        return z.acos()

    @staticmethod
    def asin(z):
        """ functional form of asin """
        return z.asin()

    @staticmethod
    def atan(z):
        """ functional form of atan """
        return z.atan()

    @staticmethod
    def cos(z):
        """ functional form of cos """
        return z.cos()

    @staticmethod
    def sin(z):
        """ functional form of sin """
        return z.sin()

    @staticmethod
    def tan(z):
        """ functional form of tan """
        return z.tan()

    @staticmethod
    def exp(z):
        """ functional form of exp """
        return z.exp()

    @staticmethod
    def log(z):
        """ functional form of log """
        return z.log()


    @staticmethod
    def log10(z):
        """ functional form of log """
        return z.log10()


def main():
    """ simple smoke test """
    print("Smoke test is now in smoke.py.")


if __name__ == '__main__':
    main()
