import sys
from collections import Counter

WINDOW_SIZE = 14
with open(sys.argv[1], 'r') as f:
    s = f.read().strip()
window_counts = Counter(s[:WINDOW_SIZE])
for out_idx, in_c in enumerate(s[WINDOW_SIZE:]):
    in_idx = out_idx + WINDOW_SIZE
    out_c = s[out_idx]

    if len(window_counts) == WINDOW_SIZE:
        print(in_idx)
        break

    window_counts[in_c] += 1
    window_counts[out_c] -= 1
    if window_counts[out_c] == 0:
        del window_counts[out_c]


