import sys
import numpy as np


def accumulate_is_new_max(a, axis=0, flip=False):
    if flip:
        a = np.flip(a, axis=axis)
    is_new_max = np.diff(np.maximum.accumulate(a, axis=axis), axis=axis) > 0
    if flip:
        return np.flip(is_new_max, axis=axis)
    return is_new_max


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        heightmap = np.array([list(map(int, line.strip())) for line in f])

    # part 1
    from_top = accumulate_is_new_max(heightmap, 0)[:-1, 1:-1]
    from_left = accumulate_is_new_max(heightmap, 1)[1:-1, :-1]
    from_bottom = accumulate_is_new_max(heightmap, 0, True)[1:, 1:-1]
    from_right = accumulate_is_new_max(heightmap, 1, True)[1:-1, 1:]
    is_visible = from_top | from_left | from_bottom | from_right
    border_size = 2 * heightmap.shape[0] + 2 * heightmap.shape[1] - 4
    print(np.sum(is_visible) + border_size)

    # part 2
    rows, cols = heightmap.shape
    max_score = 0
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            score1 = score2 = score3 = score4 = 0
            h = heightmap[r, c]
            for r2 in range(r + 1, rows):
                score1 += 1
                if heightmap[r2, c] >= h:
                    break
            for r2 in range(r - 1, -1, -1):
                score2 += 1
                if heightmap[r2, c] >= h:
                    break
            for c2 in range(c + 1, cols):
                score3 += 1
                if heightmap[r, c2] >= h:
                    break
            for c2 in range(c - 1, -1, -1):
                score4 += 1
                if heightmap[r, c2] >= h:
                    break
            score = score1 * score2 * score3 * score4
            if score > max_score:
                max_score = score

    print(max_score)
