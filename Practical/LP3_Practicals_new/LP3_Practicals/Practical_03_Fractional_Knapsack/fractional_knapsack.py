"""
Practical 3 : Fractional Knapsack using Greedy method
Subject     : Design and Analysis of Algorithms (LP-III)

Greedy choice: always pick the item with the highest value/weight ratio.
If the whole item fits, take it fully; otherwise take the fraction that fills
the remaining capacity and stop.
Time complexity : O(n log n)  (because of sorting by ratio)
"""


class Item:
    def __init__(self, index, value, weight):
        self.index = index
        self.value = value
        self.weight = weight
        self.ratio = value / weight


def fractional_knapsack(capacity, items):
    # Step 1: sort items by value/weight ratio in decreasing order
    items = sorted(items, key=lambda it: it.ratio, reverse=True)

    total_value = 0.0
    remaining = capacity
    taken = []                       # (item, fraction taken)

    # Step 2: pick greedily
    for it in items:
        if remaining <= 0:
            break
        if it.weight <= remaining:   # whole item fits
            remaining -= it.weight
            total_value += it.value
            taken.append((it, 1.0))
        else:                        # take only a fraction
            fraction = remaining / it.weight
            total_value += it.value * fraction
            taken.append((it, fraction))
            remaining = 0
    return total_value, taken


def main():
    n = int(input("Enter number of items: "))
    items = []
    for i in range(n):
        v, w = map(float, input(f"Enter value and weight of item {i + 1}: ").split())
        if w <= 0:
            print("Weight must be positive.")
            return
        items.append(Item(i + 1, v, w))
    capacity = float(input("Enter knapsack capacity: "))

    total, taken = fractional_knapsack(capacity, items)

    print("\nItems sorted by value/weight ratio and selected:")
    print("Item | Value | Weight | Ratio | Fraction taken")
    print("-" * 48)
    for it, frac in taken:
        print(f"{it.index:^4} | {it.value:^5g} | {it.weight:^6g} | {it.ratio:^5.2f} | {frac:.2f}")
    print(f"\nMaximum value in knapsack = {total:.2f}")
    print("Time complexity : O(n log n)")


if __name__ == "__main__":
    main()
