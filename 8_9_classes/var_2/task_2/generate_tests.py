import random
import sys
import os
from pathlib import Path


def count_divisors_in_range(n: int, L: int, R: int) -> int:
    cnt = 0
    d = 1
    while d * d <= n:
        if n % d == 0:
            q = n // d
            if L <= d <= R:
                cnt += 1
            if q != d and L <= q <= R:
                cnt += 1
        d += 1
    return cnt


def predefined_tests():
    return [
        (12, 2, 8),            # из примера: 4
        (1, 1, 1),             # 1 делитель
        (10, 1, 10),           # все делители
        (10, 2, 2),            # ровно один делитель
        (10, 3, 9),            # только 5
        (36, 1, 6),            # много делителей в начале
        (999983, 1, 999983),   # простое число
        (10**12, 1, 10**12),   # максимальное N, полный диапазон
    ]


def random_test():
    # иногда небольшие N, иногда крупные
    if random.random() < 0.5:
        n = random.randint(1, 10**6)
    else:
        n = random.randint(1, 10**12)
    L = random.randint(1, n)
    R = random.randint(L, n)
    return (n, L, R)


def generate_tests(count=10, out_path=Path("./tests")):
    tests = predefined_tests()

    while len(tests) < count:
        tests.append(random_test())

    for i, (n, L, R) in enumerate(tests[:count], start=1):
        ans = count_divisors_in_range(n, L, R)

        inp = f"{n} {L} {R}"
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