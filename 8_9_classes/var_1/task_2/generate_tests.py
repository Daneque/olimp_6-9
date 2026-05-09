import random
import sys
import os
from pathlib import Path
from math import gcd  # для генерации эталона допустимо

def solve_instance(p, q, b, l, r):
    if l > r:
        l, r = r, l

    y_l = (p * l + b * q) // q
    y_r = (p * r + b * q) // q

    dx = abs(r - l)
    dy = abs(y_r - y_l)

    return gcd(dx, dy) + 1

def coprime_pair(limit_q=10**5, limit_p=10**5):
    while True:
        q = random.randint(1, limit_q)
        p = random.randint(-limit_p, limit_p)
        if gcd(abs(p), q) == 1:
            return p, q

def predefined_tests():
    return [
        (1, 1, 0, 0, 10),
        (2, 1, 3, -5, 5),
        (1, 2, 0, 0, 10),
        (-3, 2, 7, 4, 10),
        (0, 1, 5, -100, 100),
        (7, 3, -2, 6, 6),
        (5, 4, 1, 8, 20),
    ]

def random_test():
    p, q = coprime_pair()
    b = random.randint(-10**9, 10**9)

    base = random.randint(-10**6, 10**6)
    step = random.randint(0, 10**6)

    l = base * q
    r = (base + step) * q

    return (p, q, b, l, r)

def generate_tests(count=10, out_path=Path("./tests")):
    tests = predefined_tests()

    while len(tests) < count:
        tests.append(random_test())

    for i, test in enumerate(tests[:count], start=1):
        p, q, b, l, r = test
        ans = solve_instance(p, q, b, l, r)

        inp = f"{p} {q} {b} {l} {r}"
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
