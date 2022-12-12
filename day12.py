import sys
import heapq
from dataclasses import dataclass

MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0)]


@dataclass(order=True)
class Node:
    steps_plus_heuristic: int
    steps: int
    row: int
    col: int


def heuristic(pos, end, height, height_end=ord('z') - ord('a')):
    return max((abs(end[0] - pos[0]) + abs(end[1] - pos[1])), height_end - height)


def a_star(heightmap, starts, end):
    n_rows, n_cols = len(heightmap), len(heightmap[0])

    heap = [Node(heuristic(start, end, heightmap[s_row][s_col]), 0, s_row, s_col) for s_row, s_col in starts]
    heapq.heapify(heap)

    checked_nodes = {(s_row, s_col) for s_row, s_col in starts}
    while heap:
        node = heapq.heappop(heap)
        if (node.row, node.col) == end:
            return node.steps

        h = heightmap[node.row][node.col]
        for dr, dc in MOVES:
            new_row, new_col = node.row + dr, node.col + dc
            if 0 <= new_row < n_rows and 0 <= new_col < n_cols and (new_row, new_col) not in checked_nodes:
                new_h = heightmap[new_row][new_col]
                if new_h - h > 1:
                    continue

                steps_plus_heuristic = node.steps + 1 + heuristic((new_row, new_col), end, new_h)
                new_node = Node(steps_plus_heuristic, node.steps + 1, new_row, new_col)
                heapq.heappush(heap, new_node)
                checked_nodes.add((new_row, new_col))


if __name__ == '__main__':
    heightmap = []
    start, end = None, None
    lowest_points = []

    with open(sys.argv[1], 'r') as f:
        for row, line in enumerate(f):
            row_heights = []
            for col, c in enumerate(line.strip()):
                if c == 'S':
                    start = (row, col)
                    c = 'a'
                elif c == 'E':
                    end = (row, col)
                    c = 'z'
                if c == 'a':
                    lowest_points.append((row, col))
                row_heights.append(ord(c) - ord('a'))
            heightmap.append(row_heights)

    # part1
    print(a_star(heightmap, [start], end))

    # part 2
    print(a_star(heightmap, lowest_points, end))
