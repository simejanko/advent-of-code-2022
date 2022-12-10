import sys

DIRECTION_MAP = {'U': (0, 1), 'D': (0, -1), 'R': (1, 0), 'L': (-1, 0)}

head_pos = [0, 0]
tail_pos = [0, 0]
tail_visited = {(0, 0)}
with open(sys.argv[1], 'r') as f:
    for line in f:
        dir_key, size_string = line.strip().split()
        dir, size = DIRECTION_MAP[dir_key], int(size_string)
        for _ in range(size):
            head_pos[0] += dir[0]
            head_pos[1] += dir[1]

            if max(abs(tail_pos[i] - head_pos[i]) for i in (0, 1)) <= 1:
                continue

            tail_pos[0] = head_pos[0] - dir[0]
            tail_pos[1] = head_pos[1] - dir[1]
            tail_visited.add(tuple(tail_pos))
print(len(tail_visited))