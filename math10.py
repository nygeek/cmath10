""" Implementation of some math functionality to extend the
    decimal.py library.

Started 2025-12-21
Split out from cmath10 2025-12-26

SPDX-License-Identifier: MIT
Copyright (C) 2025 NYGeek LLC

ToDo list in README.md

"""

# ----- Python libraries ----- #
from decimal import Decimal, localcontext


class Math10(Decimal):
    """ Class to implement trig and other math functions using
        decimal.py numbers. """

    def __init__(self, rel_tol=1e-15):
        super().__init__()
        self.rel_tol = rel_tol


    def isclose(self, z, rel_tol=1e-9, abs_tol=0.0):
        """ Implement isclose according to PEP 485 """
        if self == z:
            return True
        if self.is_nan() or z.is_nan():
            return False
        if self.is_infinite() or z.is_infinite():
            return False
        diff = abs(self - z)
        ref = max(abs(self), abs(z))
        allowed = max(Math10(rel_tol) * Math10(ref), Math10(abs_tol))
        return diff <= allowed


    @classmethod
    def pi(cls):
        """ return pi """
        # docs.python.org/3/library/decimal.html#recipes
        with localcontext() as ctx:
            ctx.prec += 2
            three = Decimal(3)
            lasts, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24
            while s != lasts:
                lasts = s
                n, na = n+na, na+8
                d, da = d+da, da+32
                t = (t * n) / d
                s += t
        return cls(+s)


    @classmethod
    def e(cls):
        """ return e """
        return cls('1').exp()

# ----- trigonometric functions ----- #

    def cos(self):
        """ return cosine """
        # from docs.python.org/3/library/decimal.html#recipes.
        with localcontext() as ctx:
            ctx.prec += 2

            twopi = 2 * self.pi()
            x = self

            if ((x > twopi) or (x < -twopi)):
                x %= twopi

            i, lasts, s, fact, num, sign = 0, 0, 1, 1, 1, 1
            while s != lasts:
                lasts = s
                i += 2
                fact *= i * (i-1)
                num *= x * x
                sign *= -1
                s += num / fact * sign

        return self.__class__(+s)


    def sin(self):
        """ return sin """
        # from docs.python.org/3/library/decimal.html#recipes
        with localcontext() as ctx:
            ctx.prec += 2

            twopi = 2 * Math10.pi()
            x = self
            if ((x > twopi) or (x < -twopi)):
                x %= twopi
            i, lasts, s, fact, num, sign = 1, 0, x, 1, x, 1
            while s != lasts:
                lasts = s
                i += 2
                fact *= i * (i-1)
                num *= x * x
                sign *= -1
                s += num / fact * sign

        return self.__class__(+s)


    def tan(self):
        """ sin(x) / cos(x) """
        return self.__class__(self.sin() / self.cos())


    def acos(self):
        """ inverse cosine """
        result = (self.pi() / 2) - self.asin()
        return self.__class__(result)


    def asin(self):
        """ inverse sine
            Compute arcsin(x) using Taylor series.
            Valid for |x| <= 1
            arcsin(x) = x + (1/2)(x^3/3) + (1*3)/(2*4)(x^5/5)
                + (1*3*5)/(2*4*6)(x^7/7) + ...
            """
        with localcontext() as ctx:
            cutoff = Decimal(10) ** -ctx.prec
            ctx.prec += 2

            x = self
            if abs(x) > 1:
                raise ValueError("arcsin(x) requires |x| <= 1")
            if abs(x) > Decimal('0.7'):
                sign = 1 if x >= 0 else -1
                # arcsin(x) = sign * (pi/2 - arcsin(sqrt(1-x^2)))
                result = sign * (self.pi() / 2 - \
                    self.__class__((1 - x*x).sqrt()).asin())
                return self.__class__(+result)
            power = x
            result = x
            i = 1
            while True:
                power *= x * x * (2*i - 1) * (2*i - 1) / ((2*i) * (2*i + 1))
                term = power
                if abs(term) < cutoff:
                    break
                result += term
                i += 1

        return self.__class__(+result)


    def atan(self):
        """ Compute arctan(x) using Taylor series.
        arctan(x) = x - x^3/3 + x^5/5 - x^7/7 + ...  for |x| <= 1
        For |x| > 1, use atan(x) = pi/2 - atan(1/x) for x > 0
                           or = -pi/2 - atan(1/x) for x < 0
        """
        with localcontext() as ctx:
            cutoff = Decimal(10) ** -ctx.prec
            ctx.prec += 2

            x = self

            # For |x| > 1, use the identity to improve convergence
            if abs(x) > 1:
                sign = 1 if x >= 0 else -1
                result = sign * self.__class__.pi() / 2 \
                        - self.__class__(1/x).atan()
                return self.__class__(+result)

            # For values close to 1, use atan(x) =
            #   pi/4 + atan((x-1)/(x+1)) to improve convergence
            if abs(x) > Decimal('0.5'):
                pi_4 = self.__class__.pi() / 4
                if x == self.__class__(1):
                    return pi_4
                if x == self.__class__(-1):
                    return -pi_4
                if x > 0:
                    result = pi_4 + self.__class__((x-1)/(x+1)).atan()
                else:
                    result = -pi_4 + self.__class__((x-1)/(x+1)).atan()
                return self.__class__(+result)

            power = x
            result = x
            i = 1
            while True:
                power *= -1 * x * x
                term = power / (2 * i + 1)
                if abs(term) < cutoff:
                    break
                result += term
                i += 1

        return self.__class__(+result)


    @classmethod
    def atan2(cls, y, x):
        """ inverse tangent y/x in radians """
        y = cls(y)
        x = cls(x)

        with localcontext() as ctx:
            ctx.prec += 2

            pi = cls.pi()
            zero = cls(0)

            if x > zero:
                # quadrants 1 and 4
                result = cls(y/x).atan()
            elif x < zero:
                if y >= zero:
                    result = cls(y/x).atan() + pi
                else:
                    result = cls(y/x).atan() - pi
            else: # x is zero
                if y > zero:
                    result = pi / 2
                elif y < zero:
                    result = -1 * cls(pi) / 2
                else:
                    result = zero

        return cls(result)


    def cosh(self):
        """ hyperbolic cosine """
        with localcontext() as ctx:
            ctx.prec += 2
            result = (self.exp() + (-1 * self).exp()) / 2
            return self.__class__(result)


    def acosh(self):
        """ inverse hyperbolic cosine """
        if self < self.__class__(1):
            raise ValueError("Math10 domain error")
        with localcontext() as ctx:
            ctx.prec += 2
            one = self.__class__(1)
            result = (self + ((self * self) - one).sqrt()).ln()
            return self.__class__(result)


    def sinh(self):
        """ hyperbolic sine """
        with localcontext() as ctx:
            ctx.prec += 2
            result = (self.exp() - (-1 * self).exp()) / 2
            return self.__class__(result)


    def asinh(self):
        """ inverse hyperbolic sin """
        with localcontext() as ctx:
            ctx.prec += 2
            one = self.__class__(1)
            result = (self + (one + (self * self)).sqrt()).ln()
            return self.__class__(result)


    def tanh(self):
        """ hyperbolic sine """
        with localcontext() as ctx:
            ctx.prec += 2
            result = self.sinh() / self.cosh()
            return self.__class__(result)


    def atanh(self):
        """ inverse hyperbolic tangent """
        if self > self.__class__(1) or self < self.__class__(-1):
            raise ValueError("Math10 domain error")
        with localcontext() as ctx:
            ctx.prec += 2
            result = ((1 + self) / (1 - self)).ln() / 2
            return self.__class__(result)


