import random
import sys
from pathlib import Path


rnd = random.Random(123456)



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
        (5, 7, [2, 1, 5, 1, 3]),
        (1, 5, [3]),
        (1, 5, [10]),
        (4, 100, [10, 20, 30, 40]),
        (3, 1, [5, 5, 5]),
        (4, 6, [1, 2, 3, 4]),
    ]



def make_test(n, value_lo, value_hi, s_mode):
    a = [rnd.randint(value_lo, value_hi) for _ in range(n)]
    total = sum(a)

    if s_mode == 0:
        S = rnd.randint(1, max(1, min(total, total // 3 + 1)))
    elif s_mode == 1:
        S = rnd.randint(1, max(1, total))
    elif s_mode == 2:
        S = total + rnd.randint(0, max(1, total // 10 + 1))
    elif s_mode == 3:
        S = max(1, min(a) - 1)
    else:
        pos = rnd.randint(0, n - 1)
        S = sum(a[:pos + 1])

    return (n, S, a)



def easy_test(idx):
    kind = idx % 5
    if kind == 0:
        n = rnd.randint(1, 10)
        return make_test(n, 1, 20, 0)
    if kind == 1:
        n = rnd.randint(1, 15)
        return make_test(n, 1, 30, 1)
    if kind == 2:
        n = rnd.randint(1, 12)
        return make_test(n, 1, 15, 2)
    if kind == 3:
        n = rnd.randint(1, 10)
        return make_test(n, 2, 25, 3)
    n = rnd.randint(1, 20)
    return make_test(n, 1, 20, 4)



def medium_test(idx):
    kind = idx % 6
    if kind == 0:
        n = rnd.randint(100, 2000)
        return make_test(n, 1, 10**3, 0)
    if kind == 1:
        n = rnd.randint(200, 3000)
        return make_test(n, 1, 10**4, 1)
    if kind == 2:
        n = rnd.randint(300, 4000)
        return make_test(n, 1, 10**3, 2)
    if kind == 3:
        n = rnd.randint(100, 2000)
        return make_test(n, 10, 10**4, 3)
    if kind == 4:
        n = rnd.randint(200, 5000)
        a = [1] * (n - 1) + [10**4]
        rnd.shuffle(a)
        S = rnd.randint(1, n)
        return (n, S, a)
    n = rnd.randint(300, 5000)
    a = [rnd.randint(1, 50) for _ in range(n)]
    pos = rnd.randint(0, n - 1)
    a[pos] = rnd.randint(10**3, 10**4)
    S = rnd.randint(50, 500)
    return (n, S, a)



def hard_test(idx):
    kind = idx % 7
    if kind == 0:
        n = rnd.randint(30000, 80000)
        return make_test(n, 1, 10**4, 0)
    if kind == 1:
        n = rnd.randint(50000, 120000)
        return make_test(n, 1, 10**4, 1)
    if kind == 2:
        n = rnd.randint(80000, 200000)
        return make_test(n, 1, 10**4, 2)
    if kind == 3:
        n = rnd.randint(30000, 100000)
        return make_test(n, 2, 10**4, 3)
    if kind == 4:
        n = rnd.randint(100000, 200000)
        a = [1] * (n - 1) + [10**9]
        rnd.shuffle(a)
        S = rnd.randint(1, n)
        return (n, S, a)
    if kind == 5:
        n = rnd.randint(120000, 200000)
        a = [rnd.randint(1, 100) for _ in range(n)]
        for _ in range(max(1, n // 5000)):
            a[rnd.randint(0, n - 1)] = 10**9
        S = rnd.randint(10**3, 10**6)
        return (n, S, a)
    n = rnd.randint(100000, 200000)
    a = [rnd.randint(1, 10**9) for _ in range(n)]
    total = sum(a)
    S = rnd.randint(1, min(total, 10**14))
    return (n, S, a)



def write_test(test_id, test, out_path):
    n, S, a = test
    ans = max_len_subarray_leq_s(a, S)

    in_lines = [f"{n} {S}", ' '.join(map(str, a))]
    inp = '\n'.join(in_lines)

    with open(out_path / f"{test_id}.in", 'w', encoding='utf-8') as f:
        f.write(inp)
    with open(out_path / f"{test_id}.out", 'w', encoding='utf-8') as f:
        f.write(str(ans))



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
        print('Использование: python generate_shield_line_tests_levels.py <easy_count> <medium_count> <hard_count> <out_dir>')
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
