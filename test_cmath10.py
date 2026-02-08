""" Unit test suite for cmath10.py

Mirrors the structure and test data format of CPython's
Lib/test/test_cmath.py but runs against cmath10 (StdLibAdapter /
CMath10) instead of the built-in cmath.

Uses mathdata/cmath_testcases.txt; comparison is via CMath10.isclose().

SPDX-License-Identifier: MIT
"""

import os
import unittest
import math as builtin_math

from cmath10 import CMath10, StdLibAdapter as c
from math10 import Math10

# Tolerances for complex Decimal vs float expected
REL_TOL = 1e-12
ABS_TOL = 1e-15

_TEST_DIR = os.path.dirname(os.path.abspath(__file__))
MATHDATA_DIR = os.path.join(_TEST_DIR, 'mathdata')
CMATH_TESTCASES = os.path.join(MATHDATA_DIR, 'cmath_testcases.txt')

# Functions in cmath that cmath10 implements (no rect, polar, or two-arg log)
CMATH10_FUNCTIONS = frozenset({
    'acos', 'acosh', 'asin', 'asinh', 'atan', 'atanh',
    'cos', 'cosh', 'exp', 'log', 'log10', 'sin', 'sinh',
    'sqrt', 'tan', 'tanh',
})
SKIP_FLAGS = {'divide-by-zero', 'overflow', 'invalid'}


