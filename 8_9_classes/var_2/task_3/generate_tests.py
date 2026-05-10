import random
import sys
import os
from pathlib import Path


def max_len_subarray_leq_s(a, S):
    n = len(a)
    best = 0
    cur_sum = 0
    left = 0
    for right in range(n):
        cur_sum += a[right]
        while cur_sum > S and left <= right:
            cur_sum -= a[left]
            left += 1
        length = right - left + 1
        if length > best:
            best = length
    return best


def predefined_tests():
    return [
        # пример из таблицы
        (5, 7, [2, 1, 5, 1, 3]),
        # один элемент
        (1, 5, [3]),
        (1, 5, [10]),
        # все влезают
        (4, 100, [10, 20, 30, 40]),
        # никто не влезает, кроме, возможно, нуля элементов
        (3, 1, [5, 5, 5]),
        # граница по сумме
        (4, 6, [1, 2, 3, 4]),
    ]


def random_test():
    # иногда маленькие N, иногда побольше
    r = random.random()
    if r < 0.4:
        n = random.randint(1, 20)
    else:
        n = random.randint(1, 200000 // 10)  # для генерации, не максимум
    a = [random.randint(1, 10**4) for _ in range(n)]
    # S берём случайно вокруг суммы
    total = sum(a)
    if random.random() < 0.5:
        S = random.randint(1, max(1, total // 2))
    else:
        S = random.randint(1, max(1, total))
    return (n, S, a)


def generate_tests(count=10, out_path=Path("./tests")):
    tests = []

    for n, S, a in predefined_tests():
        tests.append((n, S, a))

    while len(tests) < count:
        tests.append(random_test())

    for i, (n, S, a) in enumerate(tests[:count], start=1):
        ans = max_len_subarray_leq_s(a, S)

        in_lines = []
        in_lines.append(f"{n} {S}")
        in_lines.append(" ".join(map(str, a)))
        inp = "\n".join(in_lines)

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