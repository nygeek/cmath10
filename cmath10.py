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
from decimal import Decimal, getcontext, localcontext, InvalidOperation

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
    Scalar = Math10


    def __init__(self, real, imag=None, precision=32):
        """ Initialize a complex decimal. """
        # print(f"DEBUG CMath10(real: {real}, imag: {imag})")
        if isinstance(real, CMath10):
            self.real = real.real
            self.imag = real.imag
            if imag is not None:
                self.imag += self.scalar(imag)
        else:
            if imag is None:
                imag = 0
            self.real = self.Scalar(real)
            self.imag = self.Scalar(imag)
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
        with localcontext() as ctx:
            ctx.prec += 2
            real = self.real + z.real
            imag = self.imag + z.imag
        return self.__class__(real, imag)


    def __add__(self, z):
        return self.add(z)


    def sub(self, z):
        """ Implement self - b """
        with localcontext() as ctx:
            ctx.prec += 2
            real = self.real - z.real
            imag = self.imag - z.imag
        return self.__class__(real, imag)


    def __sub__(self, z):
        return self.sub(z)


    def mul(self, z):
        """ Implement self * b """
        with localcontext() as ctx:
            ctx.prec += 2
            real = (self.real * z.real) - (self.imag * z.imag)
            imag = (self.real * z.imag) + (self.imag * z.real)
        return self.__class__(real, imag)


    def __mul__(self, z):
        return self.mul(z)


    def div(self, z):
        """ Implement self / b """
        with localcontext() as ctx:
            ctx.prec += 2
            denominator = (z.real * z.real) + (z.imag * z.imag)
            real = ((self.real * z.real) + (self.imag * z.imag))/denominator
            imag = ((self.imag * z.real) - (self.real * z.imag))/denominator
        return self.__class__(real, imag)


    def __truediv__(self, z):
        return self.div(z)


# ----- complex constants ----- #

    @classmethod
    def pi(cls):
        """ (pi, 0) """
        real = cls.Scalar.pi()
        imag = cls.Scalar(0)
        return cls(real, imag)


    @classmethod
    def e(cls):
        """ (e, 0) """
        real = cls.Scalar.e()
        imag = cls.Scalar(0)
        return cls(real, imag)


# ----- complex higher math ----- #

    def abs(self):
        """ aka mag """
        # print(f"DEBUG abs(self: {self})")
        return CMath10(self.scalar_abs(), 0)


    def acos(self):
        """ inverse cosine of a complex number """
        with localcontext() as ctx:
            ctx.prec += 2
            zz = self.mul(self)
            i = self.__class__(0,1)
            one = self.__class__(1,0)
            result = zz.sub(one).sqrt().add(self).log().div(i)
        return result


    def asin(self):
        """ inverse sine of a complex number """
        with localcontext() as ctx:
            ctx.prec += 2
            zz = self.mul(self)
            i = self.__class__(0,1)
            one = self.__class__(1,0)
            result = self.mul(i).add(one.sub(zz).sqrt()).log().div(i)
        return self.__class__(result)


    def atan(self):
        """ inverse tangent of a complex number """
        with localcontext() as ctx:
            ctx.prec += 2
            i = self.__class__(0,1)
            one = self.__class__(1,0)
            two = self.__class__(2,0)
            result = (one.sub(i.mul(self)).div(one.add(i.mul(self)))).log().mul(i).div(two)
        return self.__class__(result)


    def exp(self):
        """ exp(a+bi) = exp(a)*(cos(b)+isin(b)) """
        with localcontext() as ctx:
            ctx.prec += 2
            mag = self.Scalar(self.real).exp()
            real = mag * self.Scalar(self.imag).cos()
            imag = mag * self.Scalar(self.imag).sin()
        return self.__class__(real, imag)


    def log(self):
        """ natural logarithm of z """
        # note: in cmath log is natural log, log10 is decimal log
        # note: in decimal.py ln is natural log
        real = self.Scalar(self.scalar_abs()).ln() # this calls decimal.py ln
        imag = self.Scalar.atan2(self.imag, self.real)
        return self.__class__(real, imag)


    def log10(self):
        """ decimal logarithm of z """
        # note: in cmath log is natural log, log10 is decimal log
        # note: in decimal.py ln is natural log
        return self.log().div(self.__class__(10,0).log())


    def phase(self):
        """ phase of z, aka arg z """
        return self.__class__(self.Scalar.atan2(self.real, self.imag), self.Scalar(0))


    def sqrt(self):
        """ square root of z """
        # Principal square root.  There is another, of course
        with localcontext() as ctx:
            ctx.prec += 2
            r = self.scalar_abs()
            sign = 1 if self.imag >= 0 else -1
        return self.__class__(((r + self.real)/2).sqrt(), sign * ((r - self.real)/2).sqrt())


    def cos(self):
        """ complex cosine """
        with localcontext() as ctx:
            ctx.prec += 2
            real = self.Scalar(self.real).cos() * self.Scalar(self.imag).cosh()
            imag = -1 * (self.Scalar(self.real).sin() * self.Scalar(self.imag).sinh())
        return self.__class__(real, imag)


    def sin(self):
        """ complex sine """
        with localcontext() as ctx:
            ctx.prec += 2
            real = self.Scalar(self.real).sin() * self.Scalar(self.imag).cosh()
            imag = self.Scalar(self.real).cos() * self.Scalar(self.imag).sinh()
        return self.__class__(real, imag)


    def tan(self):
        """ complex tangent """
        with localcontext() as ctx:
            ctx.prec += 2
            num = self.sin()
            den = self.cos()
            result = num.div(den)
        return self.__class__(result)


# ----- scalar result on complex numbers ----- #

    def scalar_abs(self):
        """ aka mag """
        with localcontext() as ctx:
            ctx.prec += 2
            result = self.Scalar(self.real * self.real + self.imag * self.imag).sqrt()
        return result


    def scalar_arg(self):
        """ argument """
        with localcontext() as ctx:
            ctx.prec += 2
            result = atan2(self.imag, self.real)
        return self.Scalar(result)


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
        # print(f"DEBUG StdLibAdapter: abs(z): {z}")
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
