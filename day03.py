import string
import sys

PRIORITIES = {c: p + 1 for p, c in enumerate(string.ascii_letters)}

with open(sys.argv[1], 'r') as f:
    backpacks = [l.strip() for l in f]
# part 1
print(sum([PRIORITIES[(set(items[:len(items) // 2]) & set(items[len(items) // 2:])).pop()] for items in backpacks]))
# part 2
print(sum([PRIORITIES[(set(backpacks[i]) & set(backpacks[i + 1]) & set(backpacks[i + 2])).pop()]
           for i in range(0, len(backpacks) - 2, 3)]))
