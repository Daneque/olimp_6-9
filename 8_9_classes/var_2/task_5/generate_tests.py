import sys
import math
import random
from pathlib import Path


rnd = random.Random(123456)



def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])



def convex_hull(points):
    points = sorted(points)
    if len(points) <= 1:
        return points

    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]



def polygon_area(hull):
    n = len(hull)
    if n < 3:
        return 0.0
    s = 0
    for i in range(n):
        x1, y1 = hull[i]
        x2, y2 = hull[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0



def polygon_perimeter(hull):
    n = len(hull)
    if n == 0:
        return 0.0
    per = 0.0
    for i in range(n):
        x1, y1 = hull[i]
        x2, y2 = hull[(i + 1) % n]
        per += math.hypot(x2 - x1, y2 - y1)
    return per



def solve_instance(points, R):
    hull = convex_hull(points)
    area_hull = polygon_area(hull)
    per_hull = polygon_perimeter(hull)
    total_area = area_hull + per_hull * R + math.pi * R * R
    return int(total_area)



def predefined_tests():
    tests = []

    hull1 = [(0, 0), (2, 0), (2, 2), (0, 2)]
    inner1 = [(1, 1)]
    pts1 = hull1 + inner1
    tests.append((len(pts1), 1, pts1))

    hull2 = [(0, 0), (4, 0), (0, 3)]
    inner2 = [(1, 1), (1, 2)]
    pts2 = hull2 + inner2
    tests.append((len(pts2), 1, pts2))

    hull3 = []
    for k in range(6):
        angle = 2 * math.pi * k / 6
        x = int(round(10 * math.cos(angle)))
        y = int(round(10 * math.sin(angle)))
        hull3.append((x, y))
    inner3 = [(0, 0), (1, 1), (-2, 1)]
    pts3 = hull3 + inner3
    tests.append((len(pts3), 2, pts3))

    hull4 = [(0, 0), (5, 0), (6, 2), (3, 4), (0, 3)]
    inner4 = [(2, 1), (3, 2), (2, 3)]
    pts4 = hull4 + inner4
    tests.append((len(pts4), 3, pts4))

    return tests



def random_points(n, coord_limit):
    pts = set()
    while len(pts) < n:
        x = rnd.randint(-coord_limit, coord_limit)
        y = rnd.randint(-coord_limit, coord_limit)
        pts.add((x, y))
    return list(pts)



def regular_polygon_with_inner(n, radius, inner_count):
    hull = []
    for k in range(n):
        angle = 2 * math.pi * k / n
        x = int(round(radius * math.cos(angle)))
        y = int(round(radius * math.sin(angle)))
        hull.append((x, y))

    pts = set(hull)
    while len(pts) < n + inner_count:
        x = rnd.randint(-radius // 2, radius // 2)
        y = rnd.randint(-radius // 2, radius // 2)
        pts.add((x, y))
    return list(pts)



def easy_test(idx):
    kind = idx % 5
    if kind == 0:
        n = rnd.randint(3, 10)
        R = rnd.randint(1, 10)
        pts = random_points(n, 20)
        return (len(pts), R, pts)
    if kind == 1:
        hull_n = rnd.randint(3, 8)
        inner = rnd.randint(0, 5)
        pts = regular_polygon_with_inner(hull_n, rnd.randint(5, 20), inner)
        R = rnd.randint(1, 5)
        return (len(pts), R, pts)
    if kind == 2:
        n = rnd.randint(3, 15)
        R = 1
        pts = random_points(n, 30)
        return (len(pts), R, pts)
    if kind == 3:
        n = rnd.randint(3, 12)
        R = rnd.randint(1, 20)
        pts = random_points(n, 50)
        return (len(pts), R, pts)
    hull_n = rnd.randint(4, 10)
    pts = regular_polygon_with_inner(hull_n, rnd.randint(10, 30), rnd.randint(1, 4))
    R = rnd.randint(2, 10)
    return (len(pts), R, pts)



def medium_test(idx):
    kind = idx % 6
    if kind == 0:
        n = rnd.randint(20, 100)
        R = rnd.randint(1, 100)
        pts = random_points(n, 1000)
        return (len(pts), R, pts)
    if kind == 1:
        hull_n = rnd.randint(10, 40)
        inner = rnd.randint(10, 50)
        pts = regular_polygon_with_inner(hull_n, rnd.randint(100, 1000), inner)
        R = rnd.randint(10, 200)
        return (len(pts), R, pts)
    if kind == 2:
        n = rnd.randint(50, 300)
        R = rnd.randint(1, 500)
        pts = random_points(n, 5000)
        return (len(pts), R, pts)
    if kind == 3:
        n = rnd.randint(100, 500)
        R = rnd.randint(100, 1000)
        pts = random_points(n, 10**5)
        return (len(pts), R, pts)
    if kind == 4:
        hull_n = rnd.randint(20, 60)
        inner = rnd.randint(20, 100)
        pts = regular_polygon_with_inner(hull_n, rnd.randint(500, 3000), inner)
        R = rnd.randint(1, 1000)
        return (len(pts), R, pts)
    n = rnd.randint(50, 500)
    R = rnd.randint(1, 1000)
    pts = random_points(n, 10**6)
    return (len(pts), R, pts)



def hard_test(idx):
    kind = idx % 7
    if kind == 0:
        n = rnd.randint(1000, 5000)
        R = rnd.randint(1000, 10000)
        pts = random_points(n, 10**7)
        return (len(pts), R, pts)
    if kind == 1:
        hull_n = rnd.randint(200, 1000)
        inner = rnd.randint(500, 3000)
        pts = regular_polygon_with_inner(hull_n, rnd.randint(10**4, 10**6), inner)
        R = rnd.randint(1, 10000)
        return (len(pts), R, pts)
    if kind == 2:
        n = rnd.randint(3000, 10000)
        R = rnd.randint(1, 10000)
        pts = random_points(n, 10**7)
        return (len(pts), R, pts)
    if kind == 3:
        n = rnd.randint(10000, 30000)
        R = rnd.randint(100, 10000)
        pts = random_points(n, 10**7)
        return (len(pts), R, pts)
    if kind == 4:
        hull_n = rnd.randint(500, 2000)
        inner = rnd.randint(5000, 15000)
        pts = regular_polygon_with_inner(hull_n, rnd.randint(10**5, 10**7), inner)
        R = rnd.randint(1, 10000)
        return (len(pts), R, pts)
    if kind == 5:
        n = rnd.randint(30000, 80000)
        R = rnd.randint(1, 10000)
        pts = random_points(n, 10**7)
        return (len(pts), R, pts)
    n = rnd.randint(80000, 200000)
    R = rnd.randint(1, 10000)
    pts = random_points(n, 10**7)
    return (len(pts), R, pts)



def write_test(test_id, test, out_path):
    n, R, pts = test
    ans = solve_instance(pts, R)

    lines = [f"{n} {R}"]
    for x, y in pts:
        lines.append(f"{x} {y}")
    inp = '\n'.join(lines)

    with open(out_path / f"{test_id}.in", 'w', encoding='utf-8') as f:
        f.write(inp + '\n')
    with open(out_path / f"{test_id}.out", 'w', encoding='utf-8') as f:
        f.write(str(ans) + '\n')



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
        print('Использование: python generate_ents_reserve_tests_levels.py <easy_count> <medium_count> <hard_count> <out_dir>')
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
