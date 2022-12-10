import math
import os

DIR = os.path.dirname(os.path.abspath(__file__))

FILE_PATHS = [
    os.path.join(DIR, 'input1.txt'),
    os.path.join(DIR, 'input2.txt'),
    os.path.join(DIR, 'input.txt'),
]


def main():
    for file_path in FILE_PATHS:
        with open(file_path) as f:
            lines = [line.strip().split(' ') for line in f.readlines()]

        cmds = [0 if not p_idx else int(n) for parts in lines for p_idx, n in enumerate(parts)]

        x = 1
        strength = 0
        for cmd_idx, cmd in enumerate(cmds):
            cycle = cmd_idx + 1
            if (cycle - 20) % 40 == 0:
                strength += cycle * x
            x += cmd

        result_p1 = strength
        print(file_path, result_p1)


if __name__ == "__main__":
    main()
