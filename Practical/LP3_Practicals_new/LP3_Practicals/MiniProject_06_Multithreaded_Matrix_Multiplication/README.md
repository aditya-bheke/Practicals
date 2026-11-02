# Mini Project (Group A) – Matrix Multiplication vs Multithreaded Matrix Multiplication

**Problem statement (SPPU syllabus):** Write a program to implement matrix multiplication. Also implement multithreaded matrix multiplication with either one thread per row or one thread per cell. Analyze and compare their performance.

This program implements **both** threading approaches (one thread per row and one thread per cell). It also adds a **multiprocessing** version, so you can show real parallel speed-up and explain why Python threads alone don't speed up maths.

## Files
| File | Purpose |
|---|---|
| `matrix_multiplication.py` | All four methods, correctness check and timing comparison |

## Setup and run
Only **Python 3.8+** is needed, with no extra libraries (`threading` and `multiprocessing` are built in). On macOS/Linux use `python3`.
```bash
cd MiniProject_06_Multithreaded_Matrix_Multiplication
python matrix_multiplication.py
```

## Input guide
| Prompt | What to type |
|---|---|
| `Enter choice (1/2/3):` | `1` = random matrices of a size you choose · `2` = type the matrices yourself · `3` = automatic benchmark of sizes 10, 30, 60, 120, 200 |
| `Enter the size n of the n x n matrices:` | (choices 1 and 2) a whole number, e.g. `4`. Thread-per-cell runs only when n ≤ 40, because it creates n² threads. |
| `row 1:`, `row 2:` … | (choice 2 only) **n numbers separated by spaces** for each row, first matrix A, then B |

**Test case (choice 2, hand-checkable):** n = `2`, A rows `1 2` and `3 4`, B rows `5 6` and `7 8` → C = `[[19, 22], [43, 50]]`. Matrices are printed when n ≤ 6.

**For the performance analysis**, use choice `3`, or choice `1` with n = `200` or `300`.

## Results obtained (2-core machine; your numbers will differ)
| n | Sequential | Thread per row | Thread per cell | Multiprocessing |
|---|---|---|---|---|
| 10 | 0.00005 s | 0.0013 s (10 threads) | 0.0145 s (100 threads) | 0.022 s |
| 30 | 0.0011 s | 0.0045 s | 0.136 s (900 threads) | 0.013 s |
| 120 | 0.070 s | 0.107 s | skipped | 0.068 s (1.03×) |
| 200 | 0.329 s | 0.417 s | skipped | **0.219 s (1.50×)** |

**Analysis, which is what the examiner wants to hear:**
1. **For small matrices, sequential is fastest.** Creating and joining threads or processes costs more than the multiplication itself.
2. **Thread per cell is the slowest.** It creates n² threads, each doing only n multiplications, so the overhead is enormous. Thread per row (n threads, each doing n² work) is far more practical.
3. **Python threads give no speed-up for CPU-bound work** because of the **GIL (Global Interpreter Lock)**: only one thread runs Python bytecode at a time. Threads still **run concurrently but not in parallel**. In C/C++ with pthreads, or Java threads, thread per row *would* speed up on multi-core CPUs.
4. **Multiprocessing gets real parallelism.** Each process has its own interpreter and GIL. It wins once the matrix is big enough (n ≈ 120+ here) to outweigh process start-up and data copying. On a 4–8 core laptop the speed-up will be larger.
5. **Best practice:** use about as many workers as CPU cores, each handling a block of rows. Thousands of threads waste time on creation and context switching.

## Concepts
- **Matrix multiplication:** C[i][j] = Σₖ A[i][k] · B[k][j]. For n×n matrices that is n² cells × n multiplications, so **Θ(n³)** time. Strassen's algorithm reduces it to O(n^2.81).
- **Thread:** the smallest unit of execution inside a process. Threads share the process's memory, so they're cheap to create and communicate through shared variables.
- **Process:** an independent program instance with its own memory. Processes are more expensive to start, and data must be copied (pickled) between them.
- **Multithreading:** splitting work across threads to run concurrently. On multiple cores this means parallel execution, with no GIL in C/Java.
- **Concurrency vs parallelism:** concurrency is making progress on several tasks by interleaving; parallelism is literally executing at the same time on different cores.
- **Thread per row:** n threads, and thread i computes row i of C. Each thread has work Θ(n²).
- **Thread per cell:** n² threads, and each computes one element. That's maximum parallelism but huge overhead.
- **Race condition:** two threads write to shared data at the same time and the result depends on timing. **There's none here**, because every thread writes to a *different* row or cell of C, and A and B are only read. That's why no lock is needed.
- **Work, span, speed-up** (DAA Unit VI): work T₁ = Θ(n³). With parallel loops over i and j, span T∞ = Θ(n) and parallelism T₁/T∞ = Θ(n²). Speed-up = T_sequential / T_parallel, and Amdahl's law limits it because of the serial part (thread creation, join).
- **spawn / sync:** `thread.start()` corresponds to *spawn* and `thread.join()` to *sync* in the CLRS multithreaded pseudocode.
- **GIL:** a mutex in CPython that lets only one thread execute Python bytecode at once. It makes threads useful for I/O-bound tasks (network, files) but not CPU-bound ones. Python 3.13+ has an experimental "free-threaded" build without the GIL.

## Code walkthrough
| Function | What it does |
|---|---|
| `multiply_sequential(A, B)` | Classic triple loop i, j, k |
| `_compute_row` + `multiply_thread_per_row` | Creates one `threading.Thread` per row, starts them all, then `join`s them all |
| `_compute_cell` + `multiply_thread_per_cell` | Creates one thread per (i, j) cell |
| `_rows_worker` + `multiply_multiprocessing` | Splits the rows into one block per CPU core and runs them with `multiprocessing.Pool.map` |
| `compare(A, B)` | Times every method with `time.perf_counter()`, checks each result equals the sequential one, and prints the table with speed-up |
| `benchmark()` | Runs `compare` for n = 10, 30, 60, 120, 200 |
| `if __name__ == "__main__":` | Required so multiprocessing works on Windows and macOS, where child processes re-import the file |

## Viva points
- Why is thread-per-cell slower than sequential? Thread creation overhead exceeds the tiny O(n) work per thread.
- Why no speed-up with Python threads? The GIL. Use multiprocessing, NumPy (which releases the GIL and uses optimised BLAS), or a language like C++/Java.
- How many threads are ideal? About the number of CPU cores for CPU-bound work.
- Would a race condition occur if two threads updated the same `C[i][j]` with `+=`? Yes. That would need a lock, or each thread should write to its own location.
