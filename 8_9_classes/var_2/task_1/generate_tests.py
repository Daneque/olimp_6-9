import random
import sys
import os
from pathlib import Path


def xor_1_to_n(n: int) -> int:
    r = n % 4
    if r == 0:
        return n
    if r == 1:
        return 1
    if r == 2:
        return n + 1
    return 0  # r == 3


def predefined_tests():
    return [
        1,
        2,
        3,
        4,
        5,
        10,
        16,
        10**6,
        10**18 - 1,
        10**18,
    ]


def random_test():
    # равномерно по логарифмической шкале
    # иногда маленькие, иногда очень большие
    if random.random() < 0.3:
        n = random.randint(1, 1000)
    else:
        n = random.randint(1, 10**18)
    return n


def generate_tests(count=10, out_path=Path("./tests")):
    tests = predefined_tests()

    while len(tests) < count:
        tests.append(random_test())

    for i, n in enumerate(tests[:count], start=1):
        ans = xor_1_to_n(n)

        inp = str(n)
        out = str(ans)

        with open(out_path / f"{i}.in", "w", encoding="utf-8") as f:
            f.write(inp)
        with open(out_path / f"{i}.out", "w", encoding="utf-8") as f:
            f.write(out)


if __name__ == "__main__":
    num_tests = int(sys.argv[1])
    out_path = Path(sys.argv[2])

    if not out_path.exists():
        os.mkdir(out_path)

    generate_tests(num_tests, out_path)