def parse_testfile(fname):
    """Parse cmath-style test file.
    Yields (id, fn, arg_real, arg_imag, exp_real, exp_imag, flags).
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


def make_z(real, imag):
    """Build CMath10 from float real, imag."""
    return CMath10(real, imag)


def scalar_close(a_float, b_scalar, rel_tol=REL_TOL, abs_tol=ABS_TOL):
    """True if float a_float is close to Math10/Decimal b_scalar."""
    if builtin_math.isnan(a_float):
        return getattr(b_scalar, 'is_nan', lambda: False)()
    if builtin_math.isinf(a_float):
        if not getattr(b_scalar, 'is_infinite', lambda: False)():
            return False
        return (a_float > 0) == (b_scalar > 0)
    try:
        # from math10 import Math10
        exp = Math10(str(a_float))
        return exp.isclose(b_scalar, rel_tol=rel_tol, abs_tol=abs_tol)
    except (ZeroDivisionError, TypeError, ValueError):
        return False


#  pylint: disable=R0913, R0917
def result_check_complex(\
        exp_real, exp_imag, got_z, rel_tol=REL_TOL, abs_tol=ABS_TOL,\
        ignore_real_sign=False, ignore_imag_sign=False):
    """
    Compare expected (exp_real, exp_imag) to got_z (CMath10).
    Return None if ok, else error str.
    """
    gr = got_z.real
    gi = got_z.imag
    if ignore_real_sign:
        exp_real = abs(exp_real)
        gr = abs(gr)
    if ignore_imag_sign:
        exp_imag = abs(exp_imag)
        gi = abs(gi)
    if not scalar_close(exp_real, gr, rel_tol=rel_tol, abs_tol=abs_tol):
        return f"real: expected {exp_real!r}, got {gr!r}"
    if not scalar_close(exp_imag, gi, rel_tol=rel_tol, abs_tol=abs_tol):
        return f"imag: expected {exp_imag!r}, got {gi!r}"
    return None


class CMath10Tests(unittest.TestCase):
    """Tests mirroring CPython CMathTests for cmath10."""

    def test_constants(self):
        """pi and e as complex (real, 0)."""
        pi_z = c.pi()
        e_z = c.e()
        self.assertTrue(scalar_close(builtin_math.pi, pi_z.real))
        self.assertTrue(scalar_close(0.0, pi_z.imag))
        self.assertTrue(scalar_close(builtin_math.e, e_z.real))
        self.assertTrue(scalar_close(0.0, e_z.imag))

    def test_cmath_matches_math(self):
        """Check cmath10 matches math on the real line (real input -> real output)."""
        test_values = [0.01, 0.1, 0.2, 0.5, 0.9, 0.99]
        unit_interval = test_values + [-x for x in test_values] + [0.0, 1.0, -1.0]
        positive = test_values + [1.0] + [1.0 / x for x in test_values]
        nonnegative = [0.0] + positive
        real_line = [0.0] + positive + [-x for x in positive]

        test_functions = {
            'acos': unit_interval,
            'asin': unit_interval,
            'atan': real_line,
            'cos': real_line,
            'cosh': real_line,
            'exp': real_line,
            'log': positive,
            'log10': positive,
            'sin': real_line,
            'sinh': real_line,
            'sqrt': nonnegative,
            'tan': real_line,
            'tanh': real_line,
        }
        for fn_name, values in test_functions.items():
            if fn_name not in CMATH10_FUNCTIONS:
                continue
            func = getattr(c, fn_name, None)
            if func is None:
                continue
            float_fn = getattr(builtin_math, fn_name, None)
            if float_fn is None:
                continue
            for v in values:
                z = make_z(v, 0)
                try:
                    result = func(z)
                except (ValueError, ZeroDivisionError):
                    continue
                self.assertTrue(
                    scalar_close(float_fn(v), result.real),
                    f"{fn_name}({v}): real part"
                )
                self.assertTrue(
                    scalar_close(0.0, result.imag),
                    f"{fn_name}({v}): imag part should be 0"
                )

    @unittest.skipUnless(os.path.isfile(CMATH_TESTCASES),\
            "mathdata/cmath_testcases.txt not found")
    # pylint: disable=R0913, R0917
    def test_specific_values(self):
        # pylint: disable=R0914
        """Run cases from cmath_testcases.txt for cmath10 functions."""
        run = 0
        for (id_, fn, ar, ai, er, ei, flags) in\
                parse_testfile(CMATH_TESTCASES):
            if fn not in CMATH10_FUNCTIONS:
                continue
            if any(f in flags for f in SKIP_FLAGS):
                continue
            if builtin_math.isnan(er) or builtin_math.isnan(ei):
                continue
            if builtin_math.isinf(er) or builtin_math.isinf(ei):
                continue
            run += 1
            z = make_z(ar, ai)
            try:
                func = getattr(c, fn)
                got = func(z)
            except (ValueError, ZeroDivisionError) as e:
                self.fail(f"{id_} {fn}({ar},{ai}): raised {e!r}")
            ignore_real = 'ignore-real-sign' in flags
            ignore_imag = 'ignore-imag-sign' in flags
            err = result_check_complex(er, ei, got,
                                       ignore_real_sign=ignore_real,
                                       ignore_imag_sign=ignore_imag)
            if err is not None:
                self.fail(f"{id_} {fn}(complex({ar!r},{ai!r})): {err}")
        self.assertGreater(run, 0, "no test cases ran (check mathdata/cmath_testcases.txt)")

    def test_phase(self):
        """phase(z) = arg z (real result)."""
        self.assertAlmostEqual(float(c.phase(make_z(1, 0)).real), 0.0)
        self.assertAlmostEqual(float(c.phase(make_z(-1, 0)).real), builtin_math.pi)
        self.assertAlmostEqual(float(c.phase(make_z(0, 1)).real), builtin_math.pi / 2)
        self.assertAlmostEqual(float(c.phase(make_z(0, -1)).real), -builtin_math.pi / 2)

    def test_abs(self):
        """abs(z) = magnitude (real result, imag 0)."""
        self.assertAlmostEqual(float(c.abs(make_z(0, 0)).real), 0.0)
        self.assertAlmostEqual(float(c.abs(make_z(3, 4)).real), 5.0)
        self.assertAlmostEqual(float(c.abs(make_z(1, 0)).real), 1.0)


if __name__ == '__main__':
    unittest.main()
