# Practical 4 – 0-1 Knapsack (Dynamic Programming)

**Aim:** Write a program to solve the 0-1 Knapsack problem using dynamic programming.

## Setup and run
Only **Python 3** is needed (any version 3.8+), with no extra libraries. See the main `README.md` for how to install Python on Windows, macOS or Linux. On macOS/Linux use `python3` instead of `python`.
```bash
python knapsack_01_dp.py
```
Sample:
```
Enter number of items: 4
Enter value and weight of item 1: 1 1
Enter value and weight of item 2: 4 3
Enter value and weight of item 3: 5 4
Enter value and weight of item 4: 7 5
Enter knapsack capacity: 7
(DP table printed)
Maximum value = 9
Items selected (1-based): [2, 3]
```
The DP table is printed when capacity ≤ 20, so you can show it to the examiner.

## Input guide
| Prompt | What to type | Example |
|---|---|---|
| `Enter number of items:` | number of items n | `4` |
| `Enter value and weight of item i:` | **two whole numbers on one line**: value then weight. Asked n times. | `4 3` |
| `Enter knapsack capacity:` | whole number W | `7` |

Use **integers only**, because the DP table is indexed by weight. The table is printed when W ≤ 20.

**Test case 1:** n=4, items `1 1`, `4 3`, `5 4`, `7 5`, W=`7` → **9**, items [2, 3].

**Test case 2 (shows greedy fails):** n=3, items `60 10`, `100 20`, `120 30`, W=`50` → **220**, items [2, 3]. Greedy by ratio would choose items 1 and 2 and get only 160.

**Test case 3:** n=3, items `10 5`, `40 4`, `30 6`, W=`10` → **70**, items [2, 3].

## Concepts
- **0-1 Knapsack:** each item is either taken **completely (1)** or **not at all (0)**. Items can't be split, so greedy fails here.
- **Dynamic programming:** solve smaller subproblems once, store the answers in a table, and build up to the full answer. It needs two properties:
  - **Optimal substructure:** the best answer is made from best answers to smaller problems.
  - **Overlapping subproblems:** the same subproblems repeat, so storing them saves time.
- **Recurrence**, where `dp[i][w]` is the best value using the first i items with capacity w:
```
dp[i][w] = dp[i-1][w]                                     if wt[i] > w
         = max(dp[i-1][w], val[i] + dp[i-1][w - wt[i]])   otherwise
```
  The first option means not taking item i. The second means taking it.
- **Time complexity:** O(n·W). **Space complexity:** O(n·W).

## Code explanation
- `knapsack_01()` creates an `(n+1) × (W+1)` table of zeros. Row 0 and column 0 are 0 because no items or no capacity gives value 0. It fills the table with the recurrence.
- **Backtracking to find the items:** start at `dp[n][W]`. If `dp[i][w] != dp[i-1][w]`, item i was taken, so subtract its weight and move up a row.
- `print_table()` prints the table neatly.
- `main()` reads the input and prints the table, the maximum value, the selected items and the total weight.

## Viva points
- Brute force would check all 2ⁿ subsets. DP reduces this to O(n·W), which is **pseudo-polynomial** because it depends on the numeric value W.
- **Branch and Bound** is another approach. It explores a state-space tree and prunes branches using an upper bound from fractional knapsack.
- Greedy vs DP: greedy picks the best local option, while DP considers all options through the table.
