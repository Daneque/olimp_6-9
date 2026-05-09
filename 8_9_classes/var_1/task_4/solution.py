import sys

def heap_push(h, x):
    h.append(x)
    i = len(h) - 1
    while i > 0:
        p = (i - 1) // 2
        if h[p] <= h[i]:
            break
        h[p], h[i] = h[i], h[p]
        i = p

def heap_pop(h):
    res = h[0]
    last = h.pop()
    if h:
        h[0] = last
        i = 0
        n = len(h)
        while True:
            l = 2 * i + 1
            r = l + 1
            smallest = i
            if l < n and h[l] < h[smallest]:
                smallest = l
            if r < n and h[r] < h[smallest]:
                smallest = r
            if smallest == i:
                break
            h[i], h[smallest] = h[smallest], h[i]
            i = smallest
    return res

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    arr = [int(next(it)) for _ in range(n)]

    if n == 1:
        print(0)
        return

    heap = []
    for x in arr:
        heap_push(heap, x)

    total = 0
    while len(heap) > 1:
        x = heap_pop(heap)
        y = heap_pop(heap)
        s = x + y
        total += s
        heap_push(heap, s)

    print(total)

if __name__ == "__main__":
    solve()
