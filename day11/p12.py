from functools import reduce
import re, os, math, copy
from dataclasses import dataclass


DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input1.txt'),
    os.path.join(DIR, 'input.txt'),
]


methods = {
    '+': '__add__',
    '*': '__mul__',
}


@dataclass
class Monkey:
    items: list
    operator: str
    literal: int
    variable: str
    divisor: int
    idx_true: int
    idx_false: int
    inspected_count: int = 0


def play(monkeys, rounds, use_boring):
    g_divisor = reduce(lambda a, b: abs(a * b) // math.gcd(a, b), [m.divisor for m in monkeys])

    for r_idx in range(rounds):
        for m_idx, m in enumerate(monkeys):
            while len(m.items):
                item = m.items.pop(0)
                m.inspected_count += 1
                method = methods[m.operator]
                op2 = m.literal if m.literal is not None else item
                item = getattr(item, method)(op2)
                if use_boring:
                    item = math.floor(item / 3)
                item = item % g_divisor
                next_idx = m.idx_true if item % m.divisor == 0 else m.idx_false
                monkeys[next_idx].items.append(item)

    counts = sorted([m.inspected_count for m in monkeys], reverse=True)

    return counts[0] * counts[1]


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as fr:
            input_str = fr.read()

        monkeys = []
        for m in re.finditer(r'Monkey (?:\d+):\n  Starting items: ([\d, ]+)\n  Operation: new = old ([*+]) (?:(\d+)|(old))\n  Test: divisible by (\d+)\n    If true: throw to monkey (\d+)\n    If false: throw to monkey (\d+)', input_str):
            items_str, operator, literal, variable, divisor, idx_true, idx_false = m.groups()
            items = [int(s) for s in items_str.split(', ')]
            literal = int(literal) if literal is not None else None
            divisor = int(divisor)
            idx_true = int(idx_true)
            idx_false = int(idx_false)
            monkey = Monkey(items, operator, literal, variable, divisor, idx_true, idx_false)
            monkeys.append(monkey)

        result_p1 = play(copy.deepcopy(monkeys), 20, True)
        result_p2 = play(copy.deepcopy(monkeys), 10000, False)
        print(file_path, result_p1, result_p2)


if __name__ == "__main__":
    main()
