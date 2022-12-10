import sys

DIRECTION_MAP = {'U': (0, 1), 'D': (0, -1), 'R': (1, 0), 'L': (-1, 0)}
N_KNOTS = 10

all_knots_pos = [[0, 0] for _ in range(N_KNOTS)]
head_pos, tail_pos = all_knots_pos[0], all_knots_pos[-1]
tail_visited = {(0, 0)}
with open(sys.argv[1], 'r') as f:
    for line in f:
        dir_key, size_string = line.strip().split()
        head_direction, size = DIRECTION_MAP[dir_key], int(size_string)
        for _ in range(size):
            head_pos[0] += head_direction[0]
            head_pos[1] += head_direction[1]

            for prev_i, knot_pos in enumerate(all_knots_pos[1:]):
                prev_knot_pos = all_knots_pos[prev_i]
                coord_diffs = [(abs(knot_pos[coord] - prev_knot_pos[coord]), coord) for coord in (0, 1)]
                min_coord_delta, min_coord = min(coord_diffs)
                max_coord_delta, max_coord = max(coord_diffs)

                if max_coord_delta == 2:
                    knot_pos[max_coord] += 1 if prev_knot_pos[max_coord] > knot_pos[max_coord] else -1
                    if min_coord_delta >= 1:
                        knot_pos[min_coord] += 1 if prev_knot_pos[min_coord] > knot_pos[min_coord] else -1
                else:
                    break

            tail_visited.add(tuple(tail_pos))
print(len(tail_visited))
