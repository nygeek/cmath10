""" Implementation of the Complex Decimal Math library for the cnc10
    calculator.

    Modeled on the cmath.py library distributed as part of Python,
    but using the decimal.py long decimal math machinery.


Started 2025-12-21

SPDX-License-Identifier: MIT
Copyright (C) 2025 NYGeek LLC

ToDo list in README.md

"""

# ----- Python libraries ----- #
from decimal import Decimal, getcontext, localcontext
import warnings

# ----- Local libraries ----- #
# from trace_debug import DebugTrace
from math10 import Math10

# ----- Main CMath10 class ----- #

class CMath10:
    """ Class to implement the Complex Decimal Math machinery. """
    Scalar = Math10


    def __init__(self, real, imag=None, precision=32):
        """ Initialize a complex decimal. """
        # print(f"DEBUG CMath10(real: {real}, imag: {imag})")
        if isinstance(real, CMath10):
            warnings.warn(
                "Complex10() argument 'real' must be a real number, not complex",
                DeprecationWarning,
                stacklevel=2
            )
            self.real = real.real
            self.imag = real.imag
            if imag is not None:
                warnings.warn(
                    "Complex10() argument 'imag' must be a real number, not complex",
                    DeprecationWarning,
                    stacklevel=2
                )
                self += self.__class__(0,1) * imag
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
        rel_tol = self.Scalar(rel_tol)
        abs_tol = self.Scalar(abs_tol)
        diff = (self-z).scalar_abs()
        ref = max(self.scalar_abs(), z.scalar_abs())
        return diff <= max(rel_tol * ref, abs_tol)


    def abs(self):
        """ aka mag """
        magnitude = self.scalar_abs()
        return self.__class__(magnitude, 0)

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

    def acos(self):
        """ inverse cosine of a complex number """
        with localcontext() as ctx:
            ctx.prec += 2
            zz = self.mul(self)
            i = self.__class__(0,1)
            one = self.__class__(1,0)
            result = one.sub(zz).sqrt().mul(i).add(self).log().div(i)
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
            result = (one.sub(i.mul(self)).\
                    div(one.add(i.mul(self)))).log().mul(i).div(two)
            return self.__class__(result)


    def asinh(self):
        """ inverse hyperbolic sine: asinh(z) = log(z + sqrt(z² + 1)) """
        with localcontext() as ctx:
            ctx.prec += 2
            one = self.__class__(1, 0)
            zz_plus_one = self.mul(self).add(one)
            result = self.add(zz_plus_one.sqrt()).log()
            return self.__class__(result)


    def acosh(self):
        """ inverse hyperbolic cosine: acosh(z) = log(z + sqrt(z² - 1)) """
        with localcontext() as ctx:
            ctx.prec += 2
            one = self.__class__(1, 0)
            zz_minus_one = self.mul(self).sub(one)
            result = self.add(zz_minus_one.sqrt()).log()
            return self.__class__(result)


    def atanh(self):
        """ inverse hyperbolic tangent: atanh(z) = (1/2) * log((1+z)/(1-z))
        """
        with localcontext() as ctx:
            ctx.prec += 2
            one = self.__class__(1, 0)
            two = self.__class__(2, 0)
            result = one.add(self).div(one.sub(self)).log().div(two)
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
        real = self.Scalar(self.scalar_abs()).ln()
        imag = self.Scalar.atan2(self.imag, self.real)
        return self.__class__(real, imag)


    def log10(self):
        """ decimal logarithm of z """
        # note: in cmath log is natural log, log10 is decimal log
        # note: in decimal.py ln is natural log
        return self.log().div(self.__class__(10,0).log())


    def phase(self):
        """ phase of z, aka arg z """
        return self.__class__(
                self.Scalar.atan2(self.imag, self.real),
                self.Scalar(0))


    def sqrt(self):
        """ square root of z """
        # Principal square root.  There is another, of course
        with localcontext() as ctx:
            ctx.prec += 2
            r = self.scalar_abs()
            sign = 1 if self.imag >= 0 else -1
            re_part = (r + self.real) / 2
            im_radicand = (r - self.real) / 2
            # Clamp to 0 to avoid InvalidOperation when im_radicand is tiny negative (rounding)
            if im_radicand < 0:
                im_radicand = self.Scalar(0)
            result = self.__class__(re_part.sqrt(), sign * im_radicand.sqrt())
            return result


    def cos(self):
        """ complex cosine """
        with localcontext() as ctx:
            ctx.prec += 2
            real = self.Scalar(self.real).cos() * \
                    self.Scalar(self.imag).cosh()
            imag = -1 * (self.Scalar(self.real).sin() * \
                    self.Scalar(self.imag).sinh())
            return self.__class__(real, imag)


    def cosh(self):
        """ complex hyperbolic cosine: cosh(re + i*im) = cosh(re)cos(im) + i*sinh(re)sin(im) """
        with localcontext() as ctx:
            ctx.prec += 2
            re = self.real
            im = self.imag
            real = self.Scalar(re).cosh() * self.Scalar(im).cos()
            imag = self.Scalar(re).sinh() * self.Scalar(im).sin()
            return self.__class__(real, imag)


    def sin(self):
        """ complex sine """
        with localcontext() as ctx:
            ctx.prec += 2
            real = self.Scalar(self.real).sin() * \
                    self.Scalar(self.imag).cosh()
            imag = self.Scalar(self.real).cos() * \
                    self.Scalar(self.imag).sinh()
            return self.__class__(real, imag)


    def sinh(self):
        """ complex hyperbolic sine: sinh(re + i*im) = sinh(re)cos(im) + i*cosh(re)sin(im) """
        with localcontext() as ctx:
            ctx.prec += 2
            re = self.real
            im = self.imag
            real = self.Scalar(re).sinh() * self.Scalar(im).cos()
            imag = self.Scalar(re).cosh() * self.Scalar(im).sin()
            return self.__class__(real, imag)


    def tan(self):
        """ complex tangent """
        with localcontext() as ctx:
            ctx.prec += 2
            return (self.sin() / self.cos())


    def tanh(self):
        """ complex hyperbolic tangent """
        with localcontext() as ctx:
            ctx.prec += 2
            return (self.sinh() / self.cosh())


