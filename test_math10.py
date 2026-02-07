# Unit test suite for math10.py
#
# Mirrors the structure and test data format of CPython's
# Lib/test/test_math.py
# but runs against math10 (StdLibAdapter) instead of
# the built-in math module.
# Uses the same cmath_testcases.txt format;
# comparison is via Math10.isclose()
# (rel_tol/abs_tol) instead of ULP.
#
# SPDX-License-Identifier: MIT

import os
import unittest
import math as builtin_math

from math10 import StdLibAdapter as m
from math10 import Math10

# Tolerances for Decimal vs float expected (PEP 485 style)
REL_TOL = 1e-12
ABS_TOL = 1e-15

# Locate test data (same layout as test_math.py)
_TEST_DIR = os.path.dirname(os.path.abspath(__file__))
MATHDATA_DIR = os.path.join(_TEST_DIR, 'mathdata')
CMATH_TESTCASES = os.path.join(MATHDATA_DIR, 'cmath_testcases.txt')

# Functions implemented by math10 (real-only use from cmath test file)
MATH10_FUNCTIONS = frozenset({
    'cos', 'sin', 'tan', 'acos', 'asin', 'atan',
    'cosh', 'sinh', 'tanh', 'acosh', 'asinh', 'atanh',
})


def parse_testfile(fname):
    """Parse cmath-style test file.

    Empty lines or lines starting with -- are ignored.
    Yields: (id, fn, arg_real, arg_imag, exp_real, exp_imag, flags).
    """
    with open(fname, encoding='utf-8') as fp:
        for line in fp:
            if line.startswith('--') or not line.strip():
                continue
            lhs, rhs = line.split('->')
            id_, fn, arg_real, arg_imag = lhs.split()
            rhs_pieces = rhs.split()
            exp_real, exp_imag = rhs_pieces[0], rhs_pieces[1]
            flags = rhs_pieces[2:] if len(rhs_pieces) > 2 else []
            yield (
                id_, fn,
                float(arg_real), float(arg_imag),
                float(exp_real), float(exp_imag),
                flags,
            )


def result_check(expected, got, rel_tol=REL_TOL, abs_tol=ABS_TOL):
    """
    Compare expected (float) and got (Math10/Decimal). Return None
    if ok, else error str.
    """
    try:
        exp = Math10(str(expected))
    except Exception:
        # non-finite or invalid
        return f"expected {expected!r}, got {got!r} (could not build expected Math10)"
    if exp.is_nan() and got.is_nan():
        return None
    if exp.is_infinite() and got.is_infinite():
        if (exp > 0) != (got > 0):
            return f"expected {expected!r}, got {got!r} (sign mismatch)"
        return None
    if exp.isclose(got, rel_tol=rel_tol, abs_tol=abs_tol):
        return None
    return f"expected {expected!r}, got {got!r} (not close)"


