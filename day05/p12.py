import re, os

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input_sample.txt'),
    os.path.join(DIR, 'input.txt'),
]


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as fr:
            input = fr.read()

        stacks, moves = input.split('\n\n')
        stacks = [
            [m.group(1) for m in re.finditer(r'.(.).(?: |$)', stack)]
            for stack in stacks.split('\n')[::-1][1:]
        ]
        stacks = [''.join(c for c in stack if c != ' ') for stack in zip(*stacks)]
        stacks_p2 = stacks[:]

        for move in moves.split('\n'):
            m = re.search(r'^move (\d+) from (\d+) to (\d+)$', move)
            ln, fr, to = [int(s) for s in m.groups()]
            fr -= 1
            to -= 1
            items = stacks[fr][-ln:]
            stacks[fr] = stacks[fr][:-ln]
            stacks[to] += items[::-1]

            items_p2 = stacks_p2[fr][-ln:]
            stacks_p2[fr] = stacks_p2[fr][:-ln]
            stacks_p2[to] += items_p2

        # print(stacks)
        result = ''.join(stack[-1] for stack in stacks)
        result_p2 = ''.join(stack[-1] for stack in stacks_p2)

        print(file_path, result, result_p2)


if __name__ == "__main__":
    main()
