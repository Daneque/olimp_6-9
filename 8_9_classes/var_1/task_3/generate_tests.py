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

    d = min(d_left, d_right)
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



def line_points(n, y_limit):
    return [(i, random.randint(-y_limit, y_limit)) for i in range(n)]



def cluster_points(n, center_limit, spread, allow_duplicates=False):
    cx = random.randint(-center_limit, center_limit)
    cy = random.randint(-center_limit, center_limit)
    pts = []
    used = set()
    while len(pts) < n:
        x = cx + random.randint(-spread, spread)
        y = cy + random.randint(-spread, spread)
        if allow_duplicates or (x, y) not in used:
            pts.append((x, y))
            used.add((x, y))
    return pts



def easy_test(idx):
    kind = idx % 4
    if kind == 0:
        n = random.randint(2, 50)
        return random_points(n, coord_limit=100, allow_duplicates=False)
    if kind == 1:
        n = random.randint(2, 120)
        return line_points(n, y_limit=20)
    if kind == 2:
        n = random.randint(2, 80)
        return random_points(n, coord_limit=200, allow_duplicates=True)
    n = random.randint(2, 150)
    return cluster_points(n, center_limit=100, spread=10, allow_duplicates=False)



def medium_test(idx):
    kind = idx % 5
    if kind == 0:
        n = random.randint(500, 1500)
        return random_points(n, coord_limit=10**5, allow_duplicates=False)
    if kind == 1:
        n = random.randint(500, 2000)
        return line_points(n, y_limit=10**3)
    if kind == 2:
        n = random.randint(500, 1500)
        return random_points(n, coord_limit=10**5, allow_duplicates=True)
    if kind == 3:
        n = random.randint(700, 1800)
        return cluster_points(n, center_limit=10**5, spread=200, allow_duplicates=False)
    n = random.randint(600, 1600)
    pts1 = cluster_points(n // 2, center_limit=10**5, spread=100, allow_duplicates=False)
    pts2 = cluster_points(n - n // 2, center_limit=10**5, spread=100, allow_duplicates=False)
    return pts1 + pts2



def hard_test(idx):
    kind = idx % 6
    if kind == 0:
        n = random.randint(3500, 5000)
        return random_points(n, coord_limit=10**9, allow_duplicates=False)
    if kind == 1:
        n = random.randint(3500, 5000)
        return random_points(n, coord_limit=10**9, allow_duplicates=True)
    if kind == 2:
        n = random.randint(3500, 5000)
        return line_points(n, y_limit=10**6)
    if kind == 3:
        n = random.randint(3500, 5000)
        return [(random.randint(-10**9, 10**9), random.randint(-10**9, 10**9)) for _ in range(n)]
    if kind == 4:
        n = random.randint(3500, 5000)
        return cluster_points(n, center_limit=10**9, spread=10**4, allow_duplicates=False)
    n = random.randint(3500, 5000)
    pts1 = cluster_points(n // 2, center_limit=10**9, spread=10**3, allow_duplicates=False)
    pts2 = cluster_points(n - n // 2, center_limit=10**9, spread=10**3, allow_duplicates=False)
    return pts1 + pts2



def write_test(test_id, points, out_path):
    ans = solve_instance(points)

    lines = [str(len(points))]
    lines.extend(f"{x} {y}" for x, y in points)
    inp = "\n".join(lines)
    out = str(ans)

    with open(out_path / f"{test_id}.in", "w", encoding="utf-8") as f:
        f.write(inp)
    with open(out_path / f"{test_id}.out", "w", encoding="utf-8") as f:
        f.write(out)



def generate_tests(easy_count, medium_count, hard_count, out_path=Path("./tests")):
    out_path.mkdir(parents=True, exist_ok=True)

    test_id = 1

    base = predefined_tests()
    for points in base[:easy_count]:
        write_test(test_id, points, out_path)
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
        print("Использование: python generate_tests_levels.py <easy_count> <medium_count> <hard_count> <out_dir>")
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