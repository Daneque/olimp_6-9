import sys


def max_len_subarray_leq_s(a, S):
    n = len(a)
    best = 0
    cur_sum = 0
    left = 0
    for right in range(n):
        cur_sum += a[right]
        while cur_sum > S and left <= right:
            cur_sum -= a[left]
            left += 1
        # здесь сумма на [left, right] <= S
        length = right - left + 1
        if length > best:
            best = length
    return best


def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    it = iter(data)
    n = int(next(it))
    S = int(next(it))
    a = [int(next(it)) for _ in range(n)]

    ans = max_len_subarray_leq_s(a, S)
    print(ans)


if __name__ == "__main__":
    solve()