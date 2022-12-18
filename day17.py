import sys
from dataclasses import dataclass
import itertools

from typing import Tuple, List


@dataclass
class Block:
    x: int
    y: int
    rel_shape: List[Tuple[int, int]]

    def abs_shape_gen(self):
        return ((self.x + dx, self.y + dy) for dx, dy in self.rel_shape)


def move_if_possible(block, move, occupied_cells, x_lim, y_lim):
    dx, dy = move
    block.x += dx
    block.y += dy

    if all(p not in occupied_cells and
           (x_lim[0] is None or p[0] >= x_lim[0]) and
           (x_lim[1] is None or p[0] <= x_lim[1]) and
           (y_lim[0] is None or p[1] >= y_lim[0]) and
           (y_lim[1] is None or p[1] <= y_lim[1])
           for p in block.abs_shape_gen()):
        return True

    # move not possible
    block.x -= dx
    block.y -= dy
    return False


def tetris(block_shapes, jet_pattern_right, n_blocks=2022, width=7, start_offset=(3, 4)):
    sx, sy = start_offset
    height = 0
    occupied_cells = set()
    block_shapes_idx = itertools.cycle(range(len(block_shapes)))
    jet_pattern_right_idx= itertools.cycle(range(len(jet_pattern_right)))
    for _ in range(n_blocks):
        b_idx = next(block_shapes_idx)
        block = Block(sx, height + sy, block_shapes[b_idx])

        while True:
            j_idx = next(jet_pattern_right_idx)
            move_if_possible(block, (1, 0) if jet_pattern_right[j_idx] else (-1, 0),
                             occupied_cells, (1, width), (1, None))
            able_to_fall = move_if_possible(block, (0, -1), occupied_cells, (1, width), (1, None))
            if not able_to_fall:
                break

        occupied_cells.update(block.abs_shape_gen())
        height = max(height, max(y for _, y in block.abs_shape_gen()))
    return height


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        jet_pattern_right = [c == '>' for c in f.read().strip()]

    # origin = bottom left
    block_shapes = [[(0, 0), (1, 0), (2, 0), (3, 0)],
                    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
                    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
                    [(0, 0), (0, 1), (0, 2), (0, 3)],
                    [(0, 0), (0, 1), (1, 0), (1, 1)]]

    # part 1
    print(tetris(block_shapes, jet_pattern_right))
