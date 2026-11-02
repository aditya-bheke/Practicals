"""
Practical 2 : Huffman Encoding using Greedy strategy
Subject     : Design and Analysis of Algorithms (LP-III)

Steps:
  1. Count the frequency of every character.
  2. Put every character in a min-heap (priority queue) keyed by frequency.
  3. GREEDY step: repeatedly remove the two nodes with the SMALLEST frequency,
     join them under a new internal node whose frequency = sum of both,
     and push it back. Stop when one node (the root) is left.
  4. Walk the tree: left edge = '0', right edge = '1'. The path from the root
     to a leaf is that character's Huffman code.
Time complexity : O(n log n)  (n = number of distinct characters)
"""

import heapq
from collections import Counter


class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char        # None for internal nodes
        self.left = left
        self.right = right

    # heapq needs to compare nodes -> compare by frequency
    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(text):
    freq = Counter(text)
    heap = [Node(f, ch) for ch, f in freq.items()]
    heapq.heapify(heap)                      # O(n)

    if len(heap) == 1:                       # only one distinct character
        only = heapq.heappop(heap)
        return Node(only.freq, left=only), freq

    while len(heap) > 1:                     # n-1 merges
        left = heapq.heappop(heap)           # smallest frequency
        right = heapq.heappop(heap)          # second smallest
        merged = Node(left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)         # O(log n)
    return heap[0], freq


def generate_codes(node, prefix="", codes=None):
    if codes is None:
        codes = {}
    if node is None:
        return codes
    if node.char is not None:                # leaf node
        codes[node.char] = prefix or "0"
        return codes
    generate_codes(node.left, prefix + "0", codes)
    generate_codes(node.right, prefix + "1", codes)
    return codes


def encode(text, codes):
    return "".join(codes[ch] for ch in text)


def decode(bits, root):
    result, node = [], root
    for b in bits:
        node = node.left if b == "0" else node.right
        if node.char is not None:            # reached a leaf
            result.append(node.char)
            node = root
    return "".join(result)


def main():
    text = input("Enter the text to encode: ")
    if not text:
        print("Empty input.")
        return

    root, freq = build_huffman_tree(text)
    codes = generate_codes(root)

    print("\nCharacter | Frequency | Huffman Code")
    print("-" * 38)
    for ch in sorted(codes, key=lambda c: (freq[c], c)):
        shown = repr(ch) if ch == " " else ch
        print(f"{shown:^9} | {freq[ch]:^9} | {codes[ch]}")

    encoded = encode(text, codes)
    decoded = decode(encoded, root)

    original_bits = len(text) * 8
    print("\nEncoded bit string :", encoded)
    print("Decoded text       :", decoded)
    print(f"\nOriginal size      : {original_bits} bits (8 bits per char)")
    print(f"Encoded size       : {len(encoded)} bits")
    print(f"Compression ratio  : {len(encoded) / original_bits:.2%} of original")
    print("Time complexity    : O(n log n)")


if __name__ == "__main__":
    main()
