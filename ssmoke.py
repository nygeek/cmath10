""" Smoke test for Math10 class

Started 2025-12-24

Copyright (C) 2025 NYGeek LLC

"""

# ----- Python libraries ----- #
from decimal import Decimal
import unittest

# ----- Local libraries ----- #
# from trace_debug import DebugTrace
from math10 import StdLibAdapter as m

class TestMath10Methods(unittest.TestCase):

    def test_pi(self):
        self.assertTrue(
                m.Scalar.isclose(m.pi(), 
                       m.Scalar("3.14159265358979323846264338328")))

    def test_e(self):
        self.assertTrue(
                m.Scalar.isclose(
                    m.e(),
                    m.Scalar("2.7182818284590452353602874713527")))

    def test_pi_on_four(self):
        self.assertTrue(
                m.Scalar.isclose(
                    m.pi() / m.Scalar("4"),
                    m.Scalar("0.785398163397448309615660845819875")))

    def test_cos_pi_on_four(self):
        x = m.Scalar(m.pi() / m.Scalar("4"))
        self.assertTrue(
                m.Scalar.isclose(
                    x.cos(),
                    m.Scalar("0.7071067811865475244008443621048495")))

    def test_tan_pi_on_four(self):
        x = m.Scalar(m.pi() / m.Scalar("4"))
        self.assertTrue(
                m.Scalar.isclose(
                    x.tan(),
                    m.Scalar("1")))

    # The default setting for the comparison parameters for isclose
    # are such that IEEE 754 floating point numbers (as used by cnc)
    # will match the decimal numbers (as used by cnc10).  This means
    # that the test suite from cmath should work as is, except for
    # the funny +0, -0 stuff that indicates branch.

    def test_pi_on_five(self):
        self.assertTrue(
                m.Scalar.isclose(
                    m.pi() / m.Scalar("5"),
                    m.Scalar("0.6283185307179586")))

    def test_sin_pi_on_five(self):
        x = m.Scalar(m.pi() / m.Scalar("5"))
        self.assertTrue(
                m.Scalar.isclose(
                    x.sin(),
                    m.Scalar("0.5877852522924731")))

    def test_sin_asin_pi_on_five(self):
        x = m.Scalar(m.pi() / m.Scalar("5"))
        self.assertTrue(
                m.Scalar.isclose(
                    x.sin().asin(),
                    m.Scalar("0.6283185307179586")))

    def test_cos_acos_pi_on_five(self):
        x = m.Scalar(m.pi() / m.Scalar("5"))
        self.assertTrue(
                m.Scalar.isclose(
                    x.cos().acos(),
                    m.Scalar("0.6283185307179586")))

    def test_tan_pi_on_five(self):
        x = m.Scalar(m.pi() / m.Scalar("5"))
        self.assertTrue(
                m.Scalar.isclose(
                    x.tan(),
                    m.Scalar("0.7265425280053609")))

    def test_sin_asin_pi_on_five(self):
        x = m.Scalar(m.pi() / m.Scalar("5"))
        self.assertTrue(
                m.Scalar.isclose(
                    x.tan().atan(),
                    m.Scalar("0.6283185307179586")))

    def test_atan2_1(self):
        x = m.Scalar(m.atan2(1, 1))
        self.assertTrue(
                x.isclose(
                    m.Scalar("0.78539816339744830961566084581987572")))

    def test_atan2_2(self):
        x = m.Scalar(m.atan2(-1, 1))
        self.assertTrue(
                x.isclose(
                    m.Scalar("-0.78539816339744830961566084581987572")))

if __name__ == '__main__':
    unittest.main()
