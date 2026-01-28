""" Smoke test for CMath10 class

Started 2025-12-24

Copyright (C) 2025 NYGeek LLC

"""

# ----- Python libraries ----- #
import unittest

# ----- Local libraries ----- #
# from trace_debug import DebugTrace
from cmath10 import CMath10 as cm

class TestCMathMethods(unittest.TestCase):
    """ Smoke Tests for CMath10 """

    def test_add_1(self):
        """ test complex addition """
        a = cm("1", "3")
        b = cm("2.1", "7.9")
        self.assertTrue(cm.isclose(a.add(b), cm("3.1", "10.9")))

    def test_sub_1(self):
        """ test complex subtraction """
        a = cm("1", "3")
        b = cm("2.1", "7.9")
        self.assertTrue(cm.isclose(a.sub(b), cm("-1.1", "-4.9")))

    def test_mul_1(self):
        """ test complex multiplication """
        a = cm("1", "3")
        b = cm("2.1", "7.9")
        self.assertTrue(cm.isclose(a.mul(b), cm("-21.6", "14.2")))

    def test_div_1(self):
        """ test complex multiplication """
        a = cm("3", "4")
        b = cm("1", "2")
        actual = a.div(b)
        expected = cm("2.2", "-0.4")
        self.assertTrue(cm.isclose(actual, expected))

    def test_div_2(self):
        """ test complex division 1 """
        a = cm("1", "3")
        b = cm("2.1", "7.9")
        self.assertTrue(cm.isclose(a.div(b),
                         cm("0.3861119425321759952110146662675846", \
                            "-0.02394492666866207722238850643519904")))

    def test_div_3(self):
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

    def test_abs_1(self):
        """ abs(3+4i) is 5 """
        expected = cm(5, 0)
        actual = cm(3,4).abs()
        self.assertTrue(cm.isclose(actual, expected))

    def test_log_1(self):
        """
        ln(3+4i) is (1.6094379124341003746007593332262
                     +0.927295218001612232428512462922428682i)
        """
        expected = cm("1.6094379124341003746007593332262",\
                      "0.9272952180016122324285124629224")
        actual = cm(3,4).log()
        self.assertTrue(cm.isclose(actual, expected))

    def test_exp_1(self):
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

    def test_sqrt_3(self):
        """
        sqrt(4+0i) is (2+0i)
        """
        expected = cm("2", "0")
        actual = cm(4,0).sqrt()
        self.assertTrue(cm.isclose(actual, expected))

    def test_sqrt_4(self):
        """
        sqrt(-4+0i) is (0+2i)
        """
        expected = cm("0", "2")
        actual = cm(-4,0).sqrt()
        self.assertTrue(cm.isclose(actual, expected))

    def test_sqrt_5(self):
        """
        sqrt(0+1i) is (0.7071067811865476+0.7071067811865475i)
        """
        expected = cm("0.7071067811865476", "0.7071067811865476")
        actual = cm(0,1).sqrt()
        self.assertTrue(cm.isclose(actual, expected))

    def test_sin_1(self):
        """
        sin(1+1i) is (1.2984575814159773+0.6349639147847361i)
        """
        expected = cm("1.2984575814159773", "0.6349639147847361")
        actual = cm(1,1).sin()
        self.assertTrue(cm.isclose(actual, expected))

    def test_cos_1(self):
        """
        cos(1+1i) is (0.8337300251311491-0.9888977057628651i)
        """
        expected = cm("0.8337300251311491","-0.9888977057628651")
        actual = cm(1,1).cos()
        self.assertTrue(cm.isclose(actual, expected))

    def test_tan_1(self):
        """
        tan(1+1i) is (0.2717525853195118+1.0839233273386943i)
        """
        expected = cm("0.2717525853195118","1.0839233273386943")
        actual = cm(1,1).tan()
        self.assertTrue(cm.isclose(actual, expected))

    def test_e_1(self):
        """
        e is (2.718281828459045+0i)
        """
        expected = cm("2.718281828459045","0")
        actual = cm.e()
        self.assertTrue(cm.isclose(actual, expected))

    def test_pi_1(self):
        """
        pi is (3.141592653589793+0i)
        """
        expected = cm("3.141592653589793","0")
        actual = cm.pi()
        self.assertTrue(cm.isclose(actual, expected))

    def test_square_1(self):
        """
        (1+i)^2 is (0+2i)
        """
        expected = cm("0","2")
        actual = cm(1,1).mul(cm(1,1))
        self.assertTrue(cm.isclose(actual, expected))

    def test_acos_1(self):
        """
        (1+1i).cos().acos() is (1+1i)
        """
        expected = cm("1","1")
        actual = cm(1,1).cos().acos()
        self.assertTrue(cm.isclose(actual, expected))

    def test_acos_2(self):
        """
        (0+0i).acos() is (1.5707963267948966-0i)
        """
        expected = cm("1.5707963267948966", "-0")
        actual = cm(0,0).acos()
        self.assertTrue(cm.isclose(actual, expected))

    def test_acos_3(self):
        """
        (-1+0i).acos() is (pi, 0)
        """
        expected = cm.pi()
        actual = cm(-1,0).acos()
        self.assertTrue(cm.isclose(actual, expected))


if __name__ == '__main__':
    unittest.main()
