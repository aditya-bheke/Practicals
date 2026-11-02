"""
Practical 5 : N-Queens with the first Queen already placed (Backtracking)
Subject     : Design and Analysis of Algorithms (LP-III)

The user places the first queen at (row 0, column c). The program then uses
BACKTRACKING to place one queen in every remaining row so that no two queens
attack each other (same column or same diagonal), and prints the final matrix.

Backtracking idea:
  place(row):
      if row == n: solution found
      for every column col:
          if (row, col) is safe:
              put queen, call place(row + 1)
              if that fails -> remove queen (BACKTRACK) and try next column
Time complexity : O(n!) in the worst case
"""


def is_safe(board, row, col, n):
    # Check the same column in the rows above
    for r in range(row):
        if board[r][col] == 1:
            return False
    # Check upper-left diagonal
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0:
        if board[r][c] == 1:
            return False
        r, c = r - 1, c - 1
    # Check upper-right diagonal
    r, c = row - 1, col + 1
    while r >= 0 and c < n:
        if board[r][c] == 1:
            return False
        r, c = r - 1, c + 1
    return True


def solve(board, row, n):
    if row == n:                         # all queens placed
        return True
    for col in range(n):
        if is_safe(board, row, col, n):
            board[row][col] = 1          # place queen
            if solve(board, row + 1, n):
                return True
            board[row][col] = 0          # BACKTRACK
    return False


def print_board(board):
    for row in board:
        print(" ".join("Q" if x else "." for x in row))
    print("\nAs 0/1 matrix:")
    for row in board:
        print(row)


def main():
    n = int(input("Enter the value of N (board size): "))
    if n < 1:
        print("N must be at least 1.")
        return
    col = int(input(f"Enter column (1 to {n}) of the first Queen in row 1: ")) - 1
    if not 0 <= col < n:
        print("Invalid column.")
        return

    board = [[0] * n for _ in range(n)]
    board[0][col] = 1                    # first queen fixed by the user

    if solve(board, 1, n):               # start backtracking from row 2
        print(f"\nFinal {n}-Queens matrix (first queen at row 1, column {col + 1}):\n")
        print_board(board)
    else:
        print(f"\nNo solution exists for N = {n} with the first queen at column {col + 1}.")


if __name__ == "__main__":
    main()
