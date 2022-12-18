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
    jet_pattern_right_idx = itertools.cycle(range(len(jet_pattern_right)))

    full_rows_cache = dict()
    height_offset = 0
    b = 0
    while b < n_blocks:
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
        min_block_height, max_block_height = min(y for _, y in block.abs_shape_gen()), \
            max(y for _, y in block.abs_shape_gen())
        height = max(height, max_block_height)
        b += 1

        if full_rows_cache is None:  # cache already utilized
            continue

        for y in range(max_block_height, min_block_height, -1):
            if any((x, y) not in occupied_cells for x in range(1, width + 1)):
                continue

            # new block completes a row, cache indices and occupied cells above the filled row to detect repetitions
            cells_above_y = set((cx, cy - y) for cx, cy in occupied_cells if cy > y)
            cache_element = (b_idx, j_idx, tuple(sorted(cells_above_y)))

            if cache_element not in full_rows_cache:
                full_rows_cache[cache_element] = height, b
                break

            # repetition detected
            h_prev, b_prev = full_rows_cache[cache_element]
            height_diff = height - h_prev
            b_diff = b - b_prev
            remaining_blocks = n_blocks - b
            n_full_repetitions = remaining_blocks // b_diff
            height_offset = n_full_repetitions * height_diff
            n_blocks -= n_full_repetitions * b_diff
            full_rows_cache = None
            break

    return height + height_offset


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
    print(tetris(block_shapes, jet_pattern_right))  # 3171

    # part 2
    print(tetris(block_shapes, jet_pattern_right, n_blocks=1000000000000))
