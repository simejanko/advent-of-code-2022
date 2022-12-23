import sys
from dataclasses import dataclass

from typing import Tuple, List

CW_DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def occupied(i1, i2, occupancy):
    if i1 < 0 or i1 >= len(occupancy):
        return None

    offset, l = occupancy[i1]

    if i2 < offset or i2 >= offset + len(l):
        return None

    return l[i2 - offset]


with open(sys.argv[1]) as occupancy_file, open(sys.argv[2]) as path_file:
    # (offset, occupancy list) per row
    occupancy_per_row = [(line.rstrip().count(" "), [c == '#' for c in line.strip()]) for line in occupancy_file]
    # (offset, occupancy list) per col
    occupancy_per_col = [None for _ in range(max(offset + len(l) for offset, l in occupancy_per_row))]
    for row, (offset, l) in enumerate(occupancy_per_row):
        for i, o in enumerate(l):
            col = offset + i
            if occupancy_per_col[col] is None:
                occupancy_per_col[col] = (row, [])
            occupancy_per_col[col][1].append(o)

    path = []  # (step size, cw-turn bool) per command
    step_size_str = ""
    for c in path_file.readline().strip():
        if c.isdigit():
            step_size_str += c
            continue

        path.append((int(step_size_str), c == 'R'))
        step_size_str = ""
    if step_size_str:
        path.append((int(step_size_str), None))

assert (not occupancy_per_row[0][1][0])
traveler = [0, occupancy_per_row[0][0], 0]  # row, col, direction index - CW_DIRS
for step_size, cw_turn in path:
    for _ in range(step_size):
        row, col, dir_idx = traveler
        dir_row, dir_col = CW_DIRS[dir_idx]

        next_row, next_col = row + dir_row, col + dir_col
        next_pos_occupied = occupied(next_row, next_col, occupancy_per_row)
        if next_pos_occupied is None:
            if dir_col != 0:  # traversing cols
                offset, l = occupancy_per_row[next_row]
                next_col = offset + ((len(l) - 1) if next_col < offset else 0)
            else:  # traversing rows
                offset, l = occupancy_per_col[next_col]
                next_row = offset + ((len(l) - 1) if next_row < offset else 0)

            next_pos_occupied = occupied(next_row, next_col, occupancy_per_row)
            assert (next_pos_occupied is not None)

        if next_pos_occupied:
            break

        traveler[0], traveler[1] = next_row, next_col

    if cw_turn is not None:
        dir_idx = (traveler[-1] + (1 if cw_turn else -1)) % len(CW_DIRS)
        traveler[2] = dir_idx

row, col, dir_idx = traveler
password = 1000 * (1 + row) + 4 * (1 + col) + dir_idx
print(password)
