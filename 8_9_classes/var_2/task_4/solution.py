#solution.py

import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
        
    n = int(input_data[0])
    
    if n < 3:
        print(0)
        return
        
    arr = [int(x) for x in input_data[1:]]

    left_max = [0] * n
    left_max[0] = arr[0]
    for i in range(1, n):
        left_max[i] = left_max[i - 1] if left_max[i - 1] > arr[i] else arr[i]

    right_max = [0] * n
    right_max[n - 1] = arr[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = right_max[i + 1] if right_max[i + 1] > arr[i] else arr[i]

    max_single_pool = 0
    current_pool = 0
    
    for i in range(1, n - 1):
        bound = left_max[i] if left_max[i] < right_max[i] else right_max[i]
        
        if bound > arr[i]:
            current_pool += bound - arr[i]
        else:
            if current_pool > max_single_pool:
                max_single_pool = current_pool
            current_pool = 0
            
    if current_pool > max_single_pool:
        max_single_pool = current_pool

    print(max_single_pool)

if __name__ == "__main__":
    solve()