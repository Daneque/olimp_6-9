import sys
import os
from pathlib import Path
import random


def max_area(heights):
    left = 0
    right = len(heights) - 1
    best = 0

    while left < right:
        h_left = heights[left]
        h_right = heights[right]

        width = right - left
        current = (h_left if h_left < h_right else h_right) * width
        if current > best:
            best = current

        if h_left < h_right:
            left += 1
        else:
            right -= 1

    return best


def predefined_tests():
    return [
        (2, [1, 1]),                          # минимальный N
        (9, [1, 8, 6, 2, 5, 4, 8, 3, 7]),     # классический пример: ответ 49
        (5, [1, 2, 3, 4, 5]),                 # возрастающая
        (5, [5, 4, 3, 2, 1]),                 # убывающая
        (3, [5, 1, 5]),                       # две крайние
        (2, [10**9, 10**9]),                  # максимум по значениям
        (6, [1000, 1000, 1, 1, 1, 1]),        # максимум между первыми двумя
        (6, [1, 1000, 1, 1000, 1, 1000]),     # зигзаг
    ]


def random_test():
    # иногда маленький N, иногда крупный
    if random.random() < 0.4:
        n = random.randint(2, 20)
    else:
        n = random.randint(2, 200000)
    heights = [random.randint(1, 10**9) for _ in range(n)]
    return n, heights


def generate_tests(count, out_path):
    tests = []

    for n, h in predefined_tests():
        tests.append((n, h))

    while len(tests) < count:
        tests.append(random_test())

    for i, (n, heights) in enumerate(tests[:count], start=1):
        ans = max_area(heights)

        in_lines = [
            str(n),
            " ".join(map(str, heights)),
        ]
        inp = "\n".join(in_lines)
        out = str(ans)

        with open(out_path / f"{i}.in", "w", encoding="utf-8") as f:
            f.write(inp + "\n")
        with open(out_path / f"{i}.out", "w", encoding="utf-8") as f:
            f.write(out + "\n")


if __name__ == "__main__":
    num_tests = int(sys.argv[1])
    out_path = Path(sys.argv[2])

    if not out_path.exists():
        os.mkdir(out_path)

    generate_tests(num_tests, out_path)