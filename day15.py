import sys
import re


def manhattan_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def is_beacon_possible(pos, sensor_to_beacon_dist):
    return all(manhattan_dist(pos[0], pos[1], s_x, s_y) > d for (s_x, s_y), d in sensor_to_beacon_dist.items())


def manhattan_ball_gen(center, rad):
    pos = [center[0] - rad, center[1]]
    for dx, dy in [(1, 1), (1, -1), (-1, -1), (-1, 1)]:
        approach_axis = int(pos[0] == center[0])  # 0 if x differs, 1 if y differs
        while pos[approach_axis] != center[approach_axis]:
            pos[0] += dx
            pos[1] += dy
            yield pos


if __name__ == '__main__':
    sensor_to_beacon_dist = dict()
    beacons = set()
    with open(sys.argv[1]) as f:
        for line in f:
            s_x, s_y, b_x, b_y = map(int, re.findall(r'-?\d+', line))
            sensor_to_beacon_dist[(s_x, s_y)] = manhattan_dist(s_x, s_y, b_x, b_y)
            beacons.add((b_x, b_y))

    # part 1
    Y = 2000000
    min_x = min(s_x - d for (s_x, _), d in sensor_to_beacon_dist.items())
    max_x = max(s_x + d for (s_x, _), d in sensor_to_beacon_dist.items())
    print(sum(not is_beacon_possible((x, Y), sensor_to_beacon_dist)
              for x in range(min_x, max_x + 1) if (x, Y) not in beacons))

    # part 2
    min_x, max_x = 0, 4000000
    min_y, max_y = 0, 4000000
    for s, d in sensor_to_beacon_dist.items():
        for x, y in manhattan_ball_gen(s, d + 1):
            if min_x <= x <= max_x and min_y <= y <= max_y and is_beacon_possible((x, y), sensor_to_beacon_dist):
                print(x * max_x + y)
                exit(0)
