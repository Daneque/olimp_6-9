import random
import sys
import os
from pathlib import Path
from math import gcd

def solve_instance(n, k1, k2):
    g = gcd(k1, k2)
    lcm = k1 // g * k2
    return n // k1 + n // k2 - n // lcm

def predefined_tests():
    return [
        (10, 2, 3),
        (1, 2, 3),
        (100, 10, 10),
        (100, 1, 999999937),
        (10**18, 999999937, 1000000007),
        (999999999999999999, 2, 4),
        (123456789, 17, 19),
        (10**18, 1, 1),
    ]

def random_test():
    n = random.randint(1, 10**18)
    k1 = random.randint(1, 10**9)
    k2 = random.randint(1, 10**9)
    return (n, k1, k2)

def generate_tests(count=10, out_path=Path("./tests")):
    tests = predefined_tests()

    while len(tests) < count:
        tests.append(random_test())

    for i, (n, k1, k2) in enumerate(tests[:count], start=1):
        ans = solve_instance(n, k1, k2)

        inp = f"{n} {k1} {k2}"
        out = str(ans)

        with open(out_path / f"{i}.in", "w", encoding="utf-8") as f:
            f.write(inp)
        with open(out_path / f"{i}.out", "w", encoding="utf-8") as f:
            f.write(out)

if __name__ == "__main__":
    out_path = Path(sys.argv[2])
    num_tests = int(sys.argv[1])

    if not out_path.exists():
        os.mkdir(out_path)

    generate_tests(num_tests, out_path)
