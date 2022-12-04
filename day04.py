import sys

contains_count = 0
overlaps_count = 0
with open(sys.argv[1], 'r') as f:
    for line in f:
        r1, r2 = line.strip().split(',')
        r1_min, r1_max = map(int, r1.split('-'))
        r2_min, r2_max = map(int, r2.split('-'))

        if r2_min < r1_min or r2_min == r1_min and r2_max > r1_max:
            r1_min, r1_max, r2_min, r2_max = r2_min, r2_max, r1_min, r1_max

        overlaps = (r1_max >= r2_min)
        overlaps_count += overlaps
        contains_count += overlaps and (r1_max >= r2_max)

print(contains_count)
print(overlaps_count)
