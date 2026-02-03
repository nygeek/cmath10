""" Smoke test for Math10 class

Started 2025-12-24

Copyright (C) 2025 NYGeek LLC

"""

# ----- Python libraries ----- #
# from decimal import Decimal
import unittest

# ----- Local libraries ----- #
# from trace_debug import DebugTrace
from math10 import StdLibAdapter as m

class TestMath10Methods(unittest.TestCase):
    """ Smoke test for Math10 """

    def test_pi(self):
        """ does pi() return the right value? """
        expected = m.Scalar("3.14159265358979323846264338328")
        actual = m.pi()
        self.assertTrue(m.Scalar.isclose(expected, actual))

    def test_e(self):
        """ does e() return the right value? """
        expected = m.Scalar("2.7182818284590452353602874713527")
        actual = m.e()
        self.assertTrue(m.Scalar.isclose(expected, actual))

    def test_pi_on_four(self):
        """ does pi/4 have the right value? """
        expected = m.Scalar("0.785398163397448309615660845819875")
        actual = m.pi() / m.Scalar("4")
        self.assertTrue(m.Scalar.isclose(expected, actual))

    def test_cos_pi_on_four(self):
        """ does cos(pi/4) have the right value? """
        expected = m.Scalar("0.7071067811865475244008443621048495")
        actual = m.Scalar(m.pi() / m.Scalar("4")).cos()
        self.assertTrue(m.Scalar.isclose(expected, actual))

    def test_tan_pi_on_four(self):
        """ does tan(pi/4) have the right value? """
        expected = m.Scalar("1")
        actual = m.Scalar(m.pi() / m.Scalar("4")).tan()
        self.assertTrue(m.Scalar.isclose(expected, actual))

    # The default setting for the comparison parameters for isclose
    # are such that IEEE 754 floating point numbers (as used by cnc)
    # will match the decimal numbers (as used by cnc10).  This means
    # that the test suite from cmath should work as is, except for
    # the funny +0, -0 stuff that indicates branch.

    def test_pi_on_five(self):
        """ does pi/5 have the right value? """
        expected = m.Scalar("0.6283185307179586")
        actual = m.pi() / m.Scalar("5")
        self.assertTrue(m.Scalar.isclose(expected, actual))

    def test_sin_pi_on_five(self):
        """ does sin(pi/5) have the right value? """
        expected =  m.Scalar("0.5877852522924731")
        actual = m.Scalar(m.pi() / m.Scalar("5")).sin()
        self.assertTrue(m.Scalar.isclose(expected, actual))

    def test_sin_asin_pi_on_five(self):
        """ does asin(sin(pi/5)) have the right value? """
        expected = m.Scalar("0.6283185307179586")
        actual = m.Scalar(m.pi() / m.Scalar("5")).sin().asin()
        self.assertTrue(m.Scalar.isclose(expected, actual))

    def test_cos_acos_pi_on_five(self):
        """ does acos(cos(pi/5)) have the right value? """
        expected = m.Scalar("0.6283185307179586")
        actual = m.Scalar(m.pi() / m.Scalar("5")).cos().acos()
        self.assertTrue(m.Scalar.isclose(expected, actual))

    def test_tan_pi_on_five(self):
        """ does tan(pi/5) have the right value? """
        expected = m.Scalar("0.7265425280053609")
        actual = m.Scalar(m.pi() / m.Scalar("5")).tan()
        self.assertTrue(m.Scalar.isclose(expected, actual))

    def test_tan_atan_pi_on_five(self):
        """ does atan(tan(pi/5)) have the right value? """
        expected = m.Scalar("0.6283185307179586")
        actual = m.Scalar(m.pi() / m.Scalar("5")).tan().atan()
        self.assertTrue(m.Scalar.isclose(expected, actual))

    def test_atan2_1(self):
        """ doe atan2(1,1) have the right value? """
        expected = m.Scalar("0.78539816339744830961566084581987572")
        actual = m.Scalar(m.atan2(1, 1))
        self.assertTrue(m.Scalar.isclose(expected, actual))

    def test_atan2_2(self):
        """ doe atan2(-1,1) have the right value? """
        expected = m.Scalar("-0.78539816339744830961566084581987572")
        actual = m.Scalar(m.atan2(-1, 1))
        self.assertTrue(m.Scalar.isclose(expected, actual))

    # These cosh, sinh, and tanh test cases come from
    # github.com/python/cpython/Lib/test/Mathdata/cmath_testcases.txt

    def test_cosh_1(self):
        """ does cosh() have the right value? """
        expected = m.Scalar("2.0000000000000001504")
        actual = m.Scalar(m.cosh(1.3169578969248168))
        self.assertTrue(m.Scalar.isclose(expected, actual))

    def test_cosh_2(self):
        """ does cosh() have the right value? """
        expected = m.Scalar("2.0000000000000001504")
        actual = m.Scalar(m.cosh(1.3169578969248168))
        self.assertTrue(m.Scalar.isclose(expected, actual))

    def test_acosh_1(self):
        """ does acosh() have the right value? """
        expected = m.Scalar("1.3169578969248168")
        actual = m.Scalar(m.acosh(2))
        self.assertTrue(m.Scalar.isclose(expected, actual))

    def test_sinh_1(self):
        """ does sinh() have the right value? """
        expected = m.Scalar("1.9999999999999999078")
        actual = m.Scalar(m.sinh(1.4436354751788103))
        self.assertTrue(m.Scalar.isclose(expected, actual))

    def test_sinh_2(self):
        """ does sinh() have the right value? """
        expected = m.Scalar("-1.9999999999999999078")
        actual = m.Scalar(m.sinh(-1.4436354751788103))
        self.assertTrue(m.Scalar.isclose(expected, actual))

    def test_asinh_1(self):
        """ does asinh() have the right value? """
        # this is test_sinh_2 inverted
        expected = m.Scalar("-1.4436354751788103")
        actual = m.Scalar(m.asinh(-1.9999999999999999078))
        self.assertTrue(m.Scalar.isclose(expected, actual))

    def test_tanh_1(self):
        """ does tanh() have the right value? """
        expected = m.Scalar("0.50000000000000003402")
        actual = m.Scalar(m.tanh(0.5493061443340549))
        self.assertTrue(m.Scalar.isclose(expected, actual))

    def test_tanh_2(self):
        """ does tanh() have the right value? """
        expected = m.Scalar("-0.50000000000000003402")
        actual = m.Scalar(m.tanh(-0.5493061443340549))
        self.assertTrue(m.Scalar.isclose(expected, actual))

    def test_atanh_1(self):
        """ does atanh() have the right value? """
        expected = m.Scalar("0.5493061443340549")
        actual = m.Scalar(m.atanh(0.50000000000000003402))
        self.assertTrue(m.Scalar.isclose(expected, actual))

if __name__ == '__main__':
    unittest.main()
