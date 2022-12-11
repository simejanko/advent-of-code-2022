import sys

X_per_cycle = [1]
with open(sys.argv[1], 'r') as f:
    for line in f:
        X = X_per_cycle[-1]
        tokens = line.strip().split()
        match tokens[0]:
            case 'noop':
                X_per_cycle.append(X)
            case 'addx':
                val = int(tokens[1])
                X_per_cycle.append(X)
                X_per_cycle.append(X + val)
# part 1
print(sum((i + 1) * X_per_cycle[i] for i in range(19, len(X_per_cycle), 40)))

# part 2
image = ""
for i, X in enumerate(X_per_cycle):
    pixel_x = i % 40
    if pixel_x == 0:
        image += '\n'
    image += '#' if abs(X - pixel_x) <= 1 else '.'
print(image)
