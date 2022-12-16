import sys
import re

def manhattan_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

sensor_to_beacon_dist = dict()
beacons = set()
with open(sys.argv[1]) as f:
    for line in f:
        s_x, s_y, b_x, b_y = map(int, re.findall(r'-?\d+', line))
        sensor_to_beacon_dist[(s_x, s_y)] = manhattan_dist(s_x, s_y, b_x, b_y)
        beacons.add((b_x, b_y))

min_x = min(s_x - d for (s_x, _), d in sensor_to_beacon_dist.items())
max_x = max(s_x + d for (s_x, _), d in sensor_to_beacon_dist.items())

print((min_x, max_x))

Y = 2000000
empty_n = sum(any(manhattan_dist(x, Y, s_x, s_y) <= d for (s_x, s_y), d in sensor_to_beacon_dist.items())
                for x in range(min_x, max_x+1) if (x, Y) not in beacons)
print(empty_n)