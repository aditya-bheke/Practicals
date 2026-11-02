# Practical 1 – Fibonacci Numbers (Recursive and Non-Recursive)

**Aim:** Write non-recursive and recursive programs to calculate Fibonacci numbers and analyse their time and space complexity.

## Setup and run
Only **Python 3** is needed (any version 3.8+), with no extra libraries. See the main `README.md` for how to install Python on Windows, macOS or Linux. On macOS/Linux use `python3` instead of `python`.
```bash
python fibonacci.py
```
Sample input/output:
```
Enter n (position in Fibonacci series, n >= 0): 10
Fibonacci series (first 11 terms):
0 1 1 2 3 5 8 13 21 34 55
--- Non-Recursive (Iterative) ---
F(10) = 55      Loop steps : 9
--- Recursive ---
F(10) = 55      Function calls : 177
```

## Input guide
The program asks for **one number**.

| Prompt | What to type | Rules |
|---|---|---|
| `Enter n (position in Fibonacci series, n >= 0):` | a whole number, e.g. `10`, then press Enter | must be ≥ 0. Recursion is skipped when n > 35 because it would be too slow. |

**Test inputs to show the examiner:**
| Input | Expected output |
|---|---|
| `0` | F(0) = 0 |
| `1` | F(1) = 1 |
| `9` | F(9) = 34 |
| `10` | F(10) = 55. The iterative method takes 9 steps; the recursive one makes 177 calls. |
| `25` | F(25) = 75025. The recursive version makes 242,785 calls, which shows O(2ⁿ) clearly. |
| `40` | Iterative answer 102334155. Recursion is skipped. |
| `-3` | "Please enter a non-negative integer." |

## Concepts
- **Fibonacci series:** each term is the sum of the previous two. `F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)`.
- **Recursion:** a function that calls itself. It needs a **base case** (`n <= 1`) so it stops.
- **Iteration:** the same result computed with a loop. No repeated function calls are needed.
- **Time complexity:** how the running time grows with n.
- **Space complexity:** how much extra memory the method needs.

| Method | Time | Space | Why |
|---|---|---|---|
| Iterative | **O(n)** | **O(1)** | The loop runs n-1 times and only stores two variables `a` and `b` |
| Recursive | **O(2ⁿ)** | **O(n)** | Each call makes two more calls, so the call tree roughly doubles at each level. The recursion stack can be up to n calls deep. |

The recursive method recomputes the same values again and again. For example, `F(3)` gets computed several times while computing `F(5)`. That repetition is why it's exponential. The program counts the calls: for n=10 it makes 177 calls, but the loop needs only 9 steps.

## Code explanation
- `fib_iterative(n)` keeps two variables `a, b` (the last two terms). Each step does `a, b = b, a+b`. It returns the value and the step count.
- `fib_series_iterative(n)` builds the list of the first n terms so the series can be printed.
- `fib_recursive(n)` is a direct translation of the formula. The global `call_count` counts every call to show the exponential growth.
- `main()` reads n, prints the series and runs both methods. It measures time with `time.perf_counter()` and prints the complexities. Recursion is skipped when n > 35 because it would take too long. That itself demonstrates O(2ⁿ).

## Viva points
- Recursion can be made O(n) with **memoization (dynamic programming)**, i.e. storing already computed values.
- The recursion tree has about 2ⁿ nodes, and the stack depth is n.
- Using a matrix-power method, F(n) can be found in O(log n).