# ----- scalar result on complex numbers ----- #

    def scalar_abs(self):
        """ aka mag """
        with localcontext() as ctx:
            ctx.prec += 2
            result = self.Scalar(
                         self.real * self.real +
                         self.imag * self.imag).sqrt()
        return result


    def scalar_arg(self):
        """ argument """
        with localcontext() as ctx:
            ctx.prec += 2
            result = self.Scalar.atan2(self.imag, self.real)
        return self.Scalar(result)


# ----- StdLibAdapter class ----- #

class StdLibAdapter:
    """ Make CMath10 (OO) look like cmath (functional)."""
    Scalar = Math10

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
        return CMath10(Math10.e(), Math10("0"))

    @staticmethod
    def pi():
        """ functional form of pi """
        return CMath10(Math10.pi(), Math10("0"))

    @staticmethod
    def acos(z):
        """ functional form of acos """
        return z.acos()

    @staticmethod
    def acosh(z):
        """ functional form of acosh """
        return z.acosh()

    @staticmethod
    def asin(z):
        """ functional form of asin """
        return z.asin()

    @staticmethod
    def asinh(z):
        """ functional form of asinh """
        return z.asinh()

    @staticmethod
    def atan(z):
        """ functional form of atan """
        return z.atan()

    @staticmethod
    def atanh(z):
        """ functional form of atanh """
        return z.atanh()

    @staticmethod
    def cos(z):
        """ functional form of cos """
        return z.cos()

    @staticmethod
    def cosh(z):
        """ functional form of cosh """
        return z.cosh()

    @staticmethod
    def sin(z):
        """ functional form of sin """
        return z.sin()

    @staticmethod
    def sinh(z):
        """ functional form of sinh """
        return z.sinh()

    @staticmethod
    def tan(z):
        """ functional form of tan """
        return z.tan()

    @staticmethod
    def tanh(z):
        """ functional form of tanh """
        return z.tanh()

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
