import sys


def xor_1_to_n(n: int) -> int:
    r = n % 4
    if r == 0:
        return n
    if r == 1:
        return 1
    if r == 2:
        return n + 1
    return 0


def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    ans = xor_1_to_n(n)
    print(ans)


if __name__ == "__main__":
    solve()