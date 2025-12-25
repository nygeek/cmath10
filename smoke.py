""" Smoke test for CMath10 class

Started 2025-12-24

Copyright (C) 2025 NYGeek LLC

"""

# ----- Python libraries ----- #
import json
from decimal import Decimal, getcontext, InvalidOperation

# ----- Local libraries ----- #
from trace_debug import DebugTrace
from cmath10 import CMath10
from cmath10 import scalar_pi, scalar_sin, scalar_cos, scalar_tan
from cmath10 import scalar_asin, scalar_acos, scalar_atan


def main():
    """ simple smoke test """
    DebugTrace(False)
    z = CMath10("1", "2")
    print(f"Z: {z}")
    a = CMath10("1", "3")
    b = CMath10("2.1", "7.9")
    print(f"a: {a}")
    print(f"b: {b}")
    a.add(b)
    print(f"a + b: {a}")
    a = CMath10("1", "3")
    a.sub(b)
    print(f"a - b: {a}")
    a = CMath10("1", "3")
    a.mul(b)
    print(f"a * b: {a}")
    a = CMath10("1", "1")
    b = CMath10("1", "-1")
    print(f"a: {a}")
    print(f"b: {b}")
    a.div(b)
    print(f"a / b: {a}")
    print(a)
    pi = scalar_pi()
    print(f"pi: {pi}")
    x = scalar_sin(pi/4)
    print(f"pi/4: {pi/4}")
    print(f"sin(pi/4): {x}")
    x = scalar_cos(pi/4)
    print(f"cos(pi/4): {x}")
    x = scalar_tan(pi/4)
    print(f"tan(pi/4): {x}")
    x = scalar_sin(pi/5)
    print(f"asin(sin(pi/5)): {scalar_asin(x)}")
    x = scalar_cos(pi/5)
    print(f"acos(cos(pi/5)): {scalar_acos(x)}")
    x = scalar_tan(pi/5)
    print(f"pi/5: {x}")
    print(f"tan(pi/5): {scalar_tan(x)}")
    print(f"atan(tan(pi/5)): {scalar_atan(scalar_tan(x))}")
    z = CMath10(0,scalar_pi())
    z = z.exp()
    print(f"e^(pi*i): {z}")
    z = CMath10("1", "1")
    print(f"phase(z: {z}): {z.phase()}")
    z = CMath10("1", "-1")
    print(f"phase(z: {z}): {z.phase()}")
    z = CMath10("3", "4")
    r = z.scalar_abs()
    print(f"scalar_abs(z: {z}): {r}")
    z = CMath10("3", "4")
    z2 = z.log()
    print(f"log(z: {z}): {z2}")
    print(f"e^(log(z)): {z2.exp()}")
    z = CMath10("2", "2")
    z2 = z.sqrt()
    print(f"sqrt(z: {z}): {z2}")
    z = CMath10("4", "0")
    z2 = z.sqrt()
    print(f"sqrt(z: {z}): {z2}")
    z = CMath10("-4", "0")
    z2 = z.sqrt()
    print(f"sqrt(z: {z}): {z2}")
    z = CMath10("0", "1")
    z2 = z.sqrt()
    print(f"sqrt(z: {z}): {z2}")
    z = CMath10("1", "1")
    z2 = z.sin()
    print(f"sin(z: {z}): {z2}")
    z = CMath10("1", "1")
    z2 = z.cos()
    print(f"cos(z: {z}): {z2}")
    z = CMath10("1", "1")
    z2 = z.tan()
    print(f"tan(z: {z}): {z2}")
    e = z.e()
    print(f"e(): {e}")
    pi = z.pi()
    print(f"pi(): {pi}")


if __name__ == '__main__':
    main()
