#!/usr/bin/env python3
import sys
import os
import random
import math

def cross(o, a, b):
    # векторное произведение OA x OB
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def convex_hull(points):
    # монотонная цепь, возвращает вершины выпуклой оболочки
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # последняя точка каждого списка — дубликат первой другой части
    return lower[:-1] + upper[:-1]

def restore_order(points):
    # тот же порядок, что и в solution.py:
    # базовая точка — минимальный (y, затем x), сортировка остальных по atan2
    base = min(points, key=lambda p: (p[1], p[0]))
    bx, by = base
    others = [p for p in points if p != base]
    others.sort(key=lambda p: math.atan2(p[1] - by, p[0] - bx))
    return [base] + others

def polygon_area2(poly):
    # удвоенная площадь по формуле Гаусса
    n = len(poly)
    s = 0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s)

def boundary_points(poly):
    # B = сумма gcd(|dx|, |dy|) по рёбрам
    n = len(poly)
    B = 0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        B += math.gcd(dx, dy)
    return B

def generate_convex_polygon(n, rnd, coord_limit=10**6):
    # генерируем много точек, берём выпуклую оболочку, пока размер оболочки = n
    # чтобы не зациклиться, позволим hull иметь >= n и возьмём подмножество
    while True:
        m = max(n + 5, n * 2)
        pts = []
        for _ in range(m):
            x = rnd.randint(-coord_limit, coord_limit)
            y = rnd.randint(-coord_limit, coord_limit)
            pts.append((x, y))

        hull = convex_hull(pts)
        if len(hull) < n:
            continue
        if len(hull) > n:
            # берём равномерно распределённые по контуру n точек
            step = len(hull) / n
            new_hull = []
            cur = 0.0
            for _ in range(n):
                new_hull.append(hull[int(cur)])
                cur += step
            hull = new_hull

        # проверяем ненулевую площадь
        if polygon_area2(hull) > 0:
            return hull

def main():
    if len(sys.argv) < 3:
        print("Usage: generate_tests.py <count> <dir>")
        return

    t = int(sys.argv[1])
    out_dir = sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)

    rnd = random.Random(987654)

    for test_id in range(1, t + 1):
        # размер многоугольника
        if test_id == 1:
            n = 3
        elif test_id == 2:
            n = 4
        elif test_id <= 5:
            n = rnd.randint(3, 10)
        elif test_id <= 10:
            n = rnd.randint(10, 50)
        else:
            n = rnd.randint(50, 2000)

        poly = generate_convex_polygon(n, rnd)

        # приводим порядок к тому же, что в solution.py
        ordered = restore_order(poly)

        double_area = polygon_area2(ordered)
        S = double_area // 2
        B = boundary_points(ordered)
        I = (double_area - B + 2) // 2

        # во входе вершины перемешаны
        shuffled = ordered[:]
        rnd.shuffle(shuffled)

        in_path = os.path.join(out_dir, f"{test_id}.in")
        out_path = os.path.join(out_dir, f"{test_id}.out")

        with open(in_path, "w") as fin:
            fin.write(str(n) + "\n")
            for x, y in shuffled:
                fin.write(f"{x} {y}\n")

        with open(out_path, "w") as fout:
            fout.write(f"{S} {I}")

if __name__ == "__main__":
    main()