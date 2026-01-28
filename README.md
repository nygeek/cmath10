# Complex Decimal Math

This repository represents the development environment for the
cmath10.py module.  This module is an adjunct to the decimal.py
module.  It also contains the math10.py module.

The decimal.py module provides basic arithmetic machinery for
arbitrary-length numbers with underlying representation in
decimal.  This representation, wasteful in many contexts, is
useful in accounting situations and in some other circumstances.

For reference, check the decimal.py documentation at
https://docs.python.org/3/library/decimal.html

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

Beyond the HP35, I encountered George Stibitz late in his career.
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

Moved smoke test from cmath10.py main() to a separate file, csmoke.py
(complex) and the smoke test for math10.py to ssmoke.py (scalar)

## NEWS

Using print(dir(<module>)) I retrieved the list of methods in each
of the modules involved in this project - *math* and *cmath*, which
I am trying to shadow functionally, *decimal*, which is the  underlying
arithmetic engine and *Math10* and *CMath10* which are contain the
machinery I have built.

## Install

This module should be installed to support CNC10, the decimal complex
number calculator.  Since none of this stuff is a public Python
library you will need to install it locally on your system:

```> git clone https://github.com/nygeek/cmath10.git```

And then use pip to install it for the calculator:

```> pip install -e ~/projects/c/cmath10```

## Copying, License

## Bugs

## Contributing

## FAQ

## TODO

1. [2025-12-21] polar
1. [2025-12-21] rect

1. [2025-12-21] acosh
1. [2025-12-21] asinh
1. [2025-12-21] atanh

1. [2025-12-21] cosh
1. [2025-12-21] sinh
1. [2025-12-21] tanh

1. [2025-12-24] Set up precision and clamping to emulate HP-35 behavior

1. [2025-12-24] Complex acos
1. [2025-12-24] Complex asin
1. [2025-12-24] Complex atan, atan2
1. [2025-12-21] Complex pi
1. [2025-12-21] Complex

On 2026-01-25 I gathered the lists of methods from decimal, math,
and CMath10 and used those to figure out the items needed to roughly
complete the signatures for Math10 (the scalar part) and CMath10
(the complex part).

### Math10

#### Arithmetic
```__add__, __sub__, __mul__, __truediv__, __pow__, __radd__, __rsub__, __rmul__, __rtruediv__, __rpow__, __neg__, __pos__, __abs__```

##### Comparisons
```__eq__, __ne__, __lt__, __le__, __gt__, __ge__```

##### Conversions
```__float__, __int__, __str__, __repr__```

##### Optional but useful
```__hash__```

### CMath10
```__complex__```
