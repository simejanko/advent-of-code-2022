import sys
from functools import cmp_to_key


def compare(l1, l2):
    if isinstance(l1, int) and isinstance(l2, int):
        return 0 if l1 == l2 else (-1 if l1 < l2 else 1)
    if isinstance(l1, int):
        l1 = [l1]
    elif isinstance(l2, int):
        l2 = [l2]

    if len(l1) == 0 and len(l2) > 0:
        return -1
    if len(l2) == 0 and len(l1) > 0:
        return 1
    if len(l1) == len(l2) == 0:
        return 0

    next_el_correct_order = compare(l1[0], l2[0])
    if next_el_correct_order != 0:
        return next_el_correct_order
    return compare(l1[1:], l2[1:])


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        lists = [eval(line) for line in f if line.strip().startswith('[')]

    # part1
    print(sum(pair_idx + 1 for pair_idx, l1_i in enumerate(range(0, len(lists) - 1, 2))
              if compare(lists[l1_i], lists[l1_i + 1]) == -1))

    # part2
    div1, div2 = [[2]], [[6]]
    lists.extend((div1, div2))
    lists.sort(key=cmp_to_key(compare))
    print((lists.index(div1) + 1) * (lists.index(div2) + 1))
