import sys
import math

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    p = int(data[0])
    q = int(data[1])
    b = int(data[2])
    L = int(data[3])
    R = int(data[4])

    g = math.gcd(p, q)
    step = q // g

    if L % step == 0:
        first = L
    else:
        first = L + (step - L % step)

    if R % step == 0:
        last = R
    else:
        last = R - (R % step)

    if first > last:
        print(0)
        return

    count = (last - first) // step + 1
    print(count)

if __name__ == "__main__":
    solve()