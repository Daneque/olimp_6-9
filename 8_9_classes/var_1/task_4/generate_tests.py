#!/usr/bin/env python3
import sys
import os
import random

INF = 10**30

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

def solve_instance(a):
    n = len(a)
    if n == 1:
        return 0
    heap = []
    for x in a:
        heap_push(heap, x)
    total = 0
    while len(heap) > 1:
        x = heap_pop(heap)
        y = heap_pop(heap)
        s = x + y
        total += s
        heap_push(heap, s)
    return total

def main():
    if len(sys.argv) < 3:
        print("Usage: generate_tests.py <count> <dir>")
        return

    t = int(sys.argv[1])
    out_dir = sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)

    rnd = random.Random(123456)

    for test_id in range(1, t + 1):
        if test_id == 1:
            n = 1
        elif test_id == 2:
            n = 2
        else:
            n = rnd.randint(1, 1000)

        a = []
        for _ in range(n):
            a.append(rnd.randint(1, 10**6))

        ans = solve_instance(a)

        in_path = os.path.join(out_dir, f"{test_id}.in")
        out_path = os.path.join(out_dir, f"{test_id}.out")

        with open(in_path, "w") as fin:
            fin.write(str(n) + "\n")
            if n > 0:
                fin.write(" ".join(map(str, a)) + "\n")

        with open(out_path, "w") as fout:
            fout.write(str(ans))

if __name__ == "__main__":
    main()