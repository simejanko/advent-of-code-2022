from typing import Callable, Iterable
import math


class Monkey:
    def __init__(self, starting_items: Iterable[int], worry_op: Callable[[int], int], throw_test_div: int,
                 worry_dropoff: int = 1):
        self.items = list(starting_items)
        self.worry_op = worry_op
        self.worry_dropoff = worry_dropoff
        self.throw_test_div = throw_test_div
        self.items_inspected = 0

        self.throw_to = None
        self.lcm_squared = 1

    def set_throw_to(self, m1: 'Monkey', m2: 'Monkey'):
        self.throw_to = (m1, m2)

    def inspect_items(self):
        if self.throw_to is None:
            raise ValueError("Uninitialized monkey")

        for worry_level in self.items:
            worry_level = self.worry_op(worry_level)
            if self.worry_dropoff != 1:
                worry_level = int(worry_level / self.worry_dropoff)

            if worry_level > self.lcm_squared:
                worry_level %= self.lcm_squared

            if self.throw_to:
                self.throw_to[worry_level % self.throw_test_div == 0].items.append(worry_level)

        self.items_inspected += len(self.items)
        self.items = []


if __name__ == '__main__':
    N_ROUNDS = 10000

    monkeys = [Monkey([83, 62, 93], lambda x: x * 17, 2), Monkey([90, 55], lambda x: x + 1, 17),
               Monkey([91, 78, 80, 97, 79, 88], lambda x: x + 3, 19), Monkey([64, 80, 83, 89, 59], lambda x: x + 5, 3),
               Monkey([98, 92, 99, 51], lambda x: x * x, 5),
               Monkey([68, 57, 95, 85, 98, 75, 98, 75], lambda x: x + 2, 13),
               Monkey([74], lambda x: x + 4, 7), Monkey([68, 64, 60, 68, 87, 80, 82], lambda x: x * 19, 11)]

    monkeys[0].set_throw_to(monkeys[6], monkeys[1])
    monkeys[1].set_throw_to(monkeys[3], monkeys[6])
    monkeys[2].set_throw_to(monkeys[5], monkeys[7])
    monkeys[3].set_throw_to(monkeys[2], monkeys[7])
    monkeys[4].set_throw_to(monkeys[1], monkeys[0])
    monkeys[5].set_throw_to(monkeys[0], monkeys[4])
    monkeys[6].set_throw_to(monkeys[2], monkeys[3])
    monkeys[7].set_throw_to(monkeys[5], monkeys[4])

    monkeys_div_lcm_squared = math.lcm(*[m.throw_test_div for m in monkeys])
    monkeys_div_lcm_squared *= monkeys_div_lcm_squared

    for m in monkeys:
        m.lcm_squared = monkeys_div_lcm_squared

    for i in range(N_ROUNDS):
        for monkey in monkeys:
            monkey.inspect_items()

    monkeys.sort(key=lambda m: m.items_inspected)
    print(monkeys[-1].items_inspected * monkeys[-2].items_inspected)
