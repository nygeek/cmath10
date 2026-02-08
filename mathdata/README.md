# Test data for math10 and cmath10

The test suites reuse the **test case format** from CPython's
math/cmath tests.

## Optional: full CPython test data

For full coverage (especially for **cmath10** complex-valued tests),
copy the official cmath test data file here:

- **Source:** [CPython
`Lib/test/mathdata/cmath_testcases.txt`](https://raw.githubusercontent.com/python/cpython/main/Lib/test/mathdata/cmath_testcases.txt)

- **Local name:** `cmath_testcases.txt` in this directory

- **test_math10.py** uses only real-axis cases (real input, real
expected) from this file.

- **test_cmath10.py** uses all cases (complex input, complex expected)
for the functions it implements.

A small built-in subset is included in `cmath_testcases.txt` so
tests run without copying the full file.
