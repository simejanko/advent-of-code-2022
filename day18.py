import sys
from collections import deque
from itertools import product

SIDES_NORMALS = [(0, 0, -1), (0, 0, 1), (0, -1, 0), (0, 1, 0), (-1, 0, 0), (1, 0, 0)]


def count_uncovered_sides(cubes):
    return sum((x + dx, y + dy, z + dz) not in cubes for x, y, z in cubes for dx, dy, dz in SIDES_NORMALS)


def flood_fill(cubes, start_pos, bbox):
    assert (start_pos not in cubes)
    bbox_min, bbox_max = bbox
    empty_area = {start_pos}
    stack = deque([start_pos])
    is_inside = True
    while stack:
        x, y, z = stack.pop()
        for dx, dy, dz in SIDES_NORMALS:
            new_cell = x + dx, y + dy, z + dz

            if any(not (b_min <= c <= b_max) for c, b_min, b_max in zip(new_cell, bbox_min, bbox_max)):
                is_inside = False
                continue

            if new_cell not in cubes and new_cell not in empty_area:
                empty_area.add(new_cell)
                stack.append(new_cell)

    return empty_area, is_inside


def find_surface(cubes):
    xs, ys, zs = zip(*cubes)
    bbox_min = (min(xs), min(ys), min(zs))
    bbox_max = (max(xs), max(ys), max(zs))

    non_cubes = {cell for cell in product(*(range(bmin, bmax + 1) for bmin, bmax in zip(bbox_min, bbox_max)))
                 if cell not in cubes}
    inside_sides = 0
    while non_cubes:
        empty_pos = non_cubes.pop()
        empty_area, is_inside = flood_fill(cubes, empty_pos, (bbox_min, bbox_max))
        non_cubes -= empty_area
        if is_inside:
            inside_sides += count_uncovered_sides(empty_area)
    return count_uncovered_sides(cubes) - inside_sides


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        cubes = {tuple(map(int, line.split(','))) for line in f}

    # part 1
    non_cubes = {}
    print(count_uncovered_sides(cubes))

    # part 2
    print(find_surface(cubes))
