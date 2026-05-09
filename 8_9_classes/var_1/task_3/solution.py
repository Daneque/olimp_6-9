import sys

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

def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    pts = []
    idx = 1
    for i in range(n):
        x = int(data[idx])
        y = int(data[idx + 1])
        idx += 2
        pts.append((x, y, i))

    pts.sort(key=lambda p: (p[0], p[1]))

    for i in range(1, n):
        if pts[i][0] == pts[i - 1][0] and pts[i][1] == pts[i - 1][1]:
            print(0)
            return

    py = sorted(pts, key=lambda p: (p[1], p[0]))
    ans, _ = closest_pair(pts, py)
    print(ans)

if __name__ == "__main__":
    solve()
