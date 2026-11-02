# Practical 3 – Fractional Knapsack (Greedy Method)

**Aim:** Write a program to solve the fractional Knapsack problem using the greedy method.

## Setup and run
Only **Python 3** is needed (any version 3.8+), with no extra libraries. See the main `README.md` for how to install Python on Windows, macOS or Linux. On macOS/Linux use `python3` instead of `python`.
```bash
python fractional_knapsack.py
```
Sample (the classic textbook example):
```
Enter number of items: 3
Enter value and weight of item 1: 60 10
Enter value and weight of item 2: 100 20
Enter value and weight of item 3: 120 30
Enter knapsack capacity: 50
...
Maximum value in knapsack = 240.00
```
Items 1 and 2 are taken fully, plus 2/3 of item 3: 60 + 100 + 80 = 240.

## Input guide
| Prompt | What to type | Example |
|---|---|---|
| `Enter number of items:` | number of items n | `3` |
| `Enter value and weight of item i:` | **two numbers on one line, separated by a space**: value first, then weight. Asked n times. | `60 10` |
| `Enter knapsack capacity:` | maximum weight the bag can hold | `50` |

Weights must be > 0. Decimals are allowed (e.g. `12.5 3.2`).

**Test case 1 (textbook):** n=3, items `60 10`, `100 20`, `120 30`, capacity `50` → **240.00**. Items 1 and 2 are taken fully, and 0.67 of item 3.

**Test case 2:** n=7, items `10 2`, `5 3`, `15 5`, `7 7`, `6 1`, `18 4`, `3 1`, capacity `15` → **55.33** (Horowitz–Sahni example).

**Test case 3:** n=2, items `100 20`, `60 10`, capacity `40` → **160.00** (everything fits).

## Concepts
- **Knapsack problem:** you have items with a value and a weight, and a bag with a fixed capacity. The goal is to maximise the total value without exceeding the capacity.
- **Fractional knapsack:** items can be **broken**, so you can take part of an item. The opposite is 0-1 knapsack (Practical 4).
- **Greedy method:** sort items by **value/weight ratio** (profit per unit weight) and keep taking the best item. When an item doesn't fully fit, take the fraction that fills the bag. For the fractional version, greedy always gives the **optimal** answer.
- **Time complexity:** O(n log n) for sorting, plus O(n) for the selection loop.

## Code explanation
- `class Item` stores the index, value, weight and `ratio = value / weight`.
- `fractional_knapsack()`:
  1. sorts items by ratio, highest first
  2. loops over them: if `weight <= remaining`, it takes the whole item. Otherwise it takes `fraction = remaining / weight`, adds `value * fraction` and stops.
  3. returns the total value and the list of `(item, fraction)` pairs.
- `main()` reads the input and prints a table of the selected items with their fractions, plus the maximum value.

## Viva points
- Greedy **doesn't** work for 0-1 knapsack, because items can't be split there. Use DP instead.
- Applications include loading cargo and resource allocation, where resources are divisible.
