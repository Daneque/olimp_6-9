import random
import sys
from pathlib import Path
from math import gcd


rnd = random.Random(123456)



def solve_instance(n, k1, k2):
    g = gcd(k1, k2)
    lcm = k1 // g * k2
    return n // k1 + n // k2 - n // lcm



def predefined_tests():
    return [
        (10, 2, 3),
        (1, 2, 3),
        (100, 10, 10),
        (100, 1, 999999937),
        (10**18, 999999937, 1000000007),
        (999999999999999999, 2, 4),
        (123456789, 17, 19),
        (10**18, 1, 1),
    ]



def easy_test(idx):
    kind = idx % 5
    if kind == 0:
        n = rnd.randint(1, 100)
        k1 = rnd.randint(1, 20)
        k2 = rnd.randint(1, 20)
        return (n, k1, k2)
    if kind == 1:
        n = rnd.randint(1, 1000)
        k1 = rnd.randint(1, 50)
        k2 = k1
        return (n, k1, k2)
    if kind == 2:
        n = rnd.randint(1, 500)
        k1 = 1
        k2 = rnd.randint(1, 100)
        return (n, k1, k2)
    if kind == 3:
        n = rnd.randint(1, 1000)
        k1 = rnd.randint(2, 30)
        mul = rnd.randint(1, 10)
        k2 = k1 * mul
        return (n, k1, k2)
    n = rnd.randint(1, 1000)
    k1 = rnd.randint(1, 100)
    k2 = rnd.randint(1, 100)
    return (n, k1, k2)



def medium_test(idx):
    kind = idx % 6
    if kind == 0:
        n = rnd.randint(10**5, 10**9)
        k1 = rnd.randint(1, 10**5)
        k2 = rnd.randint(1, 10**5)
        return (n, k1, k2)
    if kind == 1:
        n = rnd.randint(10**6, 10**12)
        k1 = rnd.randint(1, 10**6)
        k2 = k1
        return (n, k1, k2)
    if kind == 2:
        n = rnd.randint(10**6, 10**12)
        k1 = rnd.randint(2, 10**5)
        k2 = k1 * rnd.randint(1, 20)
        return (n, k1, k2)
    if kind == 3:
        n = rnd.randint(10**6, 10**12)
        k1 = rnd.randint(1, 10**6)
        k2 = 1
        return (n, k1, k2)
    if kind == 4:
        n = rnd.randint(10**8, 10**12)
        k1 = rnd.randint(10**4, 10**6)
        k2 = rnd.randint(10**4, 10**6)
        return (n, k1, k2)
    n = rnd.randint(10**7, 10**12)
    k1 = rnd.randint(1, 10**6)
    k2 = rnd.randint(1, 10**6)
    return (n, k1, k2)



def random_prime_like(lo, hi):
    while True:
        x = rnd.randint(lo, hi)
        if x % 2 == 0:
            x += 1
        return min(x, hi)



def hard_test(idx):
    kind = idx % 7
    if kind == 0:
        n = rnd.randint(10**17, 10**18)
        k1 = rnd.randint(1, 10**9)
        k2 = rnd.randint(1, 10**9)
        return (n, k1, k2)
    if kind == 1:
        n = rnd.randint(10**17, 10**18)
        k1 = random_prime_like(10**8, 10**9)
        k2 = random_prime_like(10**8, 10**9)
        return (n, k1, k2)
    if kind == 2:
        n = rnd.randint(10**17, 10**18)
        k1 = rnd.randint(1, 10**9)
        k2 = k1
        return (n, k1, k2)
    if kind == 3:
        n = rnd.randint(10**17, 10**18)
        k1 = rnd.randint(2, 10**8)
        k2 = k1 * rnd.randint(1, 10)
        if k2 > 10**9:
            k2 = 10**9
        return (n, k1, k2)
    if kind == 4:
        n = 10**18
        k1 = 1
        k2 = rnd.randint(1, 10**9)
        return (n, k1, k2)
    if kind == 5:
        n = rnd.randint(10**17, 10**18)
        k1 = 10**9
        k2 = rnd.randint(1, 10**9)
        return (n, k1, k2)
    n = rnd.randint(10**17, 10**18)
    k1 = rnd.randint(1, 10**9)
    k2 = rnd.randint(1, 10**9)
    return (n, k1, k2)



def write_test(test_id, test, out_path):
    n, k1, k2 = test
    ans = solve_instance(n, k1, k2)

    inp = f"{n} {k1} {k2}"
    out = str(ans)

    with open(out_path / f"{test_id}.in", "w", encoding="utf-8") as f:
        f.write(inp)
    with open(out_path / f"{test_id}.out", "w", encoding="utf-8") as f:
        f.write(out)



def generate_tests(easy_count, medium_count, hard_count, out_path=Path("./tests")):
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
        print("Использование: python generate_safe_sectors_tests_levels.py <easy_count> <medium_count> <hard_count> <out_dir>")
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
