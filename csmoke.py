""" Smoke test for CMath10 class

Started 2025-12-24

Copyright (C) 2025 NYGeek LLC

"""

# ----- Python libraries ----- #
# import json

# ----- Local libraries ----- #
from trace_debug import DebugTrace
from cmath10 import CMath10
from math10 import Math10


def main():
    """ simple smoke test """
    DebugTrace(False)

    z = CMath10("1", "2")
    print(f"Z: {z}\n")

    a = CMath10("1", "3")
    b = CMath10("2.1", "7.9")
    print(f"a: {a}")
    print(f"b: {b}\n")

    a.add(b)
    print(f"a + b: {a}")
    a = CMath10("1", "3")
    a.sub(b)
    print(f"a - b: {a}")
    a = CMath10("1", "3")
    a.mul(b)
    print(f"a * b: {a}\n")

    a = CMath10("1", "1")
    b = CMath10("1", "-1")
    print(f"a: {a}")
    print(f"b: {b}")
    a.div(b)
    print(f"a / b: {a}\n")

    z = CMath10(0,Math10.pi())
    z = z.exp()
    print(f"e^(pi*i): {z}\n")

    z = CMath10("1", "1")
    print(f"phase(z: {z}): {z.phase()}")
    z = CMath10("1", "-1")
    print(f"phase(z: {z}): {z.phase()}\n")

    z = CMath10("3", "4")
    r = z.scalar_abs()
    print(f"scalar_abs(z: {z}): {r}\n")

    z = CMath10("3", "4")
    z2 = z.log()
    print(f"log(z: {z}): {z2}")
    print(f"e^(log(z)): {z2.exp()}\n")

    z = CMath10("2", "2")
    print("(expect (1.5537739740300374+0.6435942529055826j))")
    print(f"sqrt(z: {z}): {z.sqrt()}\n")

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
    main()
