"""
Practical 4 : 0-1 Knapsack using Dynamic Programming
Subject     : Design and Analysis of Algorithms (LP-III)

dp[i][w] = best value using the first i items with capacity w

    dp[i][w] = dp[i-1][w]                                  if wt[i] > w
             = max(dp[i-1][w], val[i] + dp[i-1][w-wt[i]])  otherwise

Each item is either taken completely (1) or not at all (0).
Time complexity  : O(n * W)
Space complexity : O(n * W)
"""


def knapsack_01(values, weights, W):
    n = len(values)
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(W + 1):
            if weights[i - 1] > w:                       # item doesn't fit
                dp[i][w] = dp[i - 1][w]
            else:                                        # max(skip, take)
                dp[i][w] = max(dp[i - 1][w],
                               values[i - 1] + dp[i - 1][w - weights[i - 1]])

    # Backtrack through the table to find which items were taken
    selected, w = [], W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:                     # item i was taken
            selected.append(i)
            w -= weights[i - 1]
    selected.reverse()
    return dp[n][W], selected, dp


def print_table(dp, W):
    print("\nDP Table (rows = items 0..n, columns = capacity 0..W):")
    print("i\\w " + " ".join(f"{w:>4}" for w in range(W + 1)))
    for i, row in enumerate(dp):
        print(f"{i:>3} " + " ".join(f"{x:>4}" for x in row))


def main():
    n = int(input("Enter number of items: "))
    values, weights = [], []
    for i in range(n):
        v, w = map(int, input(f"Enter value and weight of item {i + 1}: ").split())
        values.append(v)
        weights.append(w)
    W = int(input("Enter knapsack capacity: "))

    best, selected, dp = knapsack_01(values, weights, W)

    if W <= 20:
        print_table(dp, W)
    print(f"\nMaximum value = {best}")
    print("Items selected (1-based):", selected if selected else "None")
    print("Total weight used =", sum(weights[i - 1] for i in selected))
    print("Time complexity  : O(n*W)")


if __name__ == "__main__":
    main()
