import sys

SINGLE_SCORES = {'r': 1, 'p': 2, 's': 3}
WINNERS = {'r': 'p', 'p': 's', 's': 'r'}
LOSERS = {v: k for k, v in WINNERS.items()}
WIN_SCORE, DRAW_SCORE = 6, 3


def part1():
    ENCRYPTION_KEYS = {'A': 'r', 'B': 'p', 'C': 's', 'X': 'r', 'Y': 'p', 'Z': 's'}

    with open(sys.argv[1], 'r') as f:
        score = 0
        for line in f:
            opponent, me = ENCRYPTION_KEYS[line[0]], ENCRYPTION_KEYS[line[2]]
            score += SINGLE_SCORES[me]
            if opponent == me:
                score += DRAW_SCORE
            elif WINNERS[opponent] == me:
                score += WIN_SCORE

    return score


def part2():
    ENCRYPTION_KEYS = {'A': 'r', 'B': 'p', 'C': 's'}

    with open(sys.argv[1], 'r') as f:
        score = 0
        for line in f:
            opponent, outcome = ENCRYPTION_KEYS[line[0]], line[2]
            match outcome:
                case 'X':
                    me = LOSERS[opponent]
                case 'Z':
                    me = WINNERS[opponent]
                    score += WIN_SCORE
                case _:
                    me = opponent
                    score += DRAW_SCORE
            score += SINGLE_SCORES[me]

    return score


if __name__ == '__main__':
    print(part1())
    print(part2())
