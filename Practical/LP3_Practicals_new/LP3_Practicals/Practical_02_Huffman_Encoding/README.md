# Practical 2 – Huffman Encoding (Greedy Strategy)

**Aim:** Write a program to implement Huffman Encoding using a greedy strategy.

## Setup and run
Only **Python 3** is needed (any version 3.8+), with no extra libraries. See the main `README.md` for how to install Python on Windows, macOS or Linux. On macOS/Linux use `python3` instead of `python`.
```bash
python huffman.py
```
Sample:
```
Enter the text to encode: aabbbcccc dddddeeeee
Character | Frequency | Huffman Code
   ' '    |     1     | 1110
    a     |     2     | 1111
    b     |     3     | 110
    c     |     4     | 00
    d     |     5     | 10
    e     |     5     | 01
Original size : 160 bits   Encoded size : 49 bits
```
(When frequencies are tied, the exact 0/1 codes can differ from a hand-drawn tree. The total encoded length is still optimal.)

## Input guide
The program asks for **one line of text**.

| Prompt | What to type | Rules |
|---|---|---|
| `Enter the text to encode:` | any sentence or word, then press Enter. Spaces are allowed. | must not be empty |

**Test inputs:**
| Input | What happens |
|---|---|
| `aabbbcccc dddddeeeee` | 6 distinct characters. Frequent ones (d, e, c) get 2-bit codes; rare ones (space, a) get 4-bit codes. 160 bits → 49 bits. |
| `hello world` | `l` (3 times, the most frequent) gets a short 2-bit code. 88 bits → 32 bits, and the decoded text matches the input. |
| `aaaa` | Only one distinct character, so its code is `0` and the output is 4 bits. |
| `abracadabra` | `a` (5 times) gets a 1-bit code. |

Try typing words where some letters repeat a lot, so you can explain why they get shorter codes.

## Concepts
- **Huffman coding** is a **lossless data compression** method. Characters that appear often get **short codes**, and rare characters get longer codes.
- **Prefix code:** no code is a prefix of another code, so the bit string can be decoded without separators.
- **Greedy strategy:** at every step the algorithm makes the locally best choice, which is merging the two **least frequent** nodes. For Huffman coding this local choice leads to the globally optimal (minimum-length) code.
- **Min-heap / priority queue:** gives the smallest-frequency node in O(log n).
- **Time complexity:** O(n log n), where n is the number of distinct characters. There are n-1 merges, each costing O(log n) heap operations.

## Algorithm
1. Count the frequency of each character.
2. Create a leaf node for each character and push it into a min-heap.
3. While the heap has more than one node:
   - pop the two smallest nodes (`left`, `right`)
   - create a new internal node with `freq = left.freq + right.freq`
   - push it back.
4. The remaining node is the root. Traverse the tree: left = `0`, right = `1`.

## Code explanation
- `class Node` stores `freq`, `char` (None for internal nodes), and `left`/`right` children. `__lt__` lets `heapq` compare nodes by frequency.
- `build_huffman_tree()` uses `Counter` for frequencies, `heapq.heapify` to build the heap, and the greedy merge loop. If there's only one distinct character, it's handled specially.
- `generate_codes()` does a recursive traversal that appends `0`/`1` to the path and stores each leaf's code in a dictionary.
- `encode()` replaces every character with its code.
- `decode()` walks the tree bit by bit and outputs a character whenever it reaches a leaf. This proves the prefix property works.
- `main()` prints the frequency/code table, the encoded bits, the decoded text and the compression ratio compared with 8-bit ASCII.

## Viva points
- Huffman coding is used in ZIP, JPEG and MP3 compression.
- Huffman codes are optimal among prefix codes.
- Fixed-length coding would need ⌈log₂ n⌉ bits per character. Huffman uses variable lengths.
