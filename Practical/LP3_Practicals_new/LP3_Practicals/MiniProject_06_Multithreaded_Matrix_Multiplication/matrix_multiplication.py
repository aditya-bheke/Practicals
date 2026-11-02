"""
Mini Project (Group A - DAA) : Matrix multiplication vs Multithreaded matrix multiplication

Implements and compares:
  1. Normal (sequential) matrix multiplication          - triple loop, O(n^3)
  2. Multithreaded : ONE THREAD PER ROW                  - n threads
  3. Multithreaded : ONE THREAD PER CELL                 - n*n threads
  4. (Bonus) Multiprocessing : one process per CPU core  - true parallel speed-up in Python

Every method computes C = A x B, the results are checked to be identical, and the
time taken by each is printed so their performance can be analysed.
"""

import os
import random
import threading
import time
from multiprocessing import Pool

MAX_CELL_THREADS_N = 40      # thread-per-cell creates n*n threads; above this it gets impractical


# ---------------------------------------------------------------
# 1. NORMAL (SEQUENTIAL) MULTIPLICATION
# ---------------------------------------------------------------
def multiply_sequential(A, B):
    n, m, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(n)]
    for i in range(n):                 # every row of A
        for j in range(p):             # every column of B
            s = 0
            for k in range(m):         # dot product
                s += A[i][k] * B[k][j]
            C[i][j] = s
    return C


# ---------------------------------------------------------------
# 2. ONE THREAD PER ROW
# ---------------------------------------------------------------
def _compute_row(A, B, C, i):
    """Thread worker: fills row i of C. Each thread writes to a DIFFERENT row,
    so there is no race condition and no lock is needed."""
    p, m = len(B[0]), len(B)
    row = A[i]
    C[i] = [sum(row[k] * B[k][j] for k in range(m)) for j in range(p)]


def multiply_thread_per_row(A, B):
    n, p = len(A), len(B[0])
    C = [[0] * p for _ in range(n)]
    threads = [threading.Thread(target=_compute_row, args=(A, B, C, i)) for i in range(n)]
    for t in threads:
        t.start()                      # spawn
    for t in threads:
        t.join()                       # sync: wait for all rows
    return C, len(threads)


# ---------------------------------------------------------------
# 3. ONE THREAD PER CELL
# ---------------------------------------------------------------
def _compute_cell(A, B, C, i, j):
    """Thread worker: computes the single element C[i][j]."""
    C[i][j] = sum(A[i][k] * B[k][j] for k in range(len(B)))


def multiply_thread_per_cell(A, B):
    n, p = len(A), len(B[0])
    C = [[0] * p for _ in range(n)]
    threads = [threading.Thread(target=_compute_cell, args=(A, B, C, i, j))
               for i in range(n) for j in range(p)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return C, len(threads)


# ---------------------------------------------------------------
# 4. BONUS: MULTIPROCESSING (one worker process per CPU core)
# ---------------------------------------------------------------
def _rows_worker(args):
    """Process worker: computes a block of rows of C."""
    rows, B = args
    m, p = len(B), len(B[0])
    return [[sum(r[k] * B[k][j] for k in range(m)) for j in range(p)] for r in rows]


def multiply_multiprocessing(A, B):
    workers = os.cpu_count() or 2
    chunk = max(1, len(A) // workers)
    blocks = [(A[i:i + chunk], B) for i in range(0, len(A), chunk)]
    with Pool(processes=workers) as pool:
        parts = pool.map(_rows_worker, blocks)
    return [row for part in parts for row in part], workers


# ---------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------
def random_matrix(n, low=0, high=9):
    return [[random.randint(low, high) for _ in range(n)] for _ in range(n)]


def read_matrix(name, n):
    print(f"Enter matrix {name} ({n} rows, {n} numbers per row separated by spaces):")
    M = []
    for i in range(n):
        while True:
            values = input(f"  row {i + 1}: ").split()
            if len(values) == n:
                M.append([int(v) for v in values])
                break
            print(f"  Please enter exactly {n} numbers.")
    return M


def print_matrix(name, M):
    print(f"\nMatrix {name}:")
    for row in M:
        print("  " + " ".join(f"{x:5d}" for x in row))


def timed(func, *args):
    start = time.perf_counter()
    result = func(*args)
    return result, time.perf_counter() - start


def compare(A, B, show=True):
    """Run every method on A x B, check the results and print a timing table."""
    n = len(A)
    C_seq, t_seq = timed(multiply_sequential, A, B)
    rows = [("Sequential (normal)", 1, t_seq, True)]

    (C_row, n_threads), t_row = timed(multiply_thread_per_row, A, B)
    rows.append(("Thread per row", n_threads, t_row, C_row == C_seq))

    if n <= MAX_CELL_THREADS_N:
        (C_cell, n_threads), t_cell = timed(multiply_thread_per_cell, A, B)
        rows.append(("Thread per cell", n_threads, t_cell, C_cell == C_seq))

    (C_mp, n_proc), t_mp = timed(multiply_multiprocessing, A, B)
    rows.append(("Multiprocessing (bonus)", n_proc, t_mp, C_mp == C_seq))

    if show and n <= 6:
        print_matrix("A", A)
        print_matrix("B", B)
        print_matrix("C = A x B", C_seq)

    print(f"\nPerformance for {n} x {n} matrices:")
    print(f"{'Method':<26}{'Threads/Procs':>14}{'Time (s)':>12}{'Speed-up':>10}{'Correct':>9}")
    print("-" * 71)
    for name, workers, t, ok in rows:
        print(f"{name:<26}{workers:>14}{t:>12.5f}{t_seq / t:>9.2f}x{'yes' if ok else 'NO':>9}")
    if n > MAX_CELL_THREADS_N:
        print(f"(Thread per cell skipped: it would create {n * n} threads. Use n <= {MAX_CELL_THREADS_N}.)")


def benchmark():
    """Compare the methods over several sizes for the performance analysis."""
    for n in [10, 30, 60, 120, 200]:
        compare(random_matrix(n), random_matrix(n), show=False)


def main():
    print("Matrix Multiplication: Normal vs Multithreaded")
    print("1. Random matrices of a size you choose")
    print("2. Enter the matrices yourself")
    print("3. Benchmark several sizes (10, 30, 60, 120, 200) for performance analysis")
    choice = input("Enter choice (1/2/3): ").strip()

    if choice == "3":
        benchmark()
        return
    n = int(input("Enter the size n of the n x n matrices: "))
    if n < 1:
        print("n must be at least 1.")
        return
    if choice == "2":
        A, B = read_matrix("A", n), read_matrix("B", n)
    else:
        A, B = random_matrix(n), random_matrix(n)
    compare(A, B)


if __name__ == "__main__":     # required for multiprocessing on Windows / macOS
    main()
