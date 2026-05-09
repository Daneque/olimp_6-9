import sys
import math

def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    it = iter(data)
    n = int(next(it))
    pts = [(int(next(it)), int(next(it))) for _ in range(n)]

    base = min(pts, key=lambda p: (p[1], p[0]))
    bx, by = base

    def angle_key(p):
        return math.atan2(p[1] - by, p[0] - bx)

    others = [p for p in pts if p != base]
    others.sort(key=angle_key)

    poly = [base] + others

    double_area = 0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        double_area += x1 * y2 - x2 * y1
    double_area = abs(double_area)
    area = double_area // 2

    # точки на границе
    B = 0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        B += math.gcd(dx, dy)

    I = (double_area - B + 2) // 2

    print(area, I)

if __name__ == "__main__":
    solve()