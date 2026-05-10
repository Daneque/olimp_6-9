import sys


def count_divisors_in_range(n: int, L: int, R: int) -> int:
    cnt = 0
    d = 1
    while d * d <= n:
        if n % d == 0:
            q = n // d
            if L <= d <= R:
                cnt += 1
            if q != d and L <= q <= R:
                cnt += 1
        d += 1
    return cnt


def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    L = int(data[1])
    R = int(data[2])

    ans = count_divisors_in_range(n, L, R)
    print(ans)


if __name__ == "__main__":
    solve()