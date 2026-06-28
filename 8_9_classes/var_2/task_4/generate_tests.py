import random
import sys
from pathlib import Path


rnd = random.Random(123456)



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
    return [
        (4, [3, 1, 2, 4]),
        (5, [1, 2, 3, 4, 5]),
        (4, [5, 4, 3, 2]),
        (6, [10, 1, 1, 1, 1, 10]),
        (9, [5, 2, 4, 1, 6, 1, 3, 8, 2]),
        (7, [7, 2, 4, 1, 5, 2, 6]),
    ]



def random_plain(n, lo, hi):
    return [rnd.randint(lo, hi) for _ in range(n)]



def one_big_pit(n, wall, pit_lo, pit_hi):
    arr = [wall] * n
    for i in range(1, n - 1):
        arr[i] = rnd.randint(pit_lo, pit_hi)
    return arr



def many_peaks(n, low_hi, peak_lo, peak_hi):
    arr = [rnd.randint(1, low_hi) for _ in range(n)]
    peaks = max(2, min(20, n // 2))
    for _ in range(rnd.randint(2, peaks)):
        idx = rnd.randint(0, n - 1)
        arr[idx] = rnd.randint(peak_lo, peak_hi)
    return arr



def zigzag(n, low_lo, low_hi, high_lo, high_hi):
    arr = []
    for i in range(n):
        if i % 2 == 0:
            arr.append(rnd.randint(high_lo, high_hi))
        else:
            arr.append(rnd.randint(low_lo, low_hi))
    return arr



def easy_test(idx):
    kind = idx % 5
    if kind == 0:
        n = rnd.randint(3, 15)
        return (n, random_plain(n, 1, 30))
    if kind == 1:
        n = rnd.randint(3, 20)
        wall = rnd.randint(10, 50)
        return (n, one_big_pit(n, wall, 1, wall // 2))
    if kind == 2:
        n = rnd.randint(3, 20)
        return (n, zigzag(n, 1, 10, 10, 30))
    if kind == 3:
        n = rnd.randint(3, 20)
        arr = list(range(1, n + 1))
        return (n, arr)
    n = rnd.randint(3, 20)
    arr = list(range(n, 0, -1))
    return (n, arr)



def medium_test(idx):
    kind = idx % 6
    if kind == 0:
        n = rnd.randint(50, 3000)
        return (n, random_plain(n, 1, 10**4))
    if kind == 1:
        n = rnd.randint(100, 5000)
        wall = rnd.randint(10**3, 10**5)
        return (n, one_big_pit(n, wall, 1, max(1, wall // 10)))
    if kind == 2:
        n = rnd.randint(100, 5000)
        return (n, many_peaks(n, 10**3, 10**4, 10**5))
    if kind == 3:
        n = rnd.randint(50, 4000)
        return (n, zigzag(n, 1, 100, 10**3, 10**4))
    if kind == 4:
        n = rnd.randint(100, 5000)
        arr = [1] * n
        for _ in range(max(2, n // 200)):
            arr[rnd.randint(0, n - 1)] = rnd.randint(10**3, 10**5)
        return (n, arr)
    n = rnd.randint(100, 5000)
    arr = random_plain(n, 1, 500)
    pos = rnd.randint(1, n - 2)
    arr[pos] = 1
    arr[pos - 1] = rnd.randint(10**3, 10**4)
    arr[pos + 1] = rnd.randint(10**3, 10**4)
    return (n, arr)



def hard_test(idx):
    kind = idx % 7
    if kind == 0:
        n = rnd.randint(50000, 120000)
        return (n, random_plain(n, 1, 10**9))
    if kind == 1:
        n = rnd.randint(80000, 200000)
        wall = rnd.randint(10**8, 10**9)
        return (n, one_big_pit(n, wall, 1, max(1, wall // 100)))
    if kind == 2:
        n = rnd.randint(100000, 200000)
        return (n, many_peaks(n, 10**5, 10**8, 10**9))
    if kind == 3:
        n = rnd.randint(100000, 200000)
        return (n, zigzag(n, 1, 10**3, 10**8, 10**9))
    if kind == 4:
        n = rnd.randint(120000, 200000)
        arr = [1] * n
        for _ in range(max(2, n // 5000)):
            arr[rnd.randint(0, n - 1)] = rnd.randint(10**8, 10**9)
        return (n, arr)
    if kind == 5:
        n = rnd.randint(100000, 200000)
        arr = random_plain(n, 1, 10**6)
        left_peak = rnd.randint(0, n // 4)
        right_peak = rnd.randint(3 * n // 4, n - 1)
        arr[left_peak] = rnd.randint(10**8, 10**9)
        arr[right_peak] = rnd.randint(10**8, 10**9)
        return (n, arr)
    n = rnd.randint(100000, 200000)
    arr = [rnd.randint(1, 10**4) for _ in range(n)]
    segment_l = rnd.randint(1, n // 3)
    segment_r = rnd.randint(2 * n // 3, n - 2)
    height = rnd.randint(10**8, 10**9)
    arr[segment_l - 1] = height
    arr[segment_r + 1] = height
    for i in range(segment_l, segment_r + 1):
        arr[i] = rnd.randint(1, 10**3)
    return (n, arr)



def write_test(test_id, test, out_path):
    n, arr = test
    ans = solve_instance_fast(n, arr)

    inp = f"{n}\n" + ' '.join(map(str, arr))
    out = str(ans)

    with open(out_path / f"{test_id}.in", 'w', encoding='utf-8') as f:
        f.write(inp + '\n')
    with open(out_path / f"{test_id}.out", 'w', encoding='utf-8') as f:
        f.write(out + '\n')



def generate_tests(easy_count, medium_count, hard_count, out_path=Path('./tests')):
    out_path.mkdir(parents=True, exist_ok=True)

    test_id = 1
    base = predefined_tests()

    for test in base[:easy_count]:
        write_test(test_id, test, out_path)
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
        print('Использование: python generate_square_fish_pond_tests_levels.py <easy_count> <medium_count> <hard_count> <out_dir>')
        sys.exit(1)

    easy_count = int(sys.argv[1])
    medium_count = int(sys.argv[2])
    hard_count = int(sys.argv[3])
    out_path = Path(sys.argv[4])

    if easy_count < 0 or medium_count < 0 or hard_count < 0:
        print('Количество тестов должно быть неотрицательным')
        sys.exit(1)

    generate_tests(easy_count, medium_count, hard_count, out_path)


if __name__ == '__main__':
    main()
