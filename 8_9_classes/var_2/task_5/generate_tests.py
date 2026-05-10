import sys
import os
from pathlib import Path
import random
import math


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
        dx = x2 - x1
        dy = y2 - y1
        per += math.hypot(dx, dy)
    return per


def solve_instance(points, R):
    hull = convex_hull(points)
    area_hull = polygon_area(hull)
    per_hull = polygon_perimeter(hull)
    total_area = area_hull + per_hull * R + math.pi * R * R
    return int(total_area)


def predefined_tests():
    tests = []

    # 1) Пример из условия: квадрат 2x2, добавим пару внутренних точек
    hull1 = [(0, 0), (2, 0), (2, 2), (0, 2)]
    inner1 = [(1, 1)]
    pts1 = hull1 + inner1
    tests.append((len(pts1), 1, pts1))

    # 2) Треугольник с внутренними точками
    hull2 = [(0, 0), (4, 0), (0, 3)]
    inner2 = [(1, 1), (1, 2)]
    pts2 = hull2 + inner2
    tests.append((len(pts2), 1, pts2))

    # 3) Шестиугольник и несколько внутренних
    hull3 = []
    for k in range(6):
        angle = 2 * math.pi * k / 6
        x = int(round(10 * math.cos(angle)))
        y = int(round(10 * math.sin(angle)))
        hull3.append((x, y))
    inner3 = [(0, 0), (1, 1), (-2, 1)]
    pts3 = hull3 + inner3
    tests.append((len(pts3), 2, pts3))

    # 4) Случайный выпуклый многоугольник + внутренняя "россыпь"
    hull4 = [(0, 0), (5, 0), (6, 2), (3, 4), (0, 3)]
    inner4 = [(2, 1), (3, 2), (2, 3)]
    pts4 = hull4 + inner4
    tests.append((len(pts4), 3, pts4))

    return tests


def random_points_with_inner(n, coord_limit):
    # генерируем n случайных точек, потом по ним считаем оболочку
    pts = set()
    while len(pts) < n:
        x = random.randint(-coord_limit, coord_limit)
        y = random.randint(-coord_limit, coord_limit)
        pts.add((x, y))
    pts = list(pts)
    return pts


def random_test():
    # иногда немного точек, иногда побольше
    r = random.random()
    if r < 0.3:
        n = random.randint(3, 20)
        coord_limit = 50
    elif r < 0.7:
        n = random.randint(20, 500)
        coord_limit = 1000
    else:
        n = random.randint(500, 2000)
        coord_limit = 10**7

    pts = random_points_with_inner(n, coord_limit)
    R = random.randint(1, 10000)
    return len(pts), R, pts


def generate_tests(count, out_path):
    tests = predefined_tests()

    while len(tests) < count:
        tests.append(random_test())

    for i, (n, R, pts) in enumerate(tests[:count], start=1):
        ans = solve_instance(pts, R)

        in_lines = [f"{n} {R}"]
        for x, y in pts:
            in_lines.append(f"{x} {y}")
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