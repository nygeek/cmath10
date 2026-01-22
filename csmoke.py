""" Smoke test for CMath10 class

Started 2025-12-24

Copyright (C) 2025 NYGeek LLC

"""

# ----- Python libraries ----- #
import unittest

# ----- Local libraries ----- #
from trace_debug import DebugTrace
from cmath10 import CMath10 as cm

class TestCMathMethods(unittest.TestCase):

    def test_add(self):
        """ test complex addition """
        a = cm("1", "3")
        b = cm("2.1", "7.9")
        self.assertTrue(cm.isclose(a.add(b), cm("3.1", "10.9")))

    def test_sub(self):
        """ test complex subtraction """
        a = cm("1", "3")
        b = cm("2.1", "7.9")
        self.assertTrue(cm.isclose(a.sub(b), cm("-1.1", "-4.9")))

    def test_mul(self):
        """ test complex multiplication """
        a = cm("1", "3")
        b = cm("2.1", "7.9")
        self.assertTrue(cm.isclose(a.mul(b), cm("-21.6", "14.2")))

    def test_div_1(self):
        """ test complex division 1 """
        a = cm("1", "3")
        b = cm("2.1", "7.9")
        self.assertTrue(cm.isclose(a.div(b),
                         cm("0.3861119425321759952110146662675846", \
                            "-0.02394492666866207722238850643519904")))

    def test_div_2(self):
        """ test complex division 2 """
        a = cm("1", "1")
        b = cm("1", "-1")
        self.assertTrue(cm.isclose(a.div(b), cm("0","1")))

    def test_euler(self):
        """ test Euler's Identity """
        zero = cm(0, 0)
        one = cm(1,0)
        i = cm(0,1)
        pi = cm.pi()
        res = i.mul(pi).exp().add(one)
        self.assertTrue(cm.isclose(res, zero, abs_tol = 1e-15))

    def test_phase_1(self):
        """ phase(1,1) """
        expected = cm(0.7853981633974483096, 0)
        actual = cm(1,1).phase()
        self.assertTrue(cm.isclose(actual, expected))

    def test_phase_2(self):
        """ phase(1,-1) """
        expected = cm(-0.7853981633974483096, 0)
        actual = cm(1,-1).phase()
        self.assertTrue(cm.isclose(actual, expected))

    def test_abs(self):
        """ abs(3+4i) is 5 """
        expected = cm(5, 0)
        actual = cm(3,4).abs()
        self.assertTrue(cm.isclose(actual, expected))

    def test_log(self):
        """
        ln(3+4i) is (1.6094379124341003746007593332262
                     +0.927295218001612232428512462922428682i)
        """
        expected = cm("1.6094379124341003746007593332262",\
                      "0.9272952180016122324285124629224")
        actual = cm(3,4).log()
        self.assertTrue(cm.isclose(actual, expected))

    def test_exp(self):
        """
        exp(3+4i) is (-13.128783081462158-15.200784463067956j)
        """
        expected = cm("-13.128783081462158", "-15.200784463067956")
        actual = cm(3,4).exp()
        self.assertTrue(cm.isclose(actual, expected))

    def test_sqrt_1(self):
        """
        sqrt(3+4i) is (2+i)
        """
        expected = cm("2", "1")
        actual = cm(3,4).sqrt()
        self.assertTrue(cm.isclose(actual, expected))

    def test_sqrt_2(self):
        """
        sqrt(2+2i) is (1.5537739740300374+0.6435942529055826i)
        """
        expected = cm("1.5537739740300374", "0.6435942529055826")
        actual = cm(2,2).sqrt()
        self.assertTrue(cm.isclose(actual, expected))

def oldmain():
    """ simple smoke test """
    DebugTrace(False)

    z = CMath10("4", "0")
    z2 = z.sqrt()
    print(f"sqrt(z: {z}): {z2}")
    z = CMath10("-4", "0")
    z2 = z.sqrt()
    print(f"sqrt(z: {z}): {z2}\n")

    z = CMath10("0", "1")
    z2 = z.sqrt()
    print(f"sqrt(z: {z}): {z2}\n")

    z = CMath10("1", "1")
    z2 = z.sin()
    print(f"sin(z: {z}): {z2}")
    z = CMath10("1", "1")
    z2 = z.cos()
    print(f"cos(z: {z}): {z2}")
    z = CMath10("1", "1")
    z2 = z.tan()
    print(f"tan(z: {z}): {z2}\n")

    e = CMath10.e()
    print(f"e(): {e}")
    pi = CMath10.pi()
    print(f"pi(): {pi}")

    z = CMath10(1,1)
    print(f"z: {z}")
    print(f"z^2: {z.mul(z)}")

    z1 = CMath10(3, 4)
    print(f"z1: {z1}")
    z2 = CMath10(1, 2)
    print(f"z2: {z2}")
    print("(expect 2.2 - 0.4i)")
    print(f"z1/z2: {z1.div(z2)}")

    z = CMath10("1", "1")
    print("(expect: (0.8337300251311491-0.9888977057628651j))")
    print(f"cos(z: {z}): {z.cos()}")

    z = CMath10("1", "1")
    print(f"z: {z}")
    print(f"cos(z): {z.cos()}")
    print(f"acos(cos(z: {z})): {z.cos().acos()}")

    z = CMath10(0, 0)
    print(f"z: {z}")
    print(f"acos(z): {z.acos()}")

    z = CMath10(-1, 0)
    print(f"z: {z}")
    print(f"acos(z): {z.acos()}")


if __name__ == '__main__':
    unittest.main()
