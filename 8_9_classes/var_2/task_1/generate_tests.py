import random
import sys
from pathlib import Path


rnd = random.Random(123456)



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
        (12, 2, 8),
        (1, 1, 1),
        (10, 1, 10),
        (10, 2, 2),
        (10, 3, 9),
        (36, 1, 6),
        (999983, 1, 999983),
        (10**12, 1, 10**12),
    ]



def make_range(n, mode):
    if mode == 0:
        return 1, n
    if mode == 1:
        x = rnd.randint(1, n)
        return x, x
    if mode == 2:
        l = rnd.randint(1, max(1, n // 2))
        r = rnd.randint(l, min(n, l + max(1, n // 1000 + 10)))
        return l, r
    l = rnd.randint(1, n)
    r = rnd.randint(l, n)
    return l, r



def easy_test(idx):
    kind = idx % 5
    if kind == 0:
        n = rnd.randint(1, 100)
        L, R = make_range(n, 0)
        return (n, L, R)
    if kind == 1:
        n = rnd.randint(1, 1000)
        L, R = make_range(n, 1)
        return (n, L, R)
    if kind == 2:
        n = rnd.randint(1, 5000)
        L, R = make_range(n, 2)
        return (n, L, R)
    if kind == 3:
        base = rnd.randint(1, 50)
        n = base * base
        L, R = make_range(n, 3)
        return (n, L, R)
    n = rnd.randint(1, 10**4)
    L, R = make_range(n, 3)
    return (n, L, R)



def medium_test(idx):
    kind = idx % 6
    if kind == 0:
        n = rnd.randint(10**5, 10**7)
        L, R = make_range(n, 0)
        return (n, L, R)
    if kind == 1:
        n = rnd.randint(10**6, 10**8)
        L, R = make_range(n, 2)
        return (n, L, R)
    if kind == 2:
        a = rnd.randint(10**3, 10**4)
        b = rnd.randint(10**3, 10**4)
        n = a * b
        L, R = make_range(n, 3)
        return (n, L, R)
    if kind == 3:
        a = rnd.randint(10**3, 10**5)
        n = a * a
        L, R = make_range(n, 3)
        return (n, L, R)
    if kind == 4:
        n = rnd.randint(10**7, 10**9)
        L, R = make_range(n, 1)
        return (n, L, R)
    n = rnd.randint(10**6, 10**9)
    L, R = make_range(n, 3)
    return (n, L, R)



def hard_test(idx):
    kind = idx % 7
    if kind == 0:
        n = rnd.randint(10**10, 10**12)
        L, R = make_range(n, 0)
        return (n, L, R)
    if kind == 1:
        n = rnd.randint(10**11, 10**12)
        L, R = make_range(n, 2)
        return (n, L, R)
    if kind == 2:
        a = rnd.randint(10**5, 10**6)
        b = rnd.randint(10**5, 10**6)
        n = a * b
        if n > 10**12:
            n = 10**12
        L, R = make_range(n, 3)
        return (n, L, R)
    if kind == 3:
        a = rnd.randint(10**5, 10**6)
        n = a * a
        if n > 10**12:
            n = 10**12
        L, R = make_range(n, 3)
        return (n, L, R)
    if kind == 4:
        n = 10**12
        L, R = make_range(n, 1)
        return (n, L, R)
    if kind == 5:
        n = rnd.randint(10**11, 10**12)
        L, R = make_range(n, 3)
        return (n, L, R)
    n = rnd.randint(10**10, 10**12)
    L, R = make_range(n, 2)
    return (n, L, R)



def write_test(test_id, test, out_path):
    n, L, R = test
    ans = count_divisors_in_range(n, L, R)

    with open(out_path / f"{test_id}.in", "w", encoding='utf-8') as f:
        f.write(f"{n} {L} {R}")
    with open(out_path / f"{test_id}.out", "w", encoding='utf-8') as f:
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
        print('Использование: python generate_quantum_points_tests_levels.py <easy_count> <medium_count> <hard_count> <out_dir>')
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
