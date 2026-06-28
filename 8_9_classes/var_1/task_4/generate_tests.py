#!/usr/bin/env python3
import sys
from pathlib import Path
import random
import heapq


def solve_instance(a):
    if len(a) <= 1:
        return 0
    heap = a[:]
    heapq.heapify(heap)
    total = 0
    while len(heap) > 1:
        x = heapq.heappop(heap)
        y = heapq.heappop(heap)
        s = x + y
        total += s
        heapq.heappush(heap, s)
    return total



def predefined_tests():
    return [
        [7],
        [1, 2],
        [4, 3, 2, 6],
        [1, 1, 1, 1, 1],
        [10**9, 10**9],
    ]



def random_array(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]



def equal_array(n, value):
    return [value] * n



def increasing_array(n, lo, step):
    return [lo + i * step for i in range(n)]



def clustered_array(n, small_lo, small_hi, big_lo, big_hi, big_count):
    arr = [random.randint(small_lo, small_hi) for _ in range(n - big_count)]
    arr += [random.randint(big_lo, big_hi) for _ in range(big_count)]
    random.shuffle(arr)
    return arr



def easy_test(idx):
    kind = idx % 5
    if kind == 0:
        n = random.randint(1, 20)
        return random_array(n, 1, 50)
    if kind == 1:
        n = random.randint(2, 30)
        return equal_array(n, random.randint(1, 20))
    if kind == 2:
        n = random.randint(2, 25)
        return increasing_array(n, random.randint(1, 10), random.randint(1, 5))
    if kind == 3:
        n = random.randint(2, 30)
        return clustered_array(n, 1, 20, 100, 300, random.randint(1, max(1, n // 4)))
    n = random.randint(2, 30)
    return [1] * (n - 1) + [random.randint(20, 100)]



def medium_test(idx):
    kind = idx % 6
    if kind == 0:
        n = random.randint(200, 2000)
        return random_array(n, 1, 10**4)
    if kind == 1:
        n = random.randint(300, 2500)
        return equal_array(n, random.randint(1, 10**3))
    if kind == 2:
        n = random.randint(200, 2000)
        return increasing_array(n, random.randint(1, 50), random.randint(1, 20))
    if kind == 3:
        n = random.randint(300, 2500)
        return clustered_array(n, 1, 100, 10**5, 10**6, random.randint(1, max(1, n // 10)))
    if kind == 4:
        n = random.randint(300, 2000)
        arr = random_array(n - 2, 1, 1000)
        arr += [10**6, 10**6]
        random.shuffle(arr)
        return arr
    n = random.randint(200, 2500)
    return [1] * (n // 2) + random_array(n - n // 2, 2, 5000)



def hard_test(idx):
    kind = idx % 7
    if kind == 0:
        n = random.randint(50000, 120000)
        return random_array(n, 1, 10**9)
    if kind == 1:
        n = random.randint(60000, 150000)
        return equal_array(n, random.randint(1, 10**6))
    if kind == 2:
        n = random.randint(50000, 100000)
        return increasing_array(n, random.randint(1, 1000), random.randint(1, 50))
    if kind == 3:
        n = random.randint(70000, 150000)
        return clustered_array(n, 1, 1000, 10**8, 10**9, random.randint(1, max(1, n // 20)))
    if kind == 4:
        n = random.randint(80000, 200000)
        arr = [1] * (n - 5) + [10**9] * 5
        random.shuffle(arr)
        return arr
    if kind == 5:
        n = random.randint(100000, 200000)
        return random_array(n, 1, 10**5)
    n = random.randint(90000, 180000)
    half = n // 2
    arr = random_array(half, 1, 100)
    arr += random_array(n - half, 10**8, 10**9)
    random.shuffle(arr)
    return arr



def write_test(test_id, arr, out_path):
    ans = solve_instance(arr)

    with open(out_path / f"{test_id}.in", "w", encoding="utf-8") as fin:
        fin.write(str(len(arr)) + "\n")
        fin.write(" ".join(map(str, arr)) + "\n")

    with open(out_path / f"{test_id}.out", "w", encoding="utf-8") as fout:
        fout.write(str(ans))



def generate_tests(easy_count, medium_count, hard_count, out_path):
    out_path.mkdir(parents=True, exist_ok=True)

    test_id = 1

    base = predefined_tests()
    for arr in base[:easy_count]:
        write_test(test_id, arr, out_path)
        test_id += 1

    generated_easy = max(0, easy_count - min(easy_count, len(base)))
    for i in range(generated_easy):
        write_test(test_id, easy_test(i), out_path)
        test_id += 1

    for i in range(medium_count):
        write_test(test_id, medium_test(i), out_path)
        test_id += 1

    for i in range(hard_count):
        write_test(test_id, hard_test(i), out_path)
        test_id += 1



def main():
    if len(sys.argv) != 5:
        print("Использование: python generate_chain_tests_levels.py <easy_count> <medium_count> <hard_count> <out_dir>")
        sys.exit(1)

    easy_count = int(sys.argv[1])
    medium_count = int(sys.argv[2])
    hard_count = int(sys.argv[3])
    out_path = Path(sys.argv[4])

    if easy_count < 0 or medium_count < 0 or hard_count < 0:
        print("Количество тестов должно быть неотрицательным")
        sys.exit(1)

    generate_tests(easy_count, medium_count, hard_count, out_path)


if __name__ == "__main__":
    main()