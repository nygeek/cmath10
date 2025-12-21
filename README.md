# Complex Decimal Math

This repository represents the development environment for the
cmath10.py module.  This module is an adjunct to the decimal.py
module.

The decimal.py module provides basic arithmetic machinery for
arbitrary-length numbers with underlying representation in
decimal.  This representation, wasteful in many contexts, is
useful in accounting situations and in some other circumstances.

For reference, check the decimal.py documentation at https://docs.python.org/3/library/decimal.html

## Complex decimal

Each complex decimal number is a two component item.  One item is
the ```.real``` part and the other is the ```.imag``` part.

If we refer to the complex number z as a+bj, where j is the imaginary
unit (also identified as the principal square root of -1), then the
string representation of this number is (a+bj).

Notice that we are seeking to make cmath10 behave as much like cmath
as possible.


