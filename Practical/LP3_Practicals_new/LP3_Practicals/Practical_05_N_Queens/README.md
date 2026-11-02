# Practical 5 – N-Queens with the First Queen Placed (Backtracking)

**Aim:** Design an n-Queens matrix with the first Queen already placed, and use backtracking to place the remaining Queens to generate the final n-Queens matrix.

## Setup and run
Only **Python 3** is needed (any version 3.8+), with no extra libraries. See the main `README.md` for how to install Python on Windows, macOS or Linux. On macOS/Linux use `python3` instead of `python`.
```bash
python n_queens.py
```
Sample:
```
Enter the value of N (board size): 8
Enter column (1 to 8) of the first Queen in row 1: 1

Q . . . . . . .
. . . . Q . . .
. . . . . . . Q
. . . . . Q . .
. . Q . . . . .
. . . . . . Q .
. Q . . . . . .
. . . Q . . . .
```
The 0/1 matrix is printed as well. Some positions have no solution (for example N=4 with the first queen in column 1), and the program reports that.

## Input guide
| Prompt | What to type | Rules |
|---|---|---|
| `Enter the value of N (board size):` | board size, e.g. `8` | N ≥ 1. N = 2 and N = 3 have no solution. |
| `Enter column (1 to N) of the first Queen in row 1:` | the column where you want the first queen, counted **from 1** | 1 ≤ column ≤ N |

**Test inputs:**
| N | First-queen column | Result |
|---|---|---|
| `8` | `1` | Solution found (Q at columns 1,5,8,6,3,7,2,4) |
| `4` | `2` | Solution found (2,4,1,3) |
| `4` | `1` | **No solution.** A queen in a corner of a 4×4 board can't be completed, so backtracking tries everything and reports this. |
| `6` | `2` | Solution found |
| `3` | `1` | No solution (no 3-queens solution exists) |

## Concepts
- **N-Queens problem:** place N queens on an N×N chessboard so that no two attack each other. That means no two queens share a **row, column or diagonal**.
- **Backtracking:** build the solution step by step (one queen per row). If at some row no column is safe, **undo the last choice (backtrack)** and try the next option. It's a depth-first search of the state-space tree that prunes unsafe branches early.
- **Safety check:** since we place exactly one queen per row, we only need to check the **column** and the **two upper diagonals** for queens already placed above.
- **Time complexity:** O(N!) in the worst case. Pruning makes it much faster in practice.
- Solutions exist for every N except 2 and 3. N=8 has 92 solutions.

## Code explanation
- `is_safe(board, row, col, n)` checks the same column above, then the upper-left diagonal, then the upper-right diagonal.
- `solve(board, row, n)` is the recursive backtracking function.
  - Base case: `row == n` means all queens are placed, so it returns True.
  - Otherwise it tries every column. If the square is safe, it places a queen (`1`) and recurses on the next row. If that fails, it removes the queen (`0`), which is the **backtrack**, and tries the next column.
- `main()` reads N and the first queen's column. It fixes that queen at `board[0][col] = 1`, then calls `solve(board, 1, n)` to start from row 2. It prints the board as Q/. and as a 0/1 matrix.

## Viva points
- Backtracking vs brute force: brute force checks all arrangements, while backtracking drops a partial solution as soon as it breaks a rule.
- Other backtracking problems: Sudoku, graph colouring, Hamiltonian cycle, subset sum.
- Two queens are on the same diagonal when `|r1 − r2| == |c1 − c2|`.
