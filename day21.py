import sys
from dataclasses import dataclass
import operator

OPERATORS = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.floordiv}
OPP_OPERATORS = {operator.add: operator.sub, operator.sub: operator.add, operator.mul: operator.floordiv,
                 operator.floordiv: operator.mul}


def part1(resolved, unresolved):
    while unresolved:
        for m in list(unresolved):
            m1, m2, op = unresolved[m]
            if m1 not in resolved or m2 not in resolved:
                continue
            resolved[m] = op(resolved[m1], resolved[m2])
            del unresolved[m]
    print(resolved['root'])


def part2(resolved, unresolved):
    m1, m2, op = unresolved['root']
    unresolved['root'] = (m1, m2, '=')
    resolved['humn'] = 'X'
    while unresolved:
        for m in list(unresolved):
            m1, m2, op = unresolved[m]
            if m1 not in resolved or m2 not in resolved:
                continue
            if isinstance(resolved[m1], int) and isinstance(resolved[m2], int):
                resolved[m] = op(resolved[m1], resolved[m2])
            else:
                resolved[m] = (resolved[m1], resolved[m2], op)
            del unresolved[m]

    v1, v2, _ = resolved['root']
    x, expression = (v1, v2) if isinstance(v1, int) else (v2, v1)
    while expression != 'X':
        v1, v2, op = expression
        num, expression = (v1, v2) if isinstance(v1, int) else (v2, v1)
        if num == v2 or op in (operator.add, operator.mul):
            x = OPP_OPERATORS[op](x, num)
        else:
            x = op(num, x)

    print(x)


if __name__ == '__main__':
    resolved = dict()
    unresolved = dict()
    with open(sys.argv[1]) as f:
        for line in f:
            monkey, value = line.strip().split(':')
            if value.strip().isnumeric():
                resolved[monkey] = int(value)
                continue

            for op_str, op in OPERATORS.items():
                if op_str in value:
                    m1, m2 = value.split(op_str)
                    unresolved[monkey] = (m1.strip(), m2.strip(), op)

    part1(resolved.copy(), unresolved.copy())
    part2(resolved, unresolved)
