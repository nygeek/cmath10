# Test data for math10

The test suite for math10 reuses the **test case format** from CPython's math/cmath tests.

## Optional: full CPython test data

For full coverage, copy the official cmath test data file here:

- **Source:** [CPython `Lib/test/mathdata/cmath_testcases.txt`](https://raw.githubusercontent.com/python/cpython/main/Lib/test/mathdata/cmath_testcases.txt)
- **Local name:** `cmath_testcases.txt` in this directory

If `cmath_testcases.txt` is present, `test_math10.py` will run all real-axis cases (real input, real expected) for the functions implemented by math10 (cos, sin, tan, acos, asin, atan, cosh, sinh, tanh, acosh, asinh, atanh).

A small built-in subset is also included in `cmath_testcases.txt` so tests run without copying the full file.
