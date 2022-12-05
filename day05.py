import sys
from collections import deque


def read_stacks(stacks_filename):
    with open(stacks_filename, 'r') as stacks_file:
        stacks_lines = stacks_file.readlines()
        n_stacks = 0
        for l in stacks_lines[::-1]:
            last_c = l.strip()[-1]
            if l.strip()[-1].isdigit():
                n_stacks = int(last_c)
                break
        stacks = [deque() for _ in range(n_stacks)]

        for line in stacks_lines:
            for i in range(n_stacks):
                if len(line) - 1 < i * 4 + 1:
                    break

                crate = line[i * 4 + 1]
                if crate.isupper():
                    stacks[i].appendleft(crate)

        return stacks


PICK_MULTIPLE_CRATES = True

stacks = read_stacks(sys.argv[1])
with open(sys.argv[2], 'r') as moves_file:
    for line in moves_file:
        if not line.startswith('move'):
            continue

        # move NUM from SOURCE to TARGET
        _, num, _, source_idx, _, target_idx = line.split()
        num, source_idx, target_idx = int(num), int(source_idx) - 1, int(target_idx) - 1
        crates_to_move = (stacks[source_idx].pop() for _ in range(num))
        if PICK_MULTIPLE_CRATES:
            stacks[target_idx].extend(reversed(list(crates_to_move)))
        else:
            stacks[target_idx].extend(crates_to_move)

    print(''.join(s.pop() for s in stacks if len(s) > 0))
