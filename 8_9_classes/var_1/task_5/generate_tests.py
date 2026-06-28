#!/usr/bin/env python3
import sys
import math
import random
from pathlib import Path


rnd = random.Random(987654)


def polygon_area2(poly):
    n = len(poly)
    s = 0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s)



def boundary_points(poly):
    n = len(poly)
    b = 0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        b += math.gcd(dx, dy)
    return b



def restore_order(points):
    base = min(points, key=lambda p: (p[1], p[0]))
    bx, by = base
    others = [p for p in points if p != base]
    others.sort(key=lambda p: math.atan2(p[1] - by, p[0] - bx))
    return [base] + others



def make_convex_polygon(n, coord_limit):
    angles = []
    for _ in range(n):
        angles.append(rnd.random() * 2.0 * math.pi)
    angles.sort()

    pts = []
    min_gap = max(5.0, coord_limit * 0.002)
    max_gap = max(min_gap + 5.0, coord_limit * 0.01)

    for ang in angles:
        radius = rnd.uniform(coord_limit * 0.7, coord_limit)
        x = int(round(radius * math.cos(ang)))
        y = int(round(radius * math.sin(ang)))
        pts.append((x, y))

    uniq = []
    used = set()
    for p in pts:
        if p not in used:
            uniq.append(p)
            used.add(p)

    if len(uniq) < 3:
        uniq = [(0, 0), (coord_limit, 0), (0, coord_limit)]

    poly = restore_order(uniq)

    filtered = []
    for p in poly:
        if not filtered:
            filtered.append(p)
            continue
        dx = p[0] - filtered[-1][0]
        dy = p[1] - filtered[-1][1]
        if dx * dx + dy * dy > 0:
            filtered.append(p)

    if len(filtered) >= 2 and filtered[0] == filtered[-1]:
        filtered.pop()

    poly = filtered

    if len(poly) < 3 or polygon_area2(poly) == 0:
        poly = []
        for i in range(n):
            ang = 2.0 * math.pi * i / n
            radius = coord_limit * (0.8 + 0.15 * math.sin(3 * ang))
            x = int(round(radius * math.cos(ang)))
            y = int(round(radius * math.sin(ang)))
            poly.append((x, y))
        poly = restore_order(list(dict.fromkeys(poly)))

    if len(poly) < 3 or polygon_area2(poly) == 0:
        poly = [(0, 0), (coord_limit, 0), (0, coord_limit)]

    return poly



def predefined_tests():
    return [
        [(0, 0), (3, 0), (3, 2)],
        [(0, 0), (4, 0), (4, 3), (0, 3)],
        [(0, 0), (2, 0), (3, 1), (1, 3), (-1, 2)],
    ]



def easy_polygon(idx):
    kind = idx % 3
    if kind == 0:
        n = rnd.randint(3, 6)
        return make_convex_polygon(n, coord_limit=20)
    if kind == 1:
        n = rnd.randint(3, 10)
        return make_convex_polygon(n, coord_limit=50)
    n = rnd.randint(3, 8)
    return make_convex_polygon(n, coord_limit=30)



def medium_polygon(idx):
    kind = idx % 4
    if kind == 0:
        n = rnd.randint(20, 60)
        return make_convex_polygon(n, coord_limit=500)
    if kind == 1:
        n = rnd.randint(40, 120)
        return make_convex_polygon(n, coord_limit=2000)
    if kind == 2:
        n = rnd.randint(60, 200)
        return make_convex_polygon(n, coord_limit=10000)
    n = rnd.randint(30, 100)
    return make_convex_polygon(n, coord_limit=3000)



def hard_polygon(idx):
    kind = idx % 5
    if kind == 0:
        n = rnd.randint(2000, 4000)
        return make_convex_polygon(n, coord_limit=10**6)
    if kind == 1:
        n = rnd.randint(4000, 8000)
        return make_convex_polygon(n, coord_limit=10**7)
    if kind == 2:
        n = rnd.randint(8000, 15000)
        return make_convex_polygon(n, coord_limit=10**8)
    if kind == 3:
        n = rnd.randint(15000, 25000)
        return make_convex_polygon(n, coord_limit=10**9)
    n = rnd.randint(5000, 12000)
    return make_convex_polygon(n, coord_limit=10**8)



def write_test(test_id, poly, out_path):
    ordered = restore_order(poly)
    double_area = polygon_area2(ordered)
    s = double_area // 2
    b = boundary_points(ordered)
    i = (double_area - b + 2) // 2

    shuffled = ordered[:]
    rnd.shuffle(shuffled)

    with open(out_path / f"{test_id}.in", "w", encoding="utf-8") as fin:
        fin.write(str(len(shuffled)) + "\n")
        for x, y in shuffled:
            fin.write(f"{x} {y}\n")

    with open(out_path / f"{test_id}.out", "w", encoding="utf-8") as fout:
        fout.write(f"{s} {i}")



def generate_tests(easy_count, medium_count, hard_count, out_path):
    out_path.mkdir(parents=True, exist_ok=True)
    test_id = 1

    base = predefined_tests()
    for poly in base[:easy_count]:
        write_test(test_id, poly, out_path)
        test_id += 1

    generated_easy = max(0, easy_count - min(easy_count, len(base)))
    for i in range(generated_easy):
        write_test(test_id, easy_polygon(i), out_path)
        test_id += 1

    for i in range(medium_count):
        write_test(test_id, medium_polygon(i), out_path)
        test_id += 1

    for i in range(hard_count):
        write_test(test_id, hard_polygon(i), out_path)
        test_id += 1



def main():
    if len(sys.argv) != 5:
        print("Использование: python generate_barrier_tests_levels.py <easy_count> <medium_count> <hard_count> <out_dir>")
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