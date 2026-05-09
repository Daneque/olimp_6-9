import sys

def my_gcd(a, b):
    a = abs(a)
    b = abs(b)
    while b != 0:
        a, b = b, a % b
    return a

def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    n, k1, k2 = map(int, data)

    g = my_gcd(k1, k2)
    lcm = k1 // g * k2

    ans = n // k1 + n // k2 - n // lcm
    print(ans)

if __name__ == "__main__":
    solve()
