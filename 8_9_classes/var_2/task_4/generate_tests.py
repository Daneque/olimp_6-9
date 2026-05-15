#generate_tests.py

import sys
import os
from pathlib import Path
import random

def solve_instance_fast(n, arr):
    if n < 3:
        return 0

    left_max = [0] * n
    right_max = [0] * n

    left_max[0] = arr[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], arr[i])

    right_max[n - 1] = arr[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], arr[i])

    max_single_pool = 0
    current_pool = 0
    
    for i in range(1, n - 1):
        bound = min(left_max[i], right_max[i])
        if bound > arr[i]:
            current_pool += bound - arr[i]
        else:
            if current_pool > max_single_pool:
                max_single_pool = current_pool
            current_pool = 0
            
    if current_pool > max_single_pool:
        max_single_pool = current_pool
        
    return max_single_pool


def predefined_tests():
    tests = []

    # 1) Пример из условия
    tests.append((4, [3, 1, 2, 4]))

    # 2) Нет ям вообще (возрастание)
    tests.append((5, [1, 2, 3, 4, 5]))

    # 3) Нет ям (убывание)
    tests.append((4, [5, 4, 3, 2]))

    # 4) Одна огромная яма
    tests.append((6, [10, 1, 1, 1, 1, 10]))

    # 5) Несколько разных ям, нужно выбрать максимальную
    tests.append((9, [5, 2, 4, 1, 6, 1, 3, 8, 2]))

    # 6) Яма с неровным дном
    tests.append((7, [7, 2, 4, 1, 5, 2, 6]))

    return tests

def random_test():
    r = random.random()
    if r < 0.3:
        n = random.randint(3, 20)
        max_h = 100
    elif r < 0.7:
        n = random.randint(20, 5000)
        max_h = 100000
    else:
        n = random.randint(50000, 200000)
        max_h = 10**9

    arr = []
    if random.random() < 0.5:
        arr = [random.randint(1, max_h) for _ in range(n)]
    else:
        arr = [random.randint(1, max_h // 10) for _ in range(n)]
        
        max_peaks = min(20, n // 2)
        if max_peaks >= 2:
            peaks = random.randint(2, max_peaks)
            for _ in range(peaks):
                idx = random.randint(0, n - 1)
                arr[idx] = random.randint(max_h // 2, max_h)

    return n, arr

def generate_tests(count, out_path):
    tests = predefined_tests()

    while len(tests) < count:
        tests.append(random_test())

    for i, (n, arr) in enumerate(tests[:count], start=1):
        ans = solve_instance_fast(n, arr)

        inp = f"{n}\n" + " ".join(map(str, arr))
        out = str(ans)

        with open(out_path / f"{i}.in", "w", encoding="utf-8") as f:
            f.write(inp + "\n")
        with open(out_path / f"{i}.out", "w", encoding="utf-8") as f:
            f.write(out + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_tests.py <num_tests> <output_dir>")
        sys.exit(1)
        
    num_tests = int(sys.argv[1])
    out_path = Path(sys.argv[2])

    if not out_path.exists():
        os.makedirs(out_path)

    generate_tests(num_tests, out_path)