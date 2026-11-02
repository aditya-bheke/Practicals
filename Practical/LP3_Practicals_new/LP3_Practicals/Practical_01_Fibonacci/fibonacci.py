"""
Practical 1 : Fibonacci numbers - Non-recursive and Recursive
Subject     : Design and Analysis of Algorithms (LP-III)

Computes the n-th Fibonacci number and prints the series using
  1. a non-recursive (iterative) method  -> Time O(n),   Space O(1)
  2. a recursive method                  -> Time O(2^n), Space O(n) (call stack)
It also counts the steps / function calls so the difference in
time complexity can be seen while running the program.
"""

import time

# ---------------------------------------------------------------
# 1. NON-RECURSIVE (ITERATIVE) METHOD
# ---------------------------------------------------------------
def fib_iterative(n):
    """Return (F(n), number_of_steps) using a simple loop."""
    if n <= 1:
        return n, 1
    a, b = 0, 1                 # F(0), F(1)
    steps = 0
    for _ in range(2, n + 1):   # loop runs n-1 times  -> O(n)
        a, b = b, a + b         # only two variables    -> O(1) space
        steps += 1
    return b, steps


def fib_series_iterative(n):
    """Return the first n terms of the series as a list."""
    series = []
    a, b = 0, 1
    for _ in range(n):
        series.append(a)
        a, b = b, a + b
    return series


# ---------------------------------------------------------------
# 2. RECURSIVE METHOD
# ---------------------------------------------------------------
call_count = 0  # global counter to show how many calls recursion makes


def fib_recursive(n):
    """Return F(n) using the recurrence F(n) = F(n-1) + F(n-2)."""
    global call_count
    call_count += 1
    if n <= 1:                  # base cases: F(0)=0, F(1)=1
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


# ---------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------
def main():
    n = int(input("Enter n (position in Fibonacci series, n >= 0): "))
    if n < 0:
        print("Please enter a non-negative integer.")
        return

    print("\nFibonacci series (first", n + 1, "terms):")
    print(*fib_series_iterative(n + 1))

    # ---- Iterative ----
    start = time.perf_counter()
    value_it, steps = fib_iterative(n)
    t_it = time.perf_counter() - start
    print("\n--- Non-Recursive (Iterative) ---")
    print(f"F({n}) = {value_it}")
    print(f"Loop steps        : {steps}")
    print(f"Time taken        : {t_it:.8f} sec")
    print("Time complexity   : O(n)")
    print("Space complexity  : O(1)")

    # ---- Recursive ----
    global call_count
    if n > 35:
        print("\n--- Recursive ---")
        print("n is too large for plain recursion (O(2^n) calls); try n <= 35.")
        return
    call_count = 0
    start = time.perf_counter()
    value_rec = fib_recursive(n)
    t_rec = time.perf_counter() - start
    print("\n--- Recursive ---")
    print(f"F({n}) = {value_rec}")
    print(f"Function calls    : {call_count}")
    print(f"Time taken        : {t_rec:.8f} sec")
    print("Time complexity   : O(2^n)")
    print("Space complexity  : O(n)  (maximum depth of recursion stack)")


if __name__ == "__main__":
    main()
