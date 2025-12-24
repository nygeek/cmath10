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

## Author

Written by Marc Donner (marc@nygeek.net)

## Thanks

I first started thinking about building a complex calculator based
on the HP35 calculator when I graduated from college.  Recently I
decided to implement it.

Beyond the HP-35, I encountered George Stibitz late in his career.
He had built a complex number calculator at Bell Labs, an accomplishment
that was particularly remarkable given that the whole thing was
implemented in electromechanical relays.

Finally, special thanks go to Mike Cowlishaw whose work on arbitrary
resolution decimal arithmetic underpins the decimal.py module and
enables this machinery to ultimately emulate the HP35 more
realistically.

There are two particular tests that I want this machinery to support:

1 - Euler's Identity (e^pi*i + 1 = 0)

2 - The HP35 game - minimum number of keys to display the number
200 on the display without pressing any digit keys and starting
from a cleared stack.  The best I know is six - ARC COS TAN LOG
ENTER +.

## CHANGELOG

Moved smoke test from cmath10.py main() to a separate file,
smoke.py

## NEWS

## Install

## Copying, License

## Bugs

## Contributing

## FAQ

## TODO

1. [2025-12-21] phase
    * 2025-12-22
1. [2025-12-21] polar
1. [2025-12-21] rect
1. [2025-12-21] exp
    * Scalar from decimal.py
    * Complex 2025-12-22
1. [2025-12-21] log
    * Scalar from decimal.py
    * Complex 2025-12-24
1. [2025-12-21] sqrt
    * Scalar from decimal.py
    * Complex 2025-12-24
1. [2025-12-21] acos
    * Scalar 2025-12-22
1. [2025-12-21] asin
    * Scalar 2025-12-22
1. [2025-12-21] atan, atan2
    * Scalar 2025-12-22
1. [2025-12-21] cos
    * Scalar 2025-12-22
1. [2025-12-21] sin
    * Scalar 2025-12-22
1. [2025-12-21] tan
    * Scalar 2025-12-22
1. [2025-12-21] acosh
1. [2025-12-21] asinh
1. [2025-12-21] atanh
1. [2025-12-21] cosh
1. [2025-12-21] sinh
1. [2025-12-21] tanh
1. [2025-12-21] pi
    * Scalar 2025-12-22
1. [2025-12-21] e
    * Scalar 2025-12-22
1. [2025-12-21] add
    * Scalar from decimal.py
    * Complex 2025-12-21
1. [2025-12-21] sub
    * Scalar from decimal.py
    * Complex 2025-12-21
1. [2025-12-21] mul
    * Scalar from decimal.py
    * Complex 2025-12-21
1. [2025-12-21] div
    * Scalar from decimal.py
    * Complex 2025-12-21
1. [2025-12-24] Set up precision and clamping to emulate HP-35 behavior