class Math10Tests(unittest.TestCase):
    """
	Tests mirroring CPython MathTests for functions implemented
	in math10.
    """

    def ftest(self, name, got, expected, rel_tol=REL_TOL, abs_tol=ABS_TOL):
        """Compare got (Math10) vs expected (float) with tolerance."""
        failure = result_check(expected, got, rel_tol=rel_tol, abs_tol=abs_tol)
        if failure is not None:
            self.fail(f"{name}: {failure}")

    def test_constants(self):
        """pi and e (ref: Abramowitz & Stegun)."""
        self.ftest('pi', m.pi(), 3.141592653589793238462643)
        self.ftest('e', m.e(), 2.718281828459045235360287)

    def test_acos(self):
        self.ftest('acos(-1)', m.acos(-1), builtin_math.pi)
        self.ftest('acos(0)', m.acos(0), builtin_math.pi / 2)
        self.ftest('acos(1)', m.acos(1), 0)
        self.assertRaises(ValueError, m.acos, 1.00001)
        self.assertRaises(ValueError, m.acos, -1.00001)

    def test_acosh(self):
        self.ftest('acosh(1)', m.acosh(1), 0)
        self.ftest('acosh(2)', m.acosh(2), 1.3169578969248168)
        self.assertRaises(ValueError, m.acosh, 0)
        self.assertRaises(ValueError, m.acosh, -1)

    def test_asin(self):
        self.ftest('asin(-1)', m.asin(-1), -builtin_math.pi / 2)
        self.ftest('asin(0)', m.asin(0), 0)
        self.ftest('asin(1)', m.asin(1), builtin_math.pi / 2)
        self.assertRaises(ValueError, m.asin, 1.00001)
        self.assertRaises(ValueError, m.asin, -1.00001)

    def test_asinh(self):
        self.ftest('asinh(0)', m.asinh(0), 0)
        self.ftest('asinh(1)', m.asinh(1), 0.88137358701954305)
        self.ftest('asinh(-1)', m.asinh(-1), -0.88137358701954305)

    def test_atan(self):
        self.ftest('atan(-1)', m.atan(-1), -builtin_math.pi / 4)
        self.ftest('atan(0)', m.atan(0), 0)
        self.ftest('atan(1)', m.atan(1), builtin_math.pi / 4)

    def test_atanh(self):
        self.ftest('atanh(0)', m.atanh(0), 0)
        self.ftest('atanh(0.5)', m.atanh(0.5), 0.54930614433405489)
        self.ftest('atanh(-0.5)', m.atanh(-0.5), -0.54930614433405489)
        self.assertRaises(ValueError, m.atanh, 1)
        self.assertRaises(ValueError, m.atanh, -1)

    def test_atan2(self):
        self.ftest('atan2(-1, 0)', m.atan2(-1, 0), -builtin_math.pi / 2)
        self.ftest('atan2(-1, 1)', m.atan2(-1, 1), -builtin_math.pi / 4)
        self.ftest('atan2(0, 1)', m.atan2(0, 1), 0)
        self.ftest('atan2(1, 1)', m.atan2(1, 1), builtin_math.pi / 4)
        self.ftest('atan2(1, 0)', m.atan2(1, 0), builtin_math.pi / 2)
        self.ftest('atan2(1, -1)', m.atan2(1, -1), 3 * builtin_math.pi / 4)

    def test_cos(self):
        self.ftest('cos(0)', m.cos(0), 1)
        self.ftest('cos(pi/2)', m.cos(builtin_math.pi / 2), 0, abs_tol=1e-14)
        self.ftest('cos(pi)', m.cos(builtin_math.pi), -1)

    def test_sin(self):
        self.ftest('sin(0)', m.sin(0), 0)
        self.ftest('sin(pi/2)', m.sin(builtin_math.pi / 2), 1)
        self.ftest('sin(pi)', m.sin(builtin_math.pi), 0, abs_tol=1e-14)

    def test_tan(self):
        self.ftest('tan(0)', m.tan(0), 0)
        self.ftest('tan(pi/4)', m.tan(builtin_math.pi / 4), 1)

    def test_cosh(self):
        self.ftest('cosh(0)', m.cosh(0), 1)
        self.ftest('cosh(2)-2*cosh(1)**2', m.cosh(2) - 2 * m.cosh(1) ** 2, -1)

    def test_sinh(self):
        self.ftest('sinh(0)', m.sinh(0), 0)
        self.ftest('sinh(1)', m.sinh(1), 1.1752011936438014)

    def test_tanh(self):
        self.ftest('tanh(0)', m.tanh(0), 0)
        self.ftest('tanh(1)', m.tanh(1), 0.76159415595576485)

    @unittest.skipUnless(os.path.isfile(CMATH_TESTCASES), "mathdata/cmath_testcases.txt not found")
    def test_mtestcases(self):
        """Run real-axis cases from cmath_testcases.txt for math10 functions."""
        skip_flags = {'divide-by-zero', 'overflow', 'invalid'}
        run = 0
        fail = 0
        for (id_, fn, arg_real, arg_imag, exp_real, exp_imag, flags) in parse_testfile(CMATH_TESTCASES):
            if fn not in MATH10_FUNCTIONS:
                continue
            if arg_imag != 0.0:  # only real-axis inputs
                continue
            if any(f in flags for f in skip_flags):
                continue
            if builtin_math.isnan(exp_real) or builtin_math.isinf(exp_real):
                continue
            run += 1
            try:
                if fn == 'atan2':
                    continue  # atan2 not in cmath file as single-arg
                func = getattr(m, fn)
                got = func(arg_real)
                failure = result_check(exp_real, got)
                if failure is not None:
                    fail += 1
                    self.fail(f"{id_} {fn}({arg_real}): {failure}")
            except (ValueError, ZeroDivisionError) as e:
                # domain error etc. may be expected for some cases
                fail += 1
                self.fail(f"{id_} {fn}({arg_real}): raised {e!r}")
        self.assertGreater(run, 0, "no test cases ran (check mathdata/cmath_testcases.txt)")


if __name__ == '__main__':
    unittest.main()
