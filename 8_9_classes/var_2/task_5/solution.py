import sys
import math


def cross(o, a, b):
    # векторное произведение OA x OB
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points):
    # алгоритм Эндрю, возвращает вершины оболочки в обходе по контуру
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

    # последняя точка каждого списка - дубликат первой точки другого списка
    return lower[:-1] + upper[:-1]


def polygon_area(hull):
    # площадь по формуле Гаусса
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


def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    it = iter(data)
    n = int(next(it))
    R = int(next(it))

    pts = []
    for _ in range(n):
        x = int(next(it))
        y = int(next(it))
        pts.append((x, y))

    hull = convex_hull(pts)
    area_hull = polygon_area(hull)
    per_hull = polygon_perimeter(hull)

    total_area = area_hull + per_hull * R + math.pi * R * R

    # по условию — целая часть
    print(int(total_area))


if __name__ == "__main__":
    solve()