class StdLibAdapter:
    """ functional forms for all of the Math10 (scalar) functions """
    Scalar = Math10

    @staticmethod
    def isclose(z, rel_tol=1e-9, abs_tol=0.0):
        """ functional form of isclose """
        return Math10.isclose(z, rel_tol, abs_tol)


    @staticmethod
    def pi():
        """ functional form of pi """
        return Math10.pi()


    @staticmethod
    def e():
        """ functional form of e """
        return Math10.e()


    @staticmethod
    def cos(x):
        """ functional form of cos """
        return Math10(x).cos()


    @staticmethod
    def sin(x):
        """ functional form of sin """
        return Math10(x).sin()


    @staticmethod
    def tan(x):
        """ functional form of tan """
        return Math10(x).tan()


    @staticmethod
    def acos(x):
        """ functional form of acos """
        return Math10(x).acos()


    @staticmethod
    def asin(z):
        """ functional form of asin """
        return Math10(z).asin()


    @staticmethod
    def atan(x):
        """ functional form of atan """
        return Math10(x).atan()


    @staticmethod
    def cosh(x):
        """ functional form of cosh """
        return Math10(x).cosh()


    @staticmethod
    def acosh(x):
        """ functional form of acosh """
        return Math10(x).acosh()


    @staticmethod
    def sinh(x):
        """ functional form of sinh """
        return Math10(x).sinh()


    @staticmethod
    def asinh(x):
        """ functional form of asinh """
        return Math10(x).asinh()


    @staticmethod
    def tanh(x):
        """ functional form of tanh """
        return Math10(x).tanh()

    @staticmethod
    def atanh(x):
        """ functional form of tanh """
        return Math10(x).atanh()

    @staticmethod
    def atan2(y, x):
        """ functional form of atan2 """
        return Math10.atan2(y, x)


def main():
    """ simple smoke test """
    print("Smoke test is now in ssmoke.py.")


if __name__ == '__main__':
    main()
