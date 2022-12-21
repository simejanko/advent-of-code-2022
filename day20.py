import sys
from dataclasses import dataclass


@dataclass
class CyclicNode:
    id: int
    n: int
    prev_node: 'CyclicNode' = None
    next_node: 'CyclicNode' = None

    @staticmethod
    def from_list(numbers):
        head_node = CyclicNode(0, numbers[0])
        prev_node = head_node
        for i in range(1, len(numbers)):
            node = CyclicNode(i, numbers[i], prev_node)
            prev_node.next_node = node
            prev_node = node
        head_node.prev_node = prev_node
        prev_node.next_node = head_node
        return head_node

    def traverse(self, n):
        node = self
        for _ in range(abs(n)):
            if n > 0:
                node = node.next_node
            else:
                node = node.prev_node
        return node

    def find_id(self, id):
        node = self
        while node.id != id:
            node = node.next_node
        return node

    def find_val(self, n):
        node = self
        while node.n != n:
            node = node.next_node
        return node

    def move_after(self, node):
        if node == self or node.next_node == self:
            return

        # adjusts old neighbors
        self.prev_node.next_node, self.next_node.prev_node = self.next_node, self.prev_node
        # adjust self neighbors
        self.prev_node, self.next_node = node, node.next_node
        # adjust new neighbors
        node.next_node.prev_node, node.next_node = self, self

    def move_before(self, node):
        self.move_after(node.prev_node)

    def __str__(self):
        s = f"{self.n}*"
        node = self.next_node
        while node != self:
            s += f', {node.n} '
            node = node.next_node
        return s


def mix(numbers, result_ref=0, result_moves=(1000, 1000, 1000), repeat=1):
    node = CyclicNode.from_list(numbers)

    for _ in range(repeat):
        for i in range(len(numbers)):
            node = node.find_id(i)
            to_traverse = abs(node.n) % (len(numbers) - 1)  # on the wrap-around, skip the node we're moving
            if node.n < 0:
                to_traverse = -to_traverse
            node2 = node.traverse(to_traverse)
            if to_traverse > 0:
                node.move_after(node2)
            elif to_traverse < 0:
                node.move_before(node2)

    node = node.find_val(result_ref)

    res = []
    for n in result_moves:
        node = node.traverse(n)
        res.append(node.n)
    return sum(res)


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        numbers = [int(line.strip()) for line in f]

    # part 1
    print(mix(numbers))

    # part 2
    numbers = [811589153 * n for n in numbers]
    print(mix(numbers, repeat=10))
