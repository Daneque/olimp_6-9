import random
import sys
import os
from pathlib import Path

def dist2(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy

def merge_by_y(left, right):
    res = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][1] <= right[j][1]:
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    res.extend(left[i:])
    res.extend(right[j:])
    return res

def closest_pair(px, py):
    n = len(px)
    if n <= 3:
        best = 10**30
        for i in range(n):
            for j in range(i + 1, n):
                best = min(best, dist2(px[i], px[j]))
        return best, sorted(px, key=lambda p: (p[1], p[0]))

    mid = n // 2
    mid_x = px[mid][0]

    qx = px[:mid]
    rx = px[mid:]

    left_ids = {p[2] for p in qx}
    qy = []
    ry = []
    for p in py:
        if p[2] in left_ids:
            qy.append(p)
        else:
            ry.append(p)

    d_left, sy_left = closest_pair(qx, qy)
    d_right, sy_right = closest_pair(rx, ry)

    d = d_left if d_left < d_right else d_right
    sy = merge_by_y(sy_left, sy_right)

    strip = []
    for p in sy:
        dx = p[0] - mid_x
        if dx * dx < d:
            strip.append(p)

    m = len(strip)
    for i in range(m):
        j = i + 1
        while j < m:
            dy = strip[j][1] - strip[i][1]
            if dy * dy >= d:
                break
            d2 = dist2(strip[i], strip[j])
            if d2 < d:
                d = d2
            j += 1

    return d, sy

def solve_instance(points):
    pts = [(x, y, i) for i, (x, y) in enumerate(points)]
    pts.sort(key=lambda p: (p[0], p[1]))

    for i in range(1, len(pts)):
        if pts[i][0] == pts[i - 1][0] and pts[i][1] == pts[i - 1][1]:
            return 0

    py = sorted(pts, key=lambda p: (p[1], p[0]))
    ans, _ = closest_pair(pts, py)
    return ans

def predefined_tests():
    return [
        [(0, 0), (3, 4)],
        [(0, 0), (1, 0), (2, 0), (10, 10)],
        [(5, 5), (5, 5), (100, 100)],
        [(-1, -1), (1, 1), (2, 2), (3, 3)],
        [(0, 0), (1000000000, 1000000000), (-1000000000, -1000000000)],
    ]

def random_points(n, coord_limit=10**6, allow_duplicates=False):
    pts = []
    used = set()
    while len(pts) < n:
        x = random.randint(-coord_limit, coord_limit)
        y = random.randint(-coord_limit, coord_limit)
        if allow_duplicates or (x, y) not in used:
            pts.append((x, y))
            used.add((x, y))
    return pts

def generate_tests(count=10, out_path=Path("./tests")):
    tests = predefined_tests()

    while len(tests) < count:
        t = len(tests) + 1
        if t % 4 == 0:
            n = random.randint(2, 2000)
            pts = random_points(n, allow_duplicates=True)
        elif t % 4 == 1:
            n = random.randint(2, 3000)
            pts = [(i, random.randint(-100, 100)) for i in range(n)]
        elif t % 4 == 2:
            n = random.randint(2, 3000)
            pts = random_points(n)
        else:
            n = random.randint(2, 5000)
            pts = [(random.randint(-10**9, 10**9), random.randint(-10**9, 10**9)) for _ in range(n)]
        tests.append(pts)

    for i, points in enumerate(tests[:count], start=1):
        ans = solve_instance(points)

        lines = [str(len(points))]
        lines.extend(f"{x} {y}" for x, y in points)
        inp = "\n".join(lines)
        out = str(ans)

        with open(out_path / f"{i}.in", "w", encoding="utf-8") as f:
            f.write(inp)
        with open(out_path / f"{i}.out", "w", encoding="utf-8") as f:
            f.write(out)

if __name__ == "__main__":
    out_path = Path(sys.argv[2])
    num_tests = int(sys.argv[1])

    if not out_path.exists():
        os.mkdir(out_path)

    generate_tests(num_tests, out_path)
