import random
import sys
from pathlib import Path
from math import gcd


rnd = random.Random(123456)



def solve_instance(p, q, b, l, r):
    if l > r:
        l, r = r, l

    y_l = (p * l + b * q) // q
    y_r = (p * r + b * q) // q

    dx = abs(r - l)
    dy = abs(y_r - y_l)

    return gcd(dx, dy) + 1



def coprime_pair(limit_q, limit_p):
    while True:
        q = rnd.randint(1, limit_q)
        p = rnd.randint(-limit_p, limit_p)
        if gcd(abs(p), q) == 1:
            return p, q



def predefined_tests():
    return [
        (1, 1, 0, 0, 10),
        (2, 1, 3, -5, 5),
        (1, 2, 0, 0, 10),
        (-3, 2, 7, 4, 10),
        (0, 1, 5, -100, 100),
        (7, 3, -2, 6, 6),
        (5, 4, 1, 8, 20),
    ]



def build_test(limit_p, limit_q, limit_b, limit_base, limit_step, force_zero_step=False):
    p, q = coprime_pair(limit_q=limit_q, limit_p=limit_p)
    b = rnd.randint(-limit_b, limit_b)

    base = rnd.randint(-limit_base, limit_base)
    if force_zero_step:
        step = 0
    else:
        step = rnd.randint(0, limit_step)

    l = base * q
    r = (base + step) * q
    return (p, q, b, l, r)



def easy_test(idx):
    kind = idx % 5
    if kind == 0:
        return build_test(limit_p=20, limit_q=10, limit_b=100, limit_base=20, limit_step=20)
    if kind == 1:
        return build_test(limit_p=30, limit_q=20, limit_b=1000, limit_base=50, limit_step=30)
    if kind == 2:
        return build_test(limit_p=10, limit_q=10, limit_b=50, limit_base=10, limit_step=0, force_zero_step=True)
    if kind == 3:
        return build_test(limit_p=50, limit_q=30, limit_b=500, limit_base=100, limit_step=5)
    return build_test(limit_p=5, limit_q=1, limit_b=100, limit_base=50, limit_step=50)



def medium_test(idx):
    kind = idx % 6
    if kind == 0:
        return build_test(limit_p=10**4, limit_q=10**4, limit_b=10**5, limit_base=10**4, limit_step=10**4)
    if kind == 1:
        return build_test(limit_p=10**5, limit_q=10**5, limit_b=10**6, limit_base=10**5, limit_step=10**3)
    if kind == 2:
        return build_test(limit_p=10**4, limit_q=10**3, limit_b=10**5, limit_base=10**5, limit_step=10**5)
    if kind == 3:
        return build_test(limit_p=10**5, limit_q=10**5, limit_b=10**4, limit_base=10**3, limit_step=0, force_zero_step=True)
    if kind == 4:
        return build_test(limit_p=10**3, limit_q=10**5, limit_b=10**6, limit_base=10**5, limit_step=10**4)
    return build_test(limit_p=10**5, limit_q=1, limit_b=10**6, limit_base=10**5, limit_step=10**5)



def hard_test(idx):
    kind = idx % 7
    if kind == 0:
        return build_test(limit_p=10**9, limit_q=10**9, limit_b=10**9, limit_base=10**9 // 10**5, limit_step=10**5)
    if kind == 1:
        return build_test(limit_p=10**9, limit_q=10**9, limit_b=10**9, limit_base=10**6, limit_step=10**9 // 10**5)
    if kind == 2:
        return build_test(limit_p=10**9, limit_q=10**6, limit_b=10**9, limit_base=10**8, limit_step=10**6)
    if kind == 3:
        return build_test(limit_p=10**8, limit_q=10**9, limit_b=10**9, limit_base=10**8, limit_step=10**4)
    if kind == 4:
        return build_test(limit_p=10**9, limit_q=10**9, limit_b=10**9, limit_base=10**9 // 10**6, limit_step=0, force_zero_step=True)
    if kind == 5:
        return build_test(limit_p=10**9, limit_q=1, limit_b=10**9, limit_base=10**9 // 10**5, limit_step=10**5)
    return build_test(limit_p=10**9, limit_q=10**9, limit_b=10**9, limit_base=10**4, limit_step=10**9 // 10**4)



def write_test(test_id, test, out_path):
    p, q, b, l, r = test
    ans = solve_instance(p, q, b, l, r)

    inp = f"{p} {q} {b} {l} {r}"
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
        print("Использование: python generate_fireline_tests_levels.py <easy_count> <medium_count> <hard_count> <out_dir>")
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
