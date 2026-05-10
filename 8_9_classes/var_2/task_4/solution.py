import sys


def max_area(heights):
    left = 0
    right = len(heights) - 1
    best = 0

    while left < right:
        h_left = heights[left]
        h_right = heights[right]

        width = right - left
        current = (h_left if h_left < h_right else h_right) * width
        if current > best:
            best = current

        if h_left < h_right:
            left += 1
        else:
            right -= 1

    return best


def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    heights = [int(x) for x in data[1:1 + n]]

    ans = max_area(heights)
    print(ans)


if __name__ == "__main__":
    solve()