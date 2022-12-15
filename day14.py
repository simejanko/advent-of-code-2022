import sys
import itertools
from dataclasses import dataclass

from typing import List


@dataclass
class Occupancy:
    grid: List[List[bool]]
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    has_floor: bool


def occupancy_grid(filename, floor_offset=None):
    with open(filename) as f:
        polylines = [[tuple(map(int, coord.split(','))) for coord in l.strip().split('->')] for l in f]

    all_xs1, all_xs2 = itertools.tee(x for p in polylines for x, _ in p)
    all_ys = (y for p in polylines for _, y in p)
    min_x, max_x = min(all_xs1), max(all_xs2)
    min_y, max_y = 0, max(all_ys)
    if floor_offset is not None:
        max_y += floor_offset

    grid = [[False for _ in range(max_x - min_x + 1)] for _ in range(max_y - min_y + 1)]
    if floor_offset is not None:
        for i in range(len(grid[-1])):
            grid[-1][i] = True

    for p in polylines:
        for start_idx in range(len(p) - 1):
            end_idx = start_idx + 1
            x1, y1 = p[start_idx]
            x2, y2 = p[end_idx]

            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    grid[y - min_y][x1 - min_x] = True
            else:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    grid[y1 - min_y][x - min_x] = True

    return Occupancy(grid, min_x, max_x, min_y, max_y, floor_offset is not None)


def check_resize_occupancy(occupancy, x, resize_chunk=32):
    if x < occupancy.min_x:
        occupancy.min_x -= resize_chunk
        for i in range(len(occupancy.grid) - 1):
            occupancy.grid[i] = [False for _ in range(resize_chunk)] + occupancy.grid[i]
        occupancy.grid[-1] = [occupancy.has_floor for _ in range(resize_chunk)] + occupancy.grid[-1]

    if x > occupancy.max_x:
        occupancy.max_x += resize_chunk
        for i in range(len(occupancy.grid) - 1):
            occupancy.grid[i].extend(False for _ in range(resize_chunk))
        occupancy.grid[-1].extend(occupancy.has_floor for _ in range(resize_chunk))


def simulate_single(occupancy, source):
    x, y = source
    while y < occupancy.max_y:
        for x_next, y_next in [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]:
            check_resize_occupancy(occupancy, x_next)
            if not occupancy.grid[y_next - occupancy.min_y][x_next - occupancy.min_x]:
                x, y = x_next, y_next
                break
        else:
            occupancy.grid[y - occupancy.min_y][x - occupancy.min_x] = True
            return x, y

    return None


if __name__ == '__main__':

    # part 1
    occupancy = occupancy_grid(sys.argv[1])
    n_at_rest = 0
    while simulate_single(occupancy, (500, 0)) is not None:
        n_at_rest += 1
    print(n_at_rest)

    # part 2
    occupancy = occupancy_grid(sys.argv[1], floor_offset=2)
    n_at_rest = 0
    while simulate_single(occupancy, (500, 0)) != (500, 0):
        n_at_rest += 1
    print(n_at_rest + 1)
