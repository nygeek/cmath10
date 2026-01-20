""" Smoke test for Math10 class

Started 2025-12-24

Copyright (C) 2025 NYGeek LLC

"""

# ----- Python libraries ----- #
from decimal import Decimal

# ----- Local libraries ----- #
from trace_debug import DebugTrace
from math10 import Math10

def main():
    """ simple smoke test """
    DebugTrace(False)
    # DebugTrace(True)
    pi = Math10.pi()
    print(f"pi: {pi}")

    pionfour = pi / Decimal('4')
    print(f"\npi/4: {pionfour}\n")

    x = Math10.sin(pionfour)
    print(f"sin(pi/4): {x}")

    x = Math10.cos(pionfour)
    print(f"\ncos(pi/4): {x}")

    x = Math10.tan(pionfour)
    print(f"\ntan(pi/4): {x}")

    pionfive = pi / 5
    print(f"\npi/5: {pionfive}\n")

    z = Math10.sin(pionfive)
    print(f"sin(pi/5): {z}")
    print(f"asin(sin(pi/5)): {Math10(z).asin()}\n")

    z = Math10.cos(pionfive)
    print(f"cos(pi/5): {z}")
    print(f"acos(cos(pi/5)): {Math10(z).acos()}\n")

    z = Math10.tan(pionfive)
    print(f"tan(pi/5): {z}")
    print(f"atan(tan(pi/5)): {Math10(z).atan()}\n")


if __name__ == '__main__':
    main()
