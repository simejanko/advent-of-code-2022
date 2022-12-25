import sys
from itertools import product
from collections import defaultdict

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def simulate(elves, max_rounds=None):
    round = 0
    while max_rounds is None or round < max_rounds:
        proposed_moves = defaultdict(list)  # target position -> list of source positions
        new_elves = set()
        for row, col in elves:
            any_elves_around = any((row + drow, col + dcol) in elves
                                   for drow, dcol in product(range(-1, 2), repeat=2) if not (drow == 0 and dcol == 0))
            if not any_elves_around:
                new_elves.add((row, col))
                continue

            # first direction to try depends on round
            for dir_i in range(round, round + len(DIRECTIONS)):
                drow, dcol = DIRECTIONS[dir_i % len(DIRECTIONS)]
                new_row, new_col = row + drow, col + dcol
                is_valid_move = not any(((new_row, new_col + d) if drow != 0 else (new_row + d, new_col))
                                        in elves for d in range(-1, 2))
                if is_valid_move:
                    proposed_moves[(new_row, new_col)].append((row, col))
                    break
            else:
                new_elves.add((row, col))

        if not proposed_moves:
            round += 1
            break

        for target, sources in proposed_moves.items():
            if len(sources) == 1:
                new_elves.add(target)
            else:
                new_elves.update(sources)  # multiple elves with the same target

        assert (len(elves) == len(new_elves))
        elves = new_elves

        round += 1
    return elves, round


def bbox(elves):
    return min(row for row, _ in elves), min(col for _, col in elves), \
           max(row for row, _ in elves), max(col for _, col in elves)


if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        elves = {(row, col) for (row, line) in enumerate(file) for (col, c) in enumerate(line) if c == '#'}

    # part 1
    new_elves, _ = simulate(elves, 10)
    min_row, min_col, max_row, max_col = bbox(new_elves)
    n_empty = (max_row - min_row + 1) * (max_col - min_col + 1) - len(elves)
    print(n_empty)

    # part 2
    _, rounds = simulate(elves)
    print(rounds)
