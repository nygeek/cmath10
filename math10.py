""" Implementation of some math functionality to extend the
    decimal.py library.

Started 2025-12-21
Split out from cmath10 2025-12-26

Copyright (C) 2025 NYGeek LLC

    ToDo list in README.md

"""

# ----- Python libraries ----- #
import json
from decimal import Decimal, getcontext, InvalidOperation

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

class Math10(Decimal):
    """ Class to implement trig and other math functions using
        decimal.py numbers. """

    @staticmethod
    def pi():
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


    @staticmethod
    def e():
        """ return e """
        return Decimal('1').exp()


# ----- trigonometric functions ----- #

    def cos(self):
        """ return cosine """
        # from docs.python.org/3/library/decimal.html#recipes.
        _twopi = 2 * Math10.pi()
        _x = self
        if ((_x > _twopi) or (_x < -_twopi)):
            _x %= _twopi
        getcontext().prec += 2
        i, lasts, s, fact, num, sign = 0, 0, 1, 1, 1, 1
        while s != lasts:
            lasts = s
            i += 2
            fact *= i * (i-1)
            num *= _x * _x
            sign *= -1
            s += num / fact * sign
        getcontext().prec -= 2
        return +s


    def sin(self):
        """ return sin """
        # from docs.python.org/3/library/decimal.html#recipes
        getcontext().prec += 2
        _twopi = 2 * Math10.pi()
        _x = self
        if ((_x > _twopi) or (_x < -_twopi)):
            _x %= _twopi
        i, lasts, s, fact, num, sign = 1, 0, _x, 1, _x, 1
        while s != lasts:
            lasts = s
            i += 2
            fact *= i * (i-1)
            num *= _x * _x
            sign *= -1
            s += num / fact * sign
        getcontext().prec -= 2
        return +s


    def tan(self):
        """ sin(x) / cos(x) """
        return Math10(Math10(self).sin() / Math10(self).cos())


    def acos(self):
        """ inverse cosine """
        return (Math10.pi() / 2) - self.asin()


    def asin(self):
        """ inverse sine
            Compute arcsin(x) using Taylor series.
            Valid for |x| <= 1
            arcsin(x) = x + (1/2)(x^3/3) + (1*3)/(2*4)(x^5/5)
                + (1*3*5)/(2*4*6)(x^7/7) + ...
            """
        getcontext().prec += 2
        _x = self
        if abs(_x) > 1:
            raise ValueError("arcsin(x) requires |x| <= 1")
        if abs(_x) > Decimal('0.7'):
            sign = 1 if _x >= 0 else -1
            result = Math10.pi() / 2 - \
                Math10((1 - _x*_x).sqrt()).asin() * sign
            getcontext().prec -= 2
            return Math10(+result)
        power = _x
        result = _x
        i = 1
        while True:
            power *= _x * _x * (2*i - 1) * (2*i - 1) / ((2*i) * (2*i + 1))
            term = power
            if abs(term) < Decimal(10) ** -(getcontext().prec - 2):
                break
            result += term
            i += 1
        getcontext().prec -= 2
        return Math10(+result)


    def atan(self):
        """ Compute arctan(x) using Taylor series.
        arctan(x) = x - x^3/3 + x^5/5 - x^7/7 + ...  for |x| <= 1
        For |x| > 1, use atan(x) = pi/2 - atan(1/x) for x > 0
                           or = -pi/2 - atan(1/x) for x < 0
        """
        getcontext().prec += 2
        _x = self
        # For |x| > 1, use the identity to improve convergence
        if abs(_x) > 1:
            sign = 1 if _x >= 0 else -1
            result = sign * Math10.pi() / 2 - Math10(1/_x).atan()
            getcontext().prec -= 2
            return Math10(+result)
        # For values close to 1, use atan(x) =
        #   pi/4 + atan((x-1)/(x+1)) to improve convergence
        if abs(_x) > Decimal('0.5'):
            result = Math10.pi() / 4
            if _x + 1 != 0:
                result += Math10((_x-1)/(_x+1)).atan()
            getcontext().prec -= 2
            return Math10(+result)
        power = _x
        result = _x
        i = 1
        while True:
            power *= -_x * _x
            term = power / (2 * i + 1)
            if abs(term) < Decimal(10) ** -(getcontext().prec - 2):
                break
            result += term
            i += 1
        getcontext().prec -= 2
        return Math10(+result)


    def atan2(self, y):
        """ inverse tangent x / y, with sign of y """
        getcontext().prec += 2
        _x = self
        _sign = 1
        if y < 0:
            _sign = -1
        _ratio = _x / y
        _result =  _sign * Math10(_ratio).atan()
        getcontext().prec -= 2
        return Math10(_result)


    def cosh(self):
        """ hyperbolic cosine """
        getcontext().prec += 2
        _result = (self.exp() + (-self).exp()) / 2
        getcontext().prec -=2
        return Math10(_result)


    def sinh(self):
        """ hyperbolic sine """
        getcontext().prec += 2
        _result = (self.exp() - (-self).exp()) / 2
        getcontext().prec -=2
        return Math10(_result)


    def tanh(self):
        """ hyperbolic sine """
        getcontext().prec += 2
        _result = (self.sinh() - (-self).cosh()) / 2
        getcontext().prec -=2
        return Math10(_result)


def main():
    """ simple smoke test """
    print("Smoke test is now in ssmoke.py.")


if __name__ == '__main__':
    main()
