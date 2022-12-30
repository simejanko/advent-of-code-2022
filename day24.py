"""Adapted from day12.py"""

import sys
import heapq
from dataclasses import dataclass
import numpy as np
from collections import defaultdict

MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]  # (0, 0) = wait
CHAR_TO_DIR = {'>': (0, 1), '<': (0, -1), 'v': (1, 0), '^': (-1, 0)}


@dataclass(order=True)
class Node:
    steps_plus_heuristic: int
    steps: int
    row: int
    col: int


def heuristic(pos, end):
    return abs(end[0] - pos[0]) + abs(end[1] - pos[1])


def blizzards_per_timestep(initial_blizzards, n_rows, n_cols):
    n_repeat = np.lcm(n_rows, n_cols)
    blizzards_per_t = []
    for time in range(n_repeat):
        blizzards = defaultdict(list)  # (row, col) -> list of dirs
        for (row, col), (row_dir, col_dir) in initial_blizzards.items():
            new_pos = (row + row_dir * time) % n_rows, (col + col_dir * time) % n_cols
            blizzards[new_pos].append((row_dir, col_dir))
        blizzards_per_t.append(blizzards)
    return blizzards_per_t


def a_star(blizzards_per_timestep, n_rows, n_cols):
    start, end = (-1, 0), (n_rows - 1, n_cols - 1)
    heap = [Node(heuristic(start, end), 0, start[0], start[1])]
    checked_nodes = {(start[0], start[1], 0)}  # row, col, timestep

    while heap:
        node = heapq.heappop(heap)
        if (node.row, node.col) == end:
            return node.steps

        moves = MOVES if node.row >= 0 else [(1, 0), (0, 0)]  # can only move down or wait at start

        new_step = node.steps + 1
        new_step_repeated = new_step % len(blizzards_per_timestep)
        new_blizzards = blizzards_per_timestep[new_step_repeated]
        for dr, dc in moves:
            new_row, new_col = node.row + dr, node.col + dc
            if (0 <= new_row < n_rows and 0 <= new_col < n_cols or
                (new_row, new_col) == start) and \
                    (new_row, new_col, new_step_repeated) not in checked_nodes and \
                    (new_row, new_col) not in new_blizzards:
                steps_plus_heuristic = new_step + heuristic((new_row, new_col), end)
                new_node = Node(steps_plus_heuristic, new_step, new_row, new_col)
                heapq.heappush(heap, new_node)
                checked_nodes.add((new_row, new_col, new_step_repeated))


if __name__ == '__main__':
    blizzards = dict()  # (row, col) -> (row_dir, col_dir)
    with open(sys.argv[1], 'r') as f:
        n_rows, n_cols = 0, len(f.readline().strip()) - 2
        for row, line in enumerate(f):
            if not line.startswith('#'):
                continue
            n_rows += 1
            for col, c in enumerate(line):
                if c not in CHAR_TO_DIR:
                    continue
                blizzards[(row, col - 1)] = CHAR_TO_DIR[c]
        n_rows -= 1

    # part 1
    blizzards_per_t = blizzards_per_timestep(blizzards, n_rows, n_cols)
    print(a_star(blizzards_per_t, n_rows, n_cols) + 1